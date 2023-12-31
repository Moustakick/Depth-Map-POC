import numpy as np
import cv2
from skimage import filters

import utils

def graylvl_quantization(image, k):
    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.1)
    img = image.reshape((-1,3))
    img = np.float32(img*255)
    ret, label, center = cv2.kmeans(img, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    image = res.reshape((image.shape))

    return image

def watershade(image, depthmap, thresh) :
    # Marker labelling
    thresh = np.uint8(thresh)
    ret, markers = cv2.connectedComponents(thresh)
    image = np.uint8(image*255)
    depth = np.uint8(depthmap*255)
    depth = cv2.cvtColor(depth, cv2.COLOR_GRAY2BGR)
    markers = cv2.watershed(depth, markers)
    image[markers == -1] = [0,0,255]
    return image

def edges(image) :
    img = np.uint8(image*255)
    edges = cv2.Canny(img, 20, 100)
    return edges

def extract_per_lvl(gray):
    height, width = gray.shape
    #utils.interval(gray, 0, 255)

    result = np.zeros(gray.shape)
    kernel = np.ones((29,29), np.uint8)

    for x in np.unique(gray):
        tmp = np.zeros(gray.shape)

        for i in range(height):
            for j in range(width):
                tmp[i,j] = 255 if gray[i,j]==x else 0
        tmp = cv2.erode(tmp, kernel, iterations=1)

        for i in range(height):
            for j in range(width):
                result[i,j] = tmp[i,j] if gray[i,j]==x else result[i,j]

    return result
