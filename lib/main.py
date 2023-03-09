import argparse
import utils, ponctual_processing, local_processing, global_processing, segmentation, mesh

def main():
    parser = argparse.ArgumentParser(description='Process two files')
    # main args
    parser.add_argument('--image', default=None, type=str, help='path to image file')
    parser.add_argument('--depthmap', default=None, type=str, help='path to depthmap file')
    parser.add_argument('--test', default=None, type=str, help='path to image file assuming that depthmap path is equal and ended with \'_depth\'')
    # function args
    parser.add_argument('--threshold', default=0.5, type=float, help='threshold of the depthmap')

    args = parser.parse_args()

    # load the image and depthmap file
    image_file = args.image
    depthmap_file = args.depthmap
    if args.test is not None:
        image_file = args.test
        index = image_file.rfind('.')
        depthmap_file, extension = image_file[:index], image_file[index:]
        depthmap_file += '_depth' + extension
    print(image_file, depthmap_file)
    image, depthmap = utils.load_image(image_file, depthmap_file)

    print(image.shape, depthmap.shape)

    thrshld = args.threshold

    # process
    # result = ponctual.threshold(image, depthmap, thrshld, True)
    # result = ponctual.fog(image, depthmap, 4, [.2, .2, .2])
    # result = local.blur(image, 17, 17)
    # result = local.depth_of_field(image, depthmap, 0.11, 0.15)
    result = global_processing.graylvl_quantization(depthmap, 8)
    # result = segmentation.gradient(image, depthmap)

    # save 
    utils.save_image(result, 'result')
    # mesh.save_as_obj(image, depthmap)

if __name__ == "__main__":
    main()
