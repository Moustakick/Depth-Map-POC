# PDP

## Liens utiles

+ Dataset NyuV2 : https://cs.nyu.edu/~silberman/datasets/nyu_depth_v2.html
+ Dense-Depth : https://github.com/ialhashim/DenseDepth

## Utilisation 

### Depthmap generator

This part came from [DenseDepth](https://github.com/ialhashim/DenseDepth). 

Dependencies :
- Pillow
- Numpy
- Matplotlib
- Keras
- Tensorflow

Uses : 
In `depthmap_generator/`, donwnload and put a pretrained model in `pretrained/`. You can refer to [NYU Depth V2 model](https://drive.google.com/file/d/19dfvGvDfCRYaqxVKypp1fRHwK7XtSjVu/view?usp=sharing), as we have tested it only with this model. If you want to use another model you can specify the `--model` argument. 
Put images on `image/` directory, if you want to use another file path you can specify the `--input` argument. 
Also, by default images will be resize in 640 by 480 (portrait or landscape is not a problem) because the model was trained on Nyu dataset, if you use other models you can specify the size with `--size` arguments.
Now you can launch `python3 generator` to generate your depthmaps. 

### Expérimentations

+ Télécharger le dataset NyuV2 : https://drive.google.com/drive/folders/1TzwfNA5JRFTPO-kHMU___kILmOEodoBo
+ commande : `python3 main.py "chemin vers l'image couleur" "chemin vers la carte de profondeur" "seuil de profondeur"`