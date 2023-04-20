# PDP

## Use

### Our application

Dependencies :
- OpenCV
- Pillow
- Numpy
- Scipy

Uses : </br>
In `lib/`, you can run the main file with `python3 main.py`, also this should show you the help menu. Use the `--image` and `--depthmap` arguments to specify the files of the image and depthmap you would use. With the `--process` argument you can specify which algorithm you want to apply. Some algorithm can take additional arguments, so you can use `--argi` with i from 1 to 4 to specify them. For more information about functions arguments, you can refer to the code documentation.

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
