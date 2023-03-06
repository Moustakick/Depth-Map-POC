import numpy as np
import cv2

import utils

def watershade(image, depthmap) :

    #utils.interval(depthmap, 0, 255)
    gradient = cv2.Laplacian(depthmap, cv2.CV_64F)
    gradient = abs(gradient)
    gradient = np.uint16(np.round(gradient*255))
    ret, thresh = cv2.threshold(gradient, 0, 255, cv2.THRESH_OTSU)
    kernel = np.ones((2,2), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    
    return opening
