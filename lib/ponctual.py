import numpy as np

def threshold(image, depthmap, thrshld:float, keep_near=True):
    """Generate a new image with the depthmap filter

    Args:
        image (array): the image numpy array
        depthmap (array): the depthmap numpy array
        threshold (int): the threshold of the depthmap
        keep_near (bool): keep closest pixel if true, further else.

    Returns:
        result: the numpy array of the image filtered by the depthmap with the threshold
    """

    width = image.shape[0]
    height = image.shape[1]
    channels = image.shape[2] 
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
