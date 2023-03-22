import numpy as np
import cv2
from scipy import signal

import utils, mask_exctraction

def depth_of_field(image, depthmap, center, radius, extent, kernel_length=7, debug=False):
    """Apply the depth of field effect
    
    Args:
        image (numpy array): the image
        depthmap (numpy array): the depthmap
        center: focal plane center
        radius: radius of the focal plane
        extent: length of both slopes of the transitions
                between inside and outside of the focal plane
        kernel_length: length of gaussian kernel

    Returns:
        numpy array: result
    """

    height, width, channels = image.shape

    # extract masks
    near_field_mask, far_field_mask = mask_exctraction.ponctual_masks_exctration(image, depthmap, center, radius, extent)

    # make fields
    near_field = cv2.GaussianBlur(image, (kernel_length, kernel_length), 0)
    far_field = mask_blur(image, far_field_mask, 9) # TODO: too slow
    far_field = utils.interval(far_field, np.min(image), np.max(image))

    # interpolate fields with image
    result = np.zeros((height, width, channels))
    for i in range(height):
        for j in range(width):
            result[i,j] = utils.lerp(image[i,j], far_field[i,j], far_field_mask[i,j])
            result[i,j] = utils.lerp(result[i,j], near_field[i,j], near_field_mask[i,j])

    # debug mode 
    if debug:
        utils.save_image(near_field_mask, 'near_mask')
        utils.save_image(far_field_mask, 'far_mask')
        utils.save_image(near_field, 'near_field')
        utils.save_image(far_field, 'far_field')

    return result

def mask_blur(image, mask, kernel_lenght):
    """Blur the image taking acount the mask

    Args:
        image (numpy array): the image
        mask (numpy array): the mask
        kernel_length: length of the kernel

    Returns:
        numpy array: the blured image
    """

    def gaussian_kernel(length=9, std=3):
        """Returns a 2D Gaussian kernel array."""
        gaussian_kernel_1D = signal.gaussian(length, std=std).reshape(length, 1)
        gaussian_kernel_2D = np.outer(gaussian_kernel_1D, gaussian_kernel_1D)
        return gaussian_kernel_2D
    
    def apply_kernel(image, kernel, I, J):
        """Apply a kernel to an image at a pixel (I,J)"""
        height, width, channels = image.shape
        kernel_height, kernel_width = kernel.shape
        kernel_height_radius, kernel_width_radius = int(kernel_height/2), int(kernel_width/2)

        sum = np.sum(kernel)
        value = np.array([0,0,0])
        for i in range(-kernel_height_radius, kernel_height_radius, 1):
            for j in range(-kernel_width_radius, kernel_width_radius, 1):
                # mirror the image if kernel on the edge
                x, y = I+i, J+j
                if x<0:
                    x = I-i
                elif x>=height:
                    x = (height-1) - (x-height) 
                if y<0:
                    y = J-j
                elif y>=width:
                    y = (width-1) - (y-width) 
                # add value
                value = value + (kernel[i,j] * np.array(image[x,y]))

        return value/sum

    kernel = gaussian_kernel(kernel_lenght)

    # apply mask for each pixel
    height, width, channels = image.shape
    result = np.zeros((height, width, channels))
    for i in range(height):
        for j in range(width):
            if mask[i,j] != 0:
                result[i,j] = apply_kernel(image, kernel, i, j)
    
    return result

# TODO : use mask instead of just depth !!!
def threshold(image, depthmap, thrshld:float, keep_near=True):
    """Threshold the image by depthmap values

    Args:
        image (array): the image numpy array
        depthmap (array): the depthmap numpy array
        threshold (int): the threshold of the depthmap
        keep_near (bool): keep closest pixel if true, further else.

    Returns:
        result: the numpy array of the image thresholded by depthmap values
    """

    height, width, channels = image.shape
    result = np.zeros((height, width, channels))

    # For each pixel of the image
    for i in range(height):
        for j in range(width):
            # Keep pixel wich are closest than threshold 
            if keep_near :
                if depthmap[i,j] < thrshld:
                    result[i,j] = image[i,j]
            # Keep pixel wich are further than threshold 
            else : 
                if depthmap[i,j] > thrshld:
                    result[i,j] = image[i,j]

    return result

# TODO : enhanced with noise !!!
def fog(image, depthmap, density=1, fog_color=[.5, .5, .5]):
    """Add a fog effect to the image

    Args:
        image (array): the image numpy array
        depthmap (array): the depthmap numpy array
        density (float): density of the fog
        fog_color (array): color of the fog

    Returns:
        result: the numpy array of the image with a fog effect
    """

    def linear_fog(depth):
        return 1-depth

    def exponential_fog(depth, density):
        return 2**(-depth*density)
    
    def exponential_squared_fog(depth, density):
        return 2**(-((depth*density)**2))

    height, width, channels = image.shape
    result = np.zeros((height, width, channels))

    # For each pixel of the image
    for i in range(height):
        for j in range(width):
            depth = depthmap[i,j]
            fog_factor = exponential_squared_fog(depth, density)
            result[i,j] = utils.lerp(fog_color, image[i,j], fog_factor)

    return result