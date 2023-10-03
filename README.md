# Image processing with depthmap

## Presentation

This repository came from the end-of-year project for my first year of a master's degree in computer science specializing in image and sound at the University of Bordeaux. We've worked in a group composed of Dubois Yanis, Lacoste Théo, Oçafrain Maxime and Riverain Olivier to develop an proof of concept application for image processing, based on the use of depth maps. The project was proposed by Pascal Desbarats, a researcher at LaBRI, who also supervised us throughout.

## Use

### Our application

Dependencies :
- OpenCV
- Pillow
- Numpy
- Scipy

Uses : </br>
In `lib/`, you can run the main file with `python3 main.py` like this : 

```
usage: main.py [-h] [--test TEST] [--arg1 ARG1] [--arg2 ARG2] [--arg3 ARG3]
               [--arg4 ARG4]
               image depthmap process

Process an image file using his depthmap.

positional arguments:
  image   path to image file
  depthmap
          path to depthmap file
  process
          fog, dof, light or segm :
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

optional arguments:
  -h, --help
          show this help message and exit
  --test TEST
          path to image file assuming that depthmap path is equal and ended with '_depth'
  --arg1 ARG1
          first argument of the process function, see process argument
  --arg2 ARG2
          second argument of the process function, see process argument
  --arg3 ARG3
          third argument of the process function, see process argument
  --arg4 ARG4
          fourth argument of the process function, see process argument
```

### Depthmap generator

This part came from [DenseDepth](https://github.com/ialhashim/DenseDepth). 

Dependencies :
- OpenCV
- Pillow
- Numpy
- Scipy
- Matplotlib
- Keras
- Tensorflow

Uses : </br>
In `depthmap_generator/`, download and put a pretrained model in `pretrained/`. You can refer to [NYU Depth V2 model](https://drive.google.com/file/d/19dfvGvDfCRYaqxVKypp1fRHwK7XtSjVu/view?usp=sharing), as we have tested it only with this model. If you want to use another model you can specify the `--model` argument. 

Put images on `image/` directory, if you want to use another file path you can specify the `--input` argument. 
Also, by default images will be resized in 640 by 480 (portrait or landscape is not a problem) because the model was trained on Nyu dataset, if you use another model you can specify the size with `--size` arguments.

Now you can launch `python3 generator.py` to generate your depthmaps. 
