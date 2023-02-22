import argparse
from PIL import Image
import numpy as np

import ponctual, local

def main():
    parser = argparse.ArgumentParser(description='Process two files')
    # main args
    parser.add_argument('--image', type=str, help='normal png file')
    parser.add_argument('--depthmap', type=str, help='depthmap of the file')
    # function args
    parser.add_argument('--threshold', default=0.5, type=float, help='threshold of the depthmap')

    args = parser.parse_args()

    # load the image and depthmap file
    image, depthmap = load_image(args.image, args.depthmap)

    print(image.shape, depthmap.shape)

    threshold = args.threshold

    # process
    # result = ponctual._threshold(image, depthmap, threshold)
    result = local._blur(image, depthmap, threshold)

    # denormalize and save the new image
    result = Image.fromarray(np.uint8(result*255))
    result.save('result.png')

def load_image(image_file, depthmap_file):
    """Load the image and depthmap file

    Args:
        image_file (any): the image file
        depthmap_file (any): depthmap of the image

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
    if len(depthmap.shape) == 3 and depthmap.shape[2] == 3:
        depthmap = np.delete(depthmap, 2, 2)
        depthmap = np.delete(depthmap, 1, 2)
        # normalization in [0,1]
        depthmap = np.clip(depthmap/255, 0, 1)
    # generalization of the normalization for one chanel
    else :
        # find the max value
        max_depth = np.max(depthmap)
        min_depth = np.min(depthmap)
        # normalization in [0,1]
        depthmap = np.clip((depthmap-min_depth)/max_depth, 0, 1)

    return image, depthmap

if __name__ == "__main__":
    main()
