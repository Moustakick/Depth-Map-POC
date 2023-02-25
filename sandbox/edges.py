import argparse
from PIL import Image,ImageFilter

def main():
    parser = argparse.ArgumentParser(description='Process two files')
    parser.add_argument('image', type=str, help='normal png file')
    parser.add_argument('depthmap', type=str, help='depthmap of the file')
    parser.add_argument('threshold', type=int, help='threshold of the depthmap')

    args = parser.parse_args()
    threshold = args.threshold


    with open(args.depthmap, 'rb') as depthmap_file:
        # depthmap = depthmap_file.read()
        depthmap = Image.open(depthmap_file.name)
        # Convert the image to grayscale
        depthmap = depthmap.convert('L')
        # Apply a filter to enhance the edges
        edges = depthmap.filter(ImageFilter.FIND_EDGES)
        # Threshold the image to keep only the strong edges
        # edges = edges.point(lambda x: 255 if x > threshold else 0)
        # save the resulting image
        edges.save("test_contours_depth.png")

    with open(args.image, 'rb') as image_file:
        # image = image_file.read()
        image = Image.open(image_file.name)

        image = image.convert('L')
        # Apply a filter to enhance the edges
        edges = image.filter(ImageFilter.FIND_EDGES)
        # Threshold the image to keep only the strong edges
        edges = edges.point(lambda x: 255 if x > threshold else 0)
        # save the resulting image
        edges.save("test_contours.png")


if __name__ == "__main__":
    main()