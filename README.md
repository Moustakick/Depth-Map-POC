# PDP

## Liens utiles

+ Dataset NyuV2 : https://cs.nyu.edu/~silberman/datasets/nyu_depth_v2.html
+ Dense-Depth : https://github.com/ialhashim/DenseDepth

## Utilisation 

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

Uses : 
In `depthmap_generator/`, download and put a pretrained model in `pretrained/`. You can refer to [NYU Depth V2 model](https://drive.google.com/file/d/19dfvGvDfCRYaqxVKypp1fRHwK7XtSjVu/view?usp=sharing), as we have tested it only with this model. If you want to use another model you can specify the `--model` argument. 

Put images on `image/` directory, if you want to use another file path you can specify the `--input` argument. 
Also, by default images will be resized in 640 by 480 (portrait or landscape is not a problem) because the model was trained on Nyu dataset, if you use another model you can specify the size with `--size` arguments.

Now you can launch `python3 generator.py` to generate your depthmaps. 

## Results 
average gradient magnitude :
| image |   phone   | depth of field |  camera   |
| :---: | :-------: | :------------: | :-------: |
|   A   | 314.6138  |   257.33444    | 289.23038 |
|   B   | 385.4227  |   326.61282    | 300.93024 |
|   C   | 732.67267 |    544.1622    | 471.18332 |
|   D   | 471.71713 |   403.48346    | 331.62378 |
|   E   | 808.42645 |   673.27545    | 741.3863  |
|   F   | 422.29962 |   367.93134    | 367.5415  |
|   G   | 511.32843 |   472.36356    | 438.90668 |
|   H   | 381.76453 |    341.2969    | 410.11426 |
|   I   | 439.85834 |    371.7265    | 319.0388  |

signal to noise ratio :
| image |  camera over dof   |   phone over dof   |
| :---: | :----------------: | :----------------: |
|   A   | 12.55774448623647  | 30.070308978738254 |
|   B   | 6.152245505458897  | 27.844132373559603 |
|   C   | 7.576697013393142  | 22.25194545793279  |
|   D   | 6.795075205016559  | 24.298807320600314 |
|   E   | 4.136950483631999  | 20.868539098829594 |
|   F   | 6.806565321478035  | 24.94589600703457  |
|   G   | 6.7864023571003775 | 31.13982147494808  |
|   H   | 5.5145634559853125 | 20.228565544478705 |
|   I   | 5.077237682592167  | 23.71055456712089  |

phone/camera parameters :
| image | center | radius | extent |
| :---: | :----: | :----: | :----: |
|   A   |  0.4   |  0.2   |  0.2   |
|   B   |  0.25  |  0.15  |  0.1   |
|   C   |  0.15  |  0.05  |  0.1   |
|   D   |  0.1   |  0.08  |  0.1   |
|   E   |  0.2   |  0.1   |  0.05  |
|   F   |  0.4   |  0.05  |  0.1   |
|   G   |  0.15  |  0.05  |  0.1   |
|   H   |  0.3   |  0.15  |  0.08  |
|   I   |  0.32  |  0.08  |  0.05  |

## Opencv use
import cv2

**load RGB Image**

img=cv2.imread("totoro.png")

**load gray Image**

img_depth = cv2.imread("totoro_depth.png",cv2.IMREAD_GRAYSCALE)

**get Image's shape**

img.shape

(height, width)

**show image**

cv2.imshow("image",img)

**save image**

filename = "resultat.png"

cv2.imwrite(filename, img_depth)

**split RGB image's channels**

B, G, R = cv2.split(img)

cv2.imshow("blue", B)

**overlaid 2 images**

cv2.addWeighted(img1, wt1, img2, wt2, gammaValue)

wt1 : image1's weigth
wt2 : image2's weigth
gammaValue : light's measure, example 0

**resize image**

new_image = cv2.resize(img_depth, (width,height))

**Canny edge detection**

canny = cv2.Canny(new_image, minval, maxval)

https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html








