import cv2
import numpy as np
import random as rng
import segmentation_region
import time

def seuil(img_depth, min, max):
    height = img_depth.shape[0]
    width = img_depth.shape[1]   
    tmp = img_depth
    for i in range(height):
        for j in range(width):
            if(img_depth[i] [j] < min or img_depth[i] [j] > max):
                tmp[i] [j] = 255                
    return tmp
            
    

img=cv2.imread("totoro.png")
img_depth = cv2.imread("totoro_depth.png", cv2.IMREAD_GRAYSCALE)
 

 

#cv2.imshow("image",img)
#cv2.imshow("image depth",img_depth)
 
print("taille img", img.shape)
print("taille img depth", img_depth.shape)
print("taille img depth hauteur", img_depth.shape[0])

new_image = cv2.resize(img_depth, (img.shape[1], img.shape[0])) 

#filename = "depth_resize.png" 
#cv2.imwrite(filename, new_image)
#print("taille depth resize ", new_image.shape)
#cv2.imshow("depth resize",new_image)

#canny_img = cv2.Canny(img, 100, 200)
#filename = "canny_img.png"
#cv2.imwrite(filename, canny_img)
#cv2.imshow("canny img", canny_img)

#canny_depth = cv2.Canny(new_image, 10, 90)
#filename = "canny_depth.png"
#cv2.imwrite(filename, canny_depth)
#cv2.imshow("canny depth", canny_depth)

#blur = cv2.blur(new_image, (10,10))
#ret, thresh = cv2.threshold(canny_depth, 1, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#_, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#cv2.drawContours(img, contours, -1, (0,255,0), 3)
#print("len contours", len(contours))
#or i in range(len(contours)):
  #      color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
    #    cv2.drawContours(img, contours, i, color, 2, cv2.LINE_8, hierarchy, 0)
    
#cv2.imshow('Contours', img)
#cv2.imshow('Thresh', thresh)

#filename = "segmentation_2.png"
#cv2.imwrite(filename, img)

#new = seuil(new_image, 10, 50)

#ret, thresh1 = cv2.threshold(new, 50, 255, cv2.THRESH_BINARY)
#cv2.imshow("thresh1", thresh1)

#thresh2 = cv2.adaptiveThreshold(new, 255, cv2.ADAPTIVE_THRESH_MEAN_C,  cv2.THRESH_BINARY, 199, 5)
#cv2.imshow("thresh2", thresh2)

#thresh3 = cv2.adaptiveThreshold(new, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,  cv2.THRESH_BINARY, 199, 5)
#cv2.imshow("thresh3", thresh3)

#ret, thresh4 = cv2.threshold(new, 50, 255, cv2.THRESH_BINARY +  cv2.THRESH_OTSU)   
#filename = "seuil_otsu"
#cv2.imwrite(filename, thresh2)
#cv2.imshow("thresh4", thresh4)
new_image = img_depth
debut = time.time()
distance = 20 # écart entre la moyenne de deux régions
pixelinregion, list_region, pixelUsed =segmentation_region.initializeRegion(new_image)
nb_p_region = pixelinregion.size
nb_region = len(list_region)
print("nb_region = ", nb_region, " nb_p_region = ", nb_p_region)
list_region , pixelinregion = segmentation_region.createRegion(new_image, list_region, pixelinregion, pixelUsed, distance)
fin = time.time()
nb_p_region = len(list_region)
print("nb_region = ", nb_p_region)

print("durée createRegion = ", fin-debut)
#list_region =  [[0, 858, 6], [543, 1694791, 14829], [857, 77574, 433], [1016, 1554282, 10316], [1123, 343, 3], [1128, 296013, 2737], [1251, 2266482, 17104], [1281, 230027, 2375], [1356, 261028, 2521], [1481, 729225, 5657], [1516, 524, 4], [1572, 134, 1], [1579, 99, 1], [1592, 264, 2], [1625, 4352, 32], [1633, 136, 1], [1687, 250, 2], [1776, 1407280, 9465], [1799, 126, 1]]
#print(list_region)

# sauvegarde des régions
filename = "totoro_depth_" + str(distance)
print("filename = ", filename) 
segmentation_region.saveRegion(list_region, pixelinregion, filename)

# load des régions
#pixelinregion, list_region = segmentation_region. loadRegion("totoro_depth_20_pixelinregion.npy", "totoro_depth_20_list_region")
#print("nombre de régions = ", len(list_region))

debut = time.time()
nbRegion = 80
img_region = segmentation_region.regionToDisplay(img_depth, list_region, pixelinregion, nbRegion)
fin = time.time()
print("durée regionToDisplay = ", fin-debut)
filename = "totoro_depth_" 
filename = filename  + "segmentation_region_" +str(distance) + "_" + str(nbRegion) + ".png"
cv2.imwrite(filename, img_region)
cv2.imshow("segmentation", img_region)
cv2.waitKey(0)
cv2.destroyAllWindows()
