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
In `depthmap_generator/`, donwnload and put a pretrained model in `pretrained/`. You can refer to [NYU Depth V2 model](https://drive.google.com/file/d/19dfvGvDfCRYaqxVKypp1fRHwK7XtSjVu/view?usp=sharing), as we have tested it only with this model. If you want to use another model you can specify the `--model` argument. 

Put images on `image/` directory, if you want to use another file path you can specify the `--input` argument. 
Also, by default images will be resize in 640 by 480 (portrait or landscape is not a problem) because the model was trained on Nyu dataset, if you use other models you can specify the size with `--size` arguments.

Now you can launch `python3 generator.py` to generate your depthmaps. 

## Results 
average gradient magnitude :
| image | phone | depth of field | camera |
| :---: | :---: | :------------: | :----: |
|   A   |  315  |      257       |  289   |
|   B   |  385  |      327       |  301   |
|   C   |  733  |      544       |  471   |
|   D   |  472  |      404       |  332   |
|   E   |  808  |      673       |  741   |
|   F   |  422  |      368       |  368   |
|   G   |  511  |      472       |  439   |
|   H   |  382  |      341       |  410   |
|   I   |  440  |      372       |  319   |

B & 385 & 327 & 301 \\
C & 733 & 544 & 471 \\
D & 472 & 404 & 332 \\
E & 808 & 673 & 741 \\
F & 422 & 368 & 368 \\
G & 511 & 472 & 439 \\
H & 382 & 341 & 410 \\
I & 440 & 372 & 319 \\

image & dof over phone \\
A & 30 \\
B & 27.8 \\
C & 22.2 \\
D & 24.3 \\
E & 20.7 \\
F & 24.9 \\
G & 31.1 \\
H & 20.4 \\
I & 23.7 \\

signal to noise ratio :
| image | camera over dof | phone over dof |
| :---: | :-------------: | :------------: |
|   A   |      12.6       |      30.1      |
|   B   |       6.2       |      27.8      |
|   C   |       7.6       |      22.3      |
|   D   |       6.8       |      24.3      |
|   E   |       4.1       |      20.9      |
|   F   |       6.8       |      24.9      |
|   G   |       6.8       |      31.1      |
|   H   |       5.5       |      20.2      |
|   I   |       5.1       |      23.7      |

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

## Utilisation de Opencv
import cv2

**charger une image couleur**

img=cv2.imread("totoro.png")

**charger une image niveau de gris**

img_depth = cv2.imread("totoro_depth.png",cv2.IMREAD_GRAYSCALE)

**obtenir la taille d'une image**

img.shape

(hauteur, largeur)

**afficher une image**

cv2.imshow("image",img)

**sauvegarder une image**

filename = "resultat.png"

cv2.imwrite(filename, img_depth)

**séparer les canaux d'une image couleur**

B, G, R = cv2.split(img)

cv2.imshow("blue", B)

**additionner(superposer) 2 images**

cv2.addWeighted(img1, wt1, img2, wt2, gammaValue)

wt1 est le poids de l'image1 et wt2 celui de l'image2

gammaValue est la mesure de la lumière, exemple 0

**redimensionner une image**

new_image = cv2.resize(img_depth, (width,height))

**detection de contour Canny**

canny = cv2.Canny(new_image, minval, maxval)

https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html








