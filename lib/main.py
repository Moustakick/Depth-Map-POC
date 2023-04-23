import argparse, sys
import utils, depth_processing, mask_exctraction, mesh, quality_measures, segmentation_region

def help():
    print('image : argument to specify an image file')
    print('depthmap : argument to specify an depthmap file')
    print('process : argument to specify a process from :')
    print('\tfog --arg1 density --arg2 fog_color_R --arg3 fog_color_G --arg3 fog_color_B')
    print('\tmask --arg1 focal_center --arg2 focal_radius --arg3 transition_extent')
    print('\tdof --arg1 focal_center --arg2 focal_radius --arg3 transition_extent --arg4 kernel_length')
    print('\tlight --arg1 focal_center --arg2 focal_radius --arg3 transition_extent --arg4 value')
    print('\tsegm')
    print('\teval')
    print('\tobj')

def main():
    less_indent_formatter = lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position=10)
    parser = argparse.ArgumentParser(formatter_class=less_indent_formatter,
        description='Process an image file using his depthmap.')
    # main args
    parser.add_argument('image', default=None, type=str, help='path to image file')
    parser.add_argument('depthmap', default=None, type=str, help='path to depthmap file')
    parser.add_argument('process',  choices=['fog', 'mask', 'dof', 'light', 'segm', 'eval', 'obj'], default=None, type=str, help='''\
fog, dof (depth of field), light or segm :
--------------------------------
fog :   --arg1 density (integer, default=1) 
        --arg2 fog_color_R (between 0 and 1, default=0.5) 
        --arg3 fog_color_G (between 0 and 1, default=0.5)
        --arg4 fog_color_B (between 0 and 1, default=0.5)
        apply fog on the image

mask :  --arg1 focal_center (between 0 and 1, default=0.5)
        --arg2 focal_radius (between 0 and 1, default=0.1)
        --arg3 transition_extent (between 0 and 1, default=0.1)
        calculate the near and far field mask

dof :   --arg1 focal_center (between 0 and 1, default=0.5)
        --arg2 focal_radius (between 0 and 1, default=0.1)
        --arg3 transition_extent (between 0 and 1, default=0.1)
        --arg4 kernel_length (integer, default=7)
        apply depth of field on the image from the mask

light : --arg1 focal_center (between 0 and 1, default=0.5)
        --arg2 focal_radius (between 0 and 1, default=0.1)
        --arg3 transition_extent (between 0 and 1, default=0.1)
        --arg4 value (between 0 and 1, default=0.5)
        apply lightness on the image from the mask

segm :  --arg1 distance (default=10)
        segment the image using the depthmap
        ''')
    parser.add_argument('--test', default=None, type=str, help='path to image file assuming that depthmap path is equal and ended with \'_depth\'')
    parser.add_argument('--arg1', default=None, type=str, help='first argument of the process function, see process argument')
    parser.add_argument('--arg2', default=None, type=str, help='second argument of the process function, see process argument')
    parser.add_argument('--arg3', default=None, type=str, help='third argument of the process function, see process argument')
    parser.add_argument('--arg4', default=None, type=str, help='fourth argument of the process function, see process argument')

    args = parser.parse_args()

    ''' load files and args '''
    image_file = args.image
    depthmap_file = args.depthmap
    if args.test is not None:
        image_file = args.test
        index = image_file.rfind('.')
        depthmap_file, extension = image_file[:index], image_file[index:]
        depthmap_file += '_depth' + extension
    if depthmap_file is not None:
        image, depthmap = utils.load_image_with_depthmap(image_file, depthmap_file)
    elif image_file is not None:
        image = utils.load_image(image_file)

    process = args.process
    arg1 = float(args.arg1) if args.arg1 is not None else None
    arg2 = float(args.arg2) if args.arg2 is not None else None
    arg3 = float(args.arg3) if args.arg3 is not None else None
    arg4 = float(args.arg4) if args.arg4 is not None else None

    result = None
    masks = None
    evaluation = None

    ''' apply process '''
    if process == 'fog':
        result = depth_processing.fog(image, depthmap, density=arg1, fog_color_R=arg2, fog_color_G=arg3, fog_color_B=arg4)
    elif process == 'mask' or process == 'dof' or process == 'light':
        masks = mask_exctraction.masks_exctration(image, depthmap, center=arg1, radius=arg2, extent=arg3)
        if process == 'dof':
            result = depth_processing.depth_of_field(image, masks, kernel_length=arg4)
        elif process == 'light':
            result = depth_processing.lightness(image, masks, value=arg4)
    elif process == 'segm':
        segmentation_region.segmentation(depthmap_file, distance=arg1)
    elif process == 'eval':
        evaluation = quality_measures.average_gradient_magnitude(image)
    elif process == 'obj':
        mesh.save_as_obj(image, depthmap)
    else:
        help()
        sys.exit()

    ''' save results '''
    if result is not None:
        utils.save_image(result, 'result')
    if masks is not None:
        utils.save_masks(masks)
    if evaluation is not None:
        print("eval:", evaluation)

if __name__ == "__main__":
    main()
