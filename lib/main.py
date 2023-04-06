import argparse
import utils, depth_processing, mask_exctraction, mesh, quality_measures

def main():
    parser = argparse.ArgumentParser(description='Process two files')
    # main args
    parser.add_argument('--image', default=None, type=str, help='path to image file')
    parser.add_argument('--image2', default=None, type=str, help='path to image file')
    parser.add_argument('--depthmap', default=None, type=str, help='path to depthmap file')
    parser.add_argument('--test', default=None, type=str, help='path to image file assuming that depthmap path is equal and ended with \'_depth\'')

    args = parser.parse_args()

    # load the image and depthmap file
    image_file = args.image
    image_file2 = args.image2
    depthmap_file = args.depthmap
    if args.test is not None:
        image_file = args.test
        index = image_file.rfind('.')
        depthmap_file, extension = image_file[:index], image_file[index:]
        depthmap_file += '_depth' + extension
    print(image_file, depthmap_file)
    if depthmap_file is not None:
        image, depthmap = utils.load_image_with_depthmap(image_file, depthmap_file)
    else: 
        if image_file is not None:
            image = utils.load_image(image_file)
        if image_file is not None:
            image2 = utils.load_image(image_file2)

    ''' process exemples '''
    # apply fog
#    result = depth_processing.fog(image, depthmap, 5, [.4, .4, .4])
    # extract masks
#    masks = mask_exctraction.ponctual_masks_exctration(image, depthmap, 0.1, 0.2, 0.1)
    # use masks for depth_of_field (portrait) effect
#    result = depth_processing.depth_of_field(image, masks, 13)
    # use masks for lightness correction
#    result = depth_processing.linghtness(image, masks, 0.2)

    ''' evaluation exemple '''
#    evaluation = quality_measures.average_gradient_magnitude(image)
    evaluation = quality_measures.signal_noise_ratio(image, image2)

    ''' saving results '''
    # save 
#    utils.save_image(result, 'result')
    # generate .obj file 
#    mesh.save_as_obj(image, depthmap)
    # show measure 
    print("eval:", evaluation)

if __name__ == "__main__":
    main()
