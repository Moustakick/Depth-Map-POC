import numpy as np

import utils

def ponctual_masks_exctration(image, depthmap, center, radius, extent):
    """Extract the near and far field masks 
    
    Args:
        image (numpy array): the image
        depthmap (numpy array): the depthmap
        center: focal plane center
        radius: radius of the focal plane
        extent: length of both slopes of the transitions
                between inside and outside of the focal plane

    Returns:
        tuple: near_field_mask, far_field_mask
    """

    def focus(center, radius, extent, depth):
        """Evaluate f(x) define by the function f looking like :

                start_left_slope          end_right_slope
                             ↓              ↓
        1   near field _______               _______ far field
                              \             / 
        0                      \___________/
                                focal plane
                            ↗        ↑        ↖ 
                end_left_slope     center    start_right_slope

        Args:
            center: focal plane center
            radius: radius of the focal plane
            extent: length of both slopes of the transitions
                    between inside and outside of the focal plane
            depth: point to evaluate (x)
        
        Returns:
            float: f(x)
        """

        end_left_slope, start_right_slope = center-radius, center+radius
        start_left_slope, end_right_slope = end_left_slope-extent, start_right_slope+extent

        # inside focal plane
        if (end_left_slope<=depth and depth<=start_right_slope):
            return 0
        # transition to near field
        if (start_left_slope<depth and depth<end_left_slope):
            return utils.affine(start_left_slope, end_left_slope, 1, 0, depth)
        # transition to far field
        if (start_right_slope<depth and depth<end_right_slope):
            return utils.affine(start_right_slope, end_right_slope, 0, 1, depth)
        # inside near or far field
        return 1
    
    height, width, channels = image.shape

    # Calcul fields mask
    near_field_mask = np.zeros((height, width))
    far_field_mask = np.zeros((height, width))
    for i in range(height):
        for j in range(width):
            value = focus(center, radius, extent, depthmap[i,j])
            # Pixel wich are in near field
            if depthmap[i,j] < center:
                near_field_mask[i,j] = value
            # Pixel wich are in far field
            else : 
                far_field_mask[i,j] = value

    return near_field_mask, far_field_mask

