import cv2
import numpy as np
import random as rng

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
#cv2.imshow("image depth",img_depth)import random as rngimport random as rng
 
print("taille img", img.shape)
print("taille img depth", img_depth.shape)
print("taille img depth hauteur", img_depth.shape[0])

new_image = cv2.resize(img_depth, (img.shape[1], img.shape[0])) 

#filename = "depth_resize.png" 
#cv2.imwrite(filename, new_image)
#print("taille depth resize ", new_image.shape)
cv2.imshow("depth resize",new_image)

canny_img = cv2.Canny(img, 100, 200)
#filename = "canny_img.png"
#cv2.imwrite(filename, canny_img)
#cv2.imshow("canny img", canny_img)

canny_depth = cv2.Canny(new_image, 10, 90)
#filename = "canny_depth.png"
#cv2.imwrite(filename, canny_depth)
#cv2.imshow("canny depth", canny_depth)

#blur = cv2.blur(new_image, (10,10))
ret, thresh = cv2.threshold(canny_depth, 1, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
_, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img, contours, -1, (0,255,0), 3)
print("len contours", len(contours))
#or i in range(len(contours)):
  #      color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
    #    cv2.drawContours(img, contours, i, color, 2, cv2.LINE_8, hierarchy, 0)
    
cv2.imshow('Contours', img)
cv2.imshow('Thresh', thresh)

filename = "segmentation_2.png"
cv2.imwrite(filename, img)

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

cv2.waitKey(0)
cv2.destroyAllWindows()
