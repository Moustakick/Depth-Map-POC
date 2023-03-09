import numpy as np
import utils

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
            interpolation = utils.lerp(image[i,j], fog_color, fog_factor)
            result[i,j] = interpolation

    return result
