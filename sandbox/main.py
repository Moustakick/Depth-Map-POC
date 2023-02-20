import argparse
from PIL import Image

def main():
    parser = argparse.ArgumentParser(description='Process two files')
    parser.add_argument('image', type=str, help='normal png file')
    parser.add_argument('depthmap', type=str, help='depthmap of the file')
    parser.add_argument('threshold', type=int, help='threshold of the depthmap')

    args = parser.parse_args()

    # Open and read the image file
    with open(args.image, 'rb') as image_file:
        # image = image_file.read()
        image = Image.open(image_file.name)
        
    # Open and read the depthmap file
    with open(args.depthmap, 'rb') as depthmap_file:
        # depthmap = depthmap_file.read()
        depthmap = Image.open(depthmap_file.name)

    threshold = args.threshold

    # Load the pixel matrix of the image and the depthmap
    tab_image = image.load()
    tab_depthmap = depthmap.load()

    # Create a new image with pilow
    new_image = Image.new('RGB', (image.size[0], image.size[1]), (0, 0, 0))

    # For each pixel of the image, we check if the pixel of the depthmap is black
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            # If the pixel is further than the threshold, we put the pixel of the image in the new image
            if tab_depthmap[x,y] < threshold:
                new_image.putpixel((x,y), tab_image[x,y])

    # Save the new image
    new_image.save('new_image.png')
            



if __name__ == "__main__":
    main()