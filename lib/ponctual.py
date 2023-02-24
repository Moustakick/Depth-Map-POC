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

    width, height, channels = image.shape
    result = np.zeros((width, height, channels))

    # For each pixel of the image
    for x in range(width):
        for y in range(height):
            # Keep pixel wich are closest than threshold 
            if keep_near :
                if depthmap[x,y] < thrshld:
                    result[x,y] = image[x,y]
            # Keep pixel wich are further than threshold 
            else : 
                if depthmap[x,y] > thrshld:
                    result[x,y] = image[x,y]

    return result

def fog(image, depthmap, density=1, fog_color=[.5, .5, .5]):
    """Add a fog effect to the image

    Args:
        image (array): the image numpy array
        depthmap (array): the depthmap numpy array
        threshold (int): the threshold of the depthmap

    Returns:
        result: the numpy array of the image with a fog effect
    """

    def linear_fog(depth):
        return 1-depth

    def exponential_fog(depth, density):
        return 2**(-depth*density)
    
    def exponential_squared_fog(depth, density):
        return 2**(-((depth*density)**2))

    width, height, channels = image.shape
    result = np.zeros((width, height, channels))

    # For each pixel of the image
    for x in range(width):
        for y in range(height):
            depth = depthmap[x,y]
            fog_factor = exponential_squared_fog(depth, density)
            interpolation = utils.lerp(image[x,y], fog_color, fog_factor)
            result[x,y] = interpolation

    return result
