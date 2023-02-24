from PIL import Image
import numpy as np

def load_image(image_file:str, depthmap_file:str) -> tuple:
    """Load the image and depthmap as array

    Args:
        image_file (str): image file path
        depthmap_file (str): depthmap file path

    Returns:
        image, depthmap: the normalized numpy array of the image and the depthmap
    """

    # load image
    image = Image.open(image_file)
    image = np.asarray(image, dtype=float)
    # delete alpha chanel
    if image.shape[2]==4: 
        image = np.delete(image, 3, 2)
    # normalization in [0,1]
    image = np.clip(image/255, 0, 1)

    # load depthmap
    depthmap = Image.open(depthmap_file)
    # resize as image
    depthmap = depthmap.resize((image.shape[1], image.shape[0]))
    depthmap = np.asarray(depthmap, dtype=float)
    # keep only one channel
    if len(depthmap.shape) == 3 and depthmap.shape[2] == 3:
        depthmap = np.delete(depthmap, 2, 2)
        depthmap = np.delete(depthmap, 1, 2)
    # normalization in [0,1] using min and max values
    max_depth = np.max(depthmap)
    min_depth = np.min(depthmap)
    depthmap = np.clip((depthmap-min_depth)/max_depth, 0, 1)

    return image, depthmap

def save_image(image, name:str):
    """Save image from array as png

    Args:
        image (array): the image file
        name (str): the image name without extension
    """

    # denormalize and save the new image
    result = Image.fromarray(np.uint8(image*255))
    result.save(name+'.png')
