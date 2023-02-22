import os
import glob
import argparse

# Keras / TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '5'
from keras.models import load_model
from layers import BilinearUpSampling2D
from tensorflow.keras.layers import Layer, InputSpec
from utils import predict, load_images, display_images, save_images
from matplotlib import pyplot as plt

from PIL import Image, ImageChops
import numpy as np

# Argument Parser
parser = argparse.ArgumentParser(description='High Quality Monocular Depth Estimation via Transfer Learning')
parser.add_argument('--model', default='pretrained/nyu.h5', type=str, help='Trained Keras model file.')
parser.add_argument('--input', default='image/*.png', type=str, help='Input filename or folder.')
parser.add_argument('--size', default='640,480', type=str, help='Size of the input images.')
args = parser.parse_args()

# Custom object needed for inference and training
custom_objects = {'BilinearUpSampling2D': BilinearUpSampling2D, 'depth_loss_function': None}

print('Loading model...')

# Load model into GPU / CPU
model = load_model(args.model, custom_objects=custom_objects, compile=False)

print('\nModel loaded ({0}).'.format(args.model))

# Input images
size = args.size.split(",")
size = (int) (size[0]), (int) (size[1])
size = sorted(size)
print(size)
inputs = load_images(glob.glob(args.input), size)
print('\nLoaded ({0}) images of size {1}.'.format(inputs.shape[0], inputs.shape[1:]))

# Compute results
outputs = predict(model, inputs)

# Save results
i=0
for results in outputs:
    cmap = plt.get_cmap('Greys')
    rescaled = results[:,:,0]
    rescaled = rescaled - np.min(rescaled)
    rescaled = rescaled / np.max(rescaled)
    img = cmap(rescaled)[:,:,:3]
    img = Image.fromarray(np.uint8(img*255))
    img = ImageChops.invert(img)
    img.save("depthmap/result"+str(i)+".png")
    i+=1 

# Display results
viz = display_images(outputs.copy(), inputs.copy())
plt.figure(figsize=(10,5))
plt.imshow(viz)
# plt.savefig('test.png')
plt.show()
