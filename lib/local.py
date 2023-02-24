import numpy as np

def depth_of_field():
    return None

def kernel_result(i, j, image):
    # kernel = [[1, 2, 1], [2, 4, 2], [1, 2, 1]]
    kernel = [[1, 4,  7,  4,  1], 
              [4, 16, 26, 16, 4], 
              [7, 26, 41, 26, 7], 
              [4, 16, 26, 16, 4], 
              [1, 4,  7,  4,  1]]
    result = 0
    width = image.shape[0]
    heigth = image.shape[1]
    for x in range(-2, 3):
        for y in range(-2, 3):
            if i+x >= 0 and i+x < width and j+y >= 0 and j+y < heigth:
                result += image[i+x, j+y] * kernel[x+1][y+1]
            else :
                result += 0
    return result/273

def blur(image, depthmap, threshold):
    """Blur the image with the depthmap

    Args:
        image (numpy array): the image
        depthmap (numpy array): the depthmap of the image
        threshold (float): the threshochannelsld of the depthmap

    Returns:
        numpy array: the new image
    """
    # create a mask
    mask = np.zeros(depthmap.shape)
    mask[depthmap>threshold] = 1
    # blur the image
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if mask[i,j] == 1:
                image[i,j] = kernel_result(i, j, image)
    return image
