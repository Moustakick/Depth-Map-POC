import numpy as np
import cv2
from PIL import Image

def load_image(image_file:str):

    # load image
    image = cv2.imread(image_file)
    # delete alpha chanel
    if image.shape[2]==4: 
        image = np.delete(image, 3, 2)
    # normalization in [0,1]
    image = np.clip(image/255, 0, 1)

    return image

def load_image_with_depthmap(image_file:str, depthmap_file:str) -> tuple:
    """Load the image and depthmap as array

    Args:
        image_file (str): image file path
        depthmap_file (str): depthmap file path

    Returns:
        image, depthmap: the normalized numpy array of the image and the depthmap
    """

    image = load_image(image_file)

    # load depthmap
    depthmap = Image.open(depthmap_file)
    # resize as image
    depthmap = depthmap.resize((image.shape[1], image.shape[0]))
    depthmap = np.asarray(depthmap, dtype=float)
    # keep only one channel
    # in 3 channels case (rgb)
    if len(depthmap.shape) == 3 and depthmap.shape[2] == 3:
        depthmap = np.delete(depthmap, 2, 2)
        depthmap = np.delete(depthmap, 1, 2)
        depthmap = np.reshape(depthmap, (image.shape[0], image.shape[1]))
    # in 4 channels case (rgba)
    if len(depthmap.shape) == 3 and depthmap.shape[2] == 4:
        depthmap = np.delete(depthmap, 3, 2)
        depthmap = np.delete(depthmap, 2, 2)
        depthmap = np.delete(depthmap, 1, 2)
        depthmap = np.reshape(depthmap, (image.shape[0], image.shape[1]))
    # normalization in [0,1]
    depthmap = interval(depthmap, 0, 1)
    return image, depthmap

def save_image(image, name:str):
    """Save image from array as png

    Args:
        image (array): the image file
        name (str): the image name without extension
    """

    # denormalize and save
    image = interval(image, 0, 255)
    cv2.imwrite(name+'.png', image)

def interval(image, new_min, new_max):
    max = np.max(image)
    min = np.min(image)
    a = (new_max-new_min) / (max-min)
    b = new_max - a * max
    image = np.clip(a * image + b, new_min, new_max)
    return image

def lerp(x, y, factor):
    x = np.array([(1-factor) * i for i in x])
    y = np.array([factor * i for i in y])
    return x + y

def affine(x0, x1, y0, y1, x):
    if x0-x1 == 0:
        return (y0+y1)/2
    
    a = (y1-y0) / (x1-x0)
    b = y0 - a*x0
    return a*x + b
