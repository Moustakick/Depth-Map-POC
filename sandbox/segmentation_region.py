import numpy as np

def initializeRegion(img_depth): # initialise les régions
    height = img_depth.shape[0]
    width = img_depth.shape[1]   
    list_region = []
    pixelinregion = np.zeros(height*width)
    cpt =0
    for i in range(height):
        for j in range(width):
            pixelinregion[i*width+j] = i*width+j
            list_region.append([i*width+j,img_depth[i] [j] ,1])        
    return pixelinregion, list_region

def neighbourPixel(i,j, height, width): # retourne la liste des pixels voisins d'un pixel
    listNeighbour = []
    if (i-1 >= 0):
            listNeighbour.append([(i-1)*width +j])
    if (i+1 < height):
            listNeighbour.append([(i+1)*width+j])
    if (j-1 >= 0):
            listNeighbour.append([i*width+(j-1)])
    if (j+1 < width):
            listNeighbour.append([i*width+(j+1)])
    return listNeighbour

def findRegion(p,  pixelinregion): # retourne la région où se trouve un pixel
        return pixelinregion[p]
           

def neighbourRegion(img_depth, idregion, list_region, pixelinregion): # trouver les régions voisines d'une région
    listNeighbour = []    
    regions =[]
    height = img_depth.shape[0]
    width = img_depth.shape[1]   
    # pour chaque pixel de la région regarder les pixels voisins
    for pos in range(len(pixelinregion)):
       if(pixelinregion[pos] == idregion):           
            i = pos//width
            j = pos%width
            listNeighbour = neighbourPixel(i,j, height, width)
    for p in listNeighbour:
        regionId = findRegion(p,  pixelinregion)
        for r in list_region:
            if r[0] == regionId:
                region = [r[0], r[1], r[2]]
        if regions.count ==0:
            regions.append(region)
        elif region not in regions:
            regions.append(region)
    return regions          
  
def addPixelInRegion(region1, region2, list_region, pixelinregion): # ajoute les pixels de la région2 dans la région1
    for p in range(len(pixelinregion)):
        if pixelinregion[p] == region2[0]:
                pixelinregion[p] == region1[0]                
                region1[1] += region2[1]
                region1[2] += region2[2]
    return region1

def mergeRegion(img_depth, list_region, pixelinregion, distance): # fusionne les régions
   region_to_see = list_region
   index =0
   while index < len(region_to_see):
            item = region_to_see[index]
            idregion = item[0]
            somme = item[1]
            nb = item[2]
            moy = somme * 1.0 /nb
            regions = neighbourRegion(img_depth, idregion, list_region, pixelinregion)
            for r in regions:                
                idregion2 = r[0]
                somme2 = r[1]
                nb2 = r[2]
                moy2 = somme2 * 1.0 /nb2
                if abs(moy-moy2) <= distance:
                    x  =  addPixelInRegion(item, r, list_region, pixelinregion)
                    list_region.remove(r)
            index +=1        
   return list_region    
