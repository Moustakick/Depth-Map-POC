import numpy as np
import cv2
from scipy import signal

import utils

def extract_masks(image, depthmap, center, radius, extent):
    """Extract the near and far field masks 
    
    Args:
        image (numpy array): the image
        depthmap (numpy array): the depthmap
        center: focal plane center
        radius: radius of the focal plane
        extent: length of both slopes of the transitions
                between inside and outside of the focal plane

    Returns:
        tuple: near_field_mask, far_field_mask
    """

    def focus(center, radius, extent, depth):
        """Evaluate f(x) define by the function f looking like :

                start_left_slope          end_right_slope
                             ↓              ↓
        1   near field _______               _______ far field
                              \             / 
        0                      \___________/
                                focal plane
                            ↗        ↑        ↖ 
                end_left_slope     center    start_right_slope

        Args:
            center: focal plane center
            radius: radius of the focal plane
            extent: length of both slopes of the transitions
                    between inside and outside of the focal plane
            depth: point to evaluate (x)
        
        Returns:
            float: f(x)
        """

        end_left_slope, start_right_slope = center-radius, center+radius
        start_left_slope, end_right_slope = end_left_slope-extent, start_right_slope+extent

        # inside focal plane
        if (end_left_slope<=depth and depth<=start_right_slope):
            return 0
        # transition to near field
        if (start_left_slope<depth and depth<end_left_slope):
            return utils.affine(start_left_slope, end_left_slope, 1, 0, depth)
        # transition to far field
        if (start_right_slope<depth and depth<end_right_slope):
            return utils.affine(start_right_slope, end_right_slope, 0, 1, depth)
        # inside near or far field
        return 1
    
    height, width, channels = image.shape

    # Calcul fields mask
    near_field_mask = np.zeros((height, width))
    far_field_mask = np.zeros((height, width))
    for i in range(height):
        for j in range(width):
            value = focus(center, radius, extent, depthmap[i,j])
            # Pixel wich are in near field
            if depthmap[i,j] < center:
                near_field_mask[i,j] = value
            # Pixel wich are in far field
            else : 
                far_field_mask[i,j] = value

    return near_field_mask, far_field_mask

def depth_of_field(image, depthmap, center, radius, extent, kernel_length=7):
    """Extract the near and far field masks 
    
    Args:
        image (numpy array): the image
        depthmap (numpy array): the depthmap
        center: focal plane center
        radius: radius of the focal plane
        extent: length of both slopes of the transitions
                between inside and outside of the focal plane
        kernel_length: length of gaussian kernel

    Returns:
        tuple: near_field_mask, far_field_mask
    """

    height, width, channels = image.shape

    # extract masks
    near_field_mask, far_field_mask = extract_masks(image, depthmap, center, radius, extent)
    #utils.save_image(near_field_mask, 'near_mask')
    #utils.save_image(far_field_mask, 'far_mask')

    # make fields
    near_field = cv2.GaussianBlur(image, (kernel_length, kernel_length), 0)
    far_field = mask_blur(image, far_field_mask, kernel_length)
    far_field = utils.interval(far_field, np.min(image), np.max(image))
    #utils.save_image(near_field, 'near_field')
    #utils.save_image(far_field, 'far_field')

    # interpolate fields with image
    result = np.zeros((height, width, channels))
    for i in range(height):
        for j in range(width):
            result[i,j] = utils.lerp(image[i,j], far_field[i,j], far_field_mask[i,j])
            result[i,j] = utils.lerp(result[i,j], near_field[i,j], near_field_mask[i,j])

    return result

def mask_blur(image, mask, kernel_lenght):
    """Blur the image

    Args:
        image (numpy array): the image

    Returns:
        numpy array: the new image
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

    height, width, channels = image.shape
    result = np.zeros((height, width, channels))
    for i in range(height):
        for j in range(width):
            if mask[i,j] != 0:
                result[i,j] = apply_kernel(image, kernel, i, j)
    
    return result
