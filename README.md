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
|     image     | original  | depth of field |
| :-----------: | :-------: | :------------: |
| introspection | 551.23303 |    466.7878    |
|    totoro     | 360.85947 |    273.671     |

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








