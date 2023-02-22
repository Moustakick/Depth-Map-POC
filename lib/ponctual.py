import numpy as np

def _threshold(image, depthmap, threshold):
    """Generate a new image with the depthmap filter

    Args:
        image (nparray): the image numpy array
        depthmap (nparray): the depthmap numpy array
        threshold (int): the threshold of the depthmap

    Returns:
        result: the numpy array of the image filtered by the depthmap with the threshold
    """
    width = image.shape[0]
    height = image.shape[1]
    channels = image.shape[2] 
    result = np.zeros((width, height, channels))
    # For each pixel of the image, we check if the pixel of the depthmap is black
    for x in range(width):
        for y in range(height):
            # If the pixel is further than the threshold, we put the pixel of the image in the new image
            if depthmap[x,y] < threshold:
                result[x,y] = image[x,y]

    return result
