import numpy as np
import cv2

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

    height, width, channels = image.shape

    # Calcul fields mask
    near_field_mask = np.zeros((height, width))
    far_field_mask = np.zeros((height, width))
    for i in range(height):
        for j in range(width):
            value = focus(distance, extent, depthmap[i,j])
            # Pixel wich are in near field
            if depthmap[i,j] < distance:
                near_field_mask[i,j] = value
            # Pixel wich are in far field
            else : 
                far_field_mask[i,j] = value

    # Apply mask to make fields
    near_field = np.zeros((height, width, channels))
    far_field = np.zeros((height, width, channels))
    for i in range(height):
        for j in range(width):
            near_field[i,j] = image[i,j]
            far_field[i,j] = far_field_mask[i,j] * np.array(image[i,j])
    
    # Blur both fields
    near_field = blur(near_field, 9, 9)
    far_field = blur(far_field, 9, 9)

    # Interpolate fields with image
    result = np.zeros((height, width, channels))
    for i in range(height):
        for j in range(width):
            result[i,j] = utils.lerp(far_field[i,j], image[i,j], far_field_mask[i,j])
            result[i,j] = utils.lerp(near_field[i,j], result[i,j], near_field_mask[i,j])

    return result

def blur(image, kernel_width, kernel_height):
    """Blur the image

    Args:
        image (numpy array): the image

    Returns:
        numpy array: the new image
    """

    image = cv2.GaussianBlur(image, (kernel_width, kernel_height), 0)
    return image
