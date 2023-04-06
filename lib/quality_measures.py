import numpy as np
import cv2

import utils

def average_gradient_magnitude(image):
    image = np.float32(image*255)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gradient_x = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=5)
    gradient_y = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=5)
    gradient_norm = np.sqrt(gradient_x**2 + gradient_y**2)

    utils.save_image(gradient_norm, "norm")

    sharpness = np.average(gradient_norm)
    return sharpness

def signal_noise_ratio(reference, image):
    standard_deviation = np.std(reference)
    mean_squarred_error = np.mean((reference.ravel()-image.ravel())**2)
    snr = standard_deviation / mean_squarred_error
    decibel_snr = 10.0 * np.log10(snr)
    return decibel_snr
