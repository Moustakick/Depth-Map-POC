import numpy as np
import cv2

import utils

def watershade(image, depthmap, thresh) :
    # Marker labelling
    ret, markers = cv2.connectedComponents(thresh)
    image = np.uint8(image*255)
    depth = np.uint8(depthmap*255)
    depth = cv2.cvtColor(depth, cv2.COLOR_GRAY2BGR)
    markers = cv2.watershed(depth, markers)
    image[markers == -1] = [0,0,255]
    return image

def gradient(image, depthmap) :
    depth = np.uint8(depthmap*255)
    edges = cv2.Canny(depth, 20, 100)

    kernel = np.ones((3,3),np.uint8)
    close = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=1)

    #return close
    return watershade(image, depthmap, close)
