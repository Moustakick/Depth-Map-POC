import numpy as np
import cv2

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
