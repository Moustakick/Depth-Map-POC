import argparse
import utils, ponctual, local

def main():
    parser = argparse.ArgumentParser(description='Process two files')
    # main args
    parser.add_argument('--image', type=str, help='normal png file')
    parser.add_argument('--depthmap', type=str, help='depthmap of the file')
    # function args
    parser.add_argument('--threshold', default=0.5, type=float, help='threshold of the depthmap')

    args = parser.parse_args()

    # load the image and depthmap file
    image, depthmap = utils.load_image(args.image, args.depthmap)

    print(image.shape, depthmap.shape)

    thrshld = args.threshold

    # process
    result = ponctual.threshold(image, depthmap, thrshld, True)
    # result = local.blur(image, depthmap, thrshld)

    # save 
    utils.save_image(result, 'result')

if __name__ == "__main__":
    main()
