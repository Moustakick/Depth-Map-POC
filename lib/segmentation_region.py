import numpy as np
import random
import pickle
import cv2
import time
import os

def initializeRegion(img_depth): # initialise les régions
    height = img_depth.shape[0]
    width = img_depth.shape[1]
    list_region = []
    pixelinregion = np.zeros(height*width)
    pixelUsed = np.zeros(height*width)
    cpt =0
    for i in range(height):
       for j in range(width):
          pixelinregion[i*width+j] = (int) (-1)
    return pixelinregion, list_region, pixelUsed

def findRegion(p,  pixelinregion): # retourne la région où se trouve un pixel
        return pixelinregion[p]

def neighbourPixel(pos, height, width, pixelinregion, pixelUsed ): # retourne la liste des pixels voisins d'un pixel qui n'appartiennent pas à sa région
    listNeighbour = []
    i = pos//width
    j = pos%width
    
    if i-1 >= 0 and (pixelUsed[(i-1)*width +j] == 0)   and findRegion((i-1)*width +j,  pixelinregion) != findRegion(pos,  pixelinregion):
            listNeighbour.append((i-1)*width +j)
           
    if i+1 < height  and (pixelUsed[(i+1)*width +j] == 0)  and findRegion((i+1)*width +j,  pixelinregion) != findRegion(pos,  pixelinregion):
            listNeighbour.append((i+1)*width+j)
            
    if j-1 >= 0  and (pixelUsed[i*width +(j-1)] == 0)  and findRegion(i*width +(j-1),  pixelinregion) != findRegion(pos,  pixelinregion):
            listNeighbour.append(i*width+(j-1))
           
    if j+1 < width  and (pixelUsed[i*width +(j+1)] == 0)  and findRegion(i*width +(j+1),  pixelinregion) != findRegion(pos,  pixelinregion):
            listNeighbour.append(i*width+(j+1))
           
 
    return listNeighbour

  
def addPixelsInRegion(region1, region2, list_region, pixelinregion): # ajoute les pixels de la région2 dans la région1
    for p in range(len(pixelinregion)):
        if pixelinregion[p] == region2[0]:
                pixelinregion[p] = region1[0]
    region1[1] += region2[1]
    region1[2] += region2[2]
    
    return region1

def getRegion(idRegion, list_region):  # retourne la région
    region = []
    for r in list_region:
        if r[0] == idRegion:
            region = r
    return region

def createRegion(img_depth, list_region, pixelinregion, pixelUsed, distance): # fusionne les régions
  height = img_depth.shape[0]
  width = img_depth.shape[1]
  list_region = []
  index =0
  list_pixel = []
  list_pixel.append(0) # premier pixel de l'image
  list_region.append([0,(int) (img_depth[0] [0]), 1 ]) # première région
  pixelinregion[0] = 0
  while len(list_pixel) > 0:
    pos = list_pixel.pop(0) # le premier de la  liste
    item = getRegion(pixelinregion[pos],list_region)
    idregion = item[0]
    somme = item[1]
    nb = item[2]
    moy = somme * 1.0 /nb
    listNeighbour = neighbourPixel(pos, height, width, pixelinregion, pixelUsed)
   
    if len(listNeighbour)>0:
        for posNeighbourPixel in listNeighbour:
                i = posNeighbourPixel//width
                j = posNeighbourPixel%width
                regionIndex = findRegion(posNeighbourPixel,  pixelinregion)
                if regionIndex == -1: # cas d'un pixel seul
                    somme2 = (int)( img_depth[i] [j])
                    nb2 = 1
                    moy2 = somme2 * 1.0 /nb2
                    if abs(moy-moy2) <= distance: # on ajoute le pixel dans la région
                        pixelinregion[posNeighbourPixel] = idregion
                        item[1] += somme2
                        item[2] += nb2
                        list_pixel.append(posNeighbourPixel) # on ajoute le pixel dans la liste
                    else: # on crée une région pour ce pixel
                        index += 1
                        list_region.append([index,(int) (img_depth[i] [j]), 1 ])
                        list_pixel.append(posNeighbourPixel)
                        pixelinregion[posNeighbourPixel] = index
                else: # cas d'un pixel appartenant à une région
                    for region in list_region:
                        if region[0] == regionIndex:
                            somme2 = region[1]
                            nb2 = region[2]
                            moy2 = somme2 * 1.0 /nb2
                            if abs(moy-moy2) <= distance: # on ajoute tous les pixels de la région dans la région
                                x  =  addPixelsInRegion(item, region, list_region, pixelinregion)
                                item[1] = x[1]
                                item[2] = x[2]
                                list_region.remove(region)
    
    pixelUsed[pos] =1
    
  return list_region, pixelinregion
  
def selectRegion(list_region, nbRegion):
     list_region.sort( key=lambda region: region[2], reverse=True)
     list_region_chosen = []
     for i in range(nbRegion):
            list_region_chosen.append(list_region[i])
     return list_region_chosen

def regionToDisplay(img_depth, list_region, pixelinregion, nbRegion):
    height = img_depth.shape[0]
    width = img_depth.shape[1]
    list_region_chosen = selectRegion(list_region, nbRegion)
    img_region = np.zeros((height,width,3), np.uint8)
    
    for i in range(height):
        for j in range(width):
            img_region[i] [j] = 0
    for r in list_region_chosen:
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255) )
        for i in range(height):
            for j in range(width):
                if pixelinregion[i*width+j] == r[0]:
                    img_region[i] [j] = color
    return img_region
    
def cleanRegion(list_region, seuil): # supprimer les régions trop petites
    list_temp = []
    list_index_region = []
    for i in range(len(list_region)):
        if list_region[i][2] > seuil:
              list_temp.append(list_region[i])
              list_index_region.append(list_region[i][0])
    return list_temp, list_index_region

def saveRegion(list_region, pixelinregion, filename):
    np.save( filename + "_pixelinregion" + ".npy", pixelinregion)
    with open(filename +"_list_region", 'wb') as temp_file:
        pickle.dump(list_region, temp_file)
    return

def loadRegion(filenamepixel, filenamelistr):
    pixelinregion = np.load(filenamepixel)
    with open(filenamelistr, 'rb') as temp_file:
        list_region = pickle.load( temp_file)
    return pixelinregion, list_region
    
def mergeRegion(img_depth, filenamepixel, filenamelistr): # fusionner des régions
    height = img_depth.shape[0]
    width = img_depth.shape[1]
    pixelinregion, list_region = loadRegion(filenamepixel, filenamelistr)
    list_region, list_index_region = cleanRegion(list_region, 4)
    #print("après cleanRegion len(list_region) = ", len(list_region))
    tabRegion = tabCorespRListregion(height, width, pixelinregion, list_region)
    #print("len(tabRegion) = ", len(tabRegion), " tabRegion = ", tabRegion)
    list_adj =  list_adjacence(height, width, pixelinregion, tabRegion, list_region, list_index_region)
    #print("len(list_region) = ", len(list_region))
    #print("list_region = ", list_region)
    #print("len(list_adj) = ", len(list_adj))
    #print("list_adj = ", list_adj)
    moy = 0
    #for idxregion in range(len(list_region)):
    #    moy = 1.0 * list_region[idxregion][1] / list_region[idxregion][2]
    #    print("index " , idxregion, " moyenne region ", list_region[idxregion], " = ", moy)
        #print("list_adj[idxregion][1] = ", list_adj[idxregion][1])
    #    for adj in list_adj[idxregion][1]:
    #        moyAdj = list_region[int(tabRegion[adj])][1] / list_region[int(tabRegion[adj])][2]
    #        print("adj = ", adj, "moy = ", moyAdj)
    #        if abs(moy-moyAdj)< 20:
    #            print("fusion ", list_region[idxregion][0] , " ", adj)
             
        
    return list_region

def neighbourPixelRegion(pos, height, width, pixelinregion, list_index_region): # retourne la liste des régions voisines d'un pixel
    listNeighbour = []
    i = pos//width
    j = pos%width
    
    if i-1 >= 0  and findRegion((i-1)*width +j,  pixelinregion) != findRegion(pos,  pixelinregion) and findRegion((i-1)*width +j,  pixelinregion) in list_index_region:
            listNeighbour.append(int(findRegion((i-1)*width +j,  pixelinregion)))
           
    if i+1 < height  and findRegion((i+1)*width +j,  pixelinregion) != findRegion(pos,  pixelinregion) and findRegion((i+1)*width +j,  pixelinregion) in list_index_region:
            idRegion = findRegion((i+1)*width+j,  pixelinregion)
            if idRegion not in listNeighbour:
                listNeighbour.append(int(idRegion))
            
    if j-1 >= 0  and findRegion(i*width +(j-1),  pixelinregion) != findRegion(pos,  pixelinregion) and findRegion(i*width +(j-1),  pixelinregion) in list_index_region:
            idRegion = findRegion(i*width+(j-1),  pixelinregion)
            if idRegion not in listNeighbour:
                listNeighbour.append(int(idRegion))
           
    if j+1 < width  and findRegion(i*width +(j+1),  pixelinregion) != findRegion(pos,  pixelinregion) and findRegion(i*width +(j+1),  pixelinregion) in list_index_region:
            idRegion = findRegion(i*width+(j+1),  pixelinregion)
            if idRegion not in listNeighbour:
                listNeighbour.append(int(idRegion))
    
    return listNeighbour

def tabCorespRListregion(height, width, pixelinregion, list_region): # 
    max = 0
    for pos in range(len(pixelinregion)):
        if pixelinregion[pos] > max:
            max = pixelinregion[pos]
    #print("max = ",max+1)
    #tabRegion = np.full(int(max)+1, -1)
    tabRegion = np.zeros(int(max)+1)
    for i in range(int(max)+1):
         tabRegion[i] = (int) (-1)
    for i in range(len(list_region)):
        tabRegion[int(list_region[i][0])] =  i
    return tabRegion

def list_adjacence(height, width, pixelinregion, tabRegion, list_region, list_index_region): # retourne la liste d'adajacence du graphe des régions
    list_adj = []
    for i in range(len(list_region)):
        list_adj.append([list_region[i][0], []])
    for pos in range(height * width):
        listNeighbour = neighbourPixelRegion(pos, height, width, pixelinregion, list_index_region)
        if len(listNeighbour)>0:
            for l in listNeighbour:
                list_neighbour = list_adj[int(tabRegion[int(pixelinregion[pos])])] [1]
                if l not in list_neighbour:
                    list_neighbour.append(int(l))
    return list_adj

def segmentation(image_name, distance):
    if not os.path.exists(image_name) or not os.path.isfile(image_name):
        print("This image does not exist!")
        return
    new_image = cv2.imread(image_name, cv2.IMREAD_GRAYSCALE)
    name = image_name.split('.')
    image_name = name[0]    
    filename = image_name + "_" + str(distance)
    if  os.path.exists(filename + "_pixelinregion" + ".npy") and  os.path.exists(filename +"_list_region" ) and os.path.isfile(filename + "_pixelinregion" + ".npy") and os.path.isfile(filename +"_list_region"):
        pixelinregion, list_region = loadRegion( filename + "_pixelinregion" + ".npy", filename +"_list_region" )
    else:
        print("début segmentation")
        debut = time.time()
        pixelinregion, list_region, pixelUsed =initializeRegion(new_image)
        list_region , pixelinregion = createRegion(new_image, list_region, pixelinregion, pixelUsed, distance)   
        print("fin segmentation")
        saveRegion(list_region, pixelinregion, filename)  
        fin = time.time()
        print("durée segmentation = ", fin-debut)
        
    debut = time.time()
    list_region = mergeRegion(new_image, filename + "_pixelinregion" + ".npy", filename +"_list_region" )
    fin = time.time()
    print("durée merge = ", fin-debut)
    nbRegion = len(list_region)
    print("nombre de régions", nbRegion)
    debut = time.time()
    img_region = regionToDisplay(new_image, list_region, pixelinregion, nbRegion)
    filename = filename  + "_segmentation_region_" +str(nbRegion)  + ".png"
    cv2.imwrite(filename, img_region)
    fin = time.time()
    print("durée display write = ", fin-debut)
    return
