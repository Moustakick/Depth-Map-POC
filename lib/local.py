import numpy as np
from PIL import Image, ImageFilter

import utils

def depth_of_field(image, depthmap, distance, extent):

    def focus(distance, extent, depth):
        focal_start, focal_end = distance-extent, distance+extent

        if (depth<=focal_start or focal_end<=depth):
            return 1
        if (focal_start<=depth and depth<=distance):
            return (depth/(focal_start-distance)) - (distance/(focal_start-distance))
        # if (distance<=depth and depth<=focal_end):
        return (depth/(focal_end-distance)) - (distance/(focal_end-distance))

    width, height, channels = image.shape

    # Calcul fields mask
    near_field_mask = np.zeros((width, height))
    far_field_mask = np.zeros((width, height))
    for x in range(width):
        for y in range(height):
            value = focus(distance, extent, depthmap[x,y])
            # Pixel wich are in near field
            if depthmap[x,y] < distance:
                near_field_mask[x,y] = value
            # Pixel wich are in far field
            else : 
                far_field_mask[x,y] = value

    # Apply mask to make fields
    near_field = np.zeros((width, height, channels))
    far_field = np.zeros((width, height, channels))
    for x in range(width):
        for y in range(height):
            near_field[x,y] = image[x,y]
            far_field[x,y] = far_field_mask[x,y] * np.array(image[x,y])
    
    # Blur both fields
    near_field = blur(near_field, 3)
    far_field = blur(far_field, 3)

    # Interpolate fields with image
    result = np.zeros((width, height, channels))
    for x in range(width):
        for y in range(height):
            result[x,y] = utils.lerp(far_field[x,y], image[x,y], far_field_mask[x,y])
            result[x,y] = utils.lerp(near_field[x,y], result[x,y], near_field_mask[x,y])

    return result

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

def blur(image, radius):
    """Blur the image

    Args:
        image (numpy array): the image

    Returns:
        numpy array: the new image
    """

    image = utils.from_numpy_to_pillow(image)
    image = image.filter(ImageFilter.GaussianBlur(radius))
    image = utils.from_pillow_to_numpy(image)

    return image

def blur_(image, depthmap, threshold):
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
