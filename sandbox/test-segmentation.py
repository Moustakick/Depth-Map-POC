import cv2
import numpy as np


img=cv2.imread("totoro.png")
img_depth = cv2.imread("totoro_depth.png", cv2.IMREAD_GRAYSCALE)
 

 

#cv2.imshow("image",img)
#cv2.imshow("image depth",img_depth)
 
print("taille img", img.shape)
print("taille img depth", img_depth.shape)
print("taille img depth hauteur", img_depth.shape[0])

new_image = cv2.resize(img_depth, (img.shape[1], img.shape[0])) 

filename = "depth_resize.png" 
cv2.imwrite(filename, new_image)
print("taille depth resize ", new_image.shape)
cv2.imshow("depth resize",new_image)

canny_img = cv2.Canny(img, 100, 200)
filename = "canny_img.png"
cv2.imwrite(filename, canny_img)
cv2.imshow("canny img", canny_img)

canny_depth = cv2.Canny(new_image, 10, 90)
filename = "canny_depth.png"
cv2.imwrite(filename, canny_depth)
cv2.imshow("canny depth", canny_depth)



cv2.waitKey(0)
cv2.destroyAllWindows()
