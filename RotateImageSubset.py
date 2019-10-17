# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 22:34:58 2019

@author: njoosse
"""

import imageio
import numpy as np
from PIL import Image

imagePath = r"rainbow-rocket-seal-canvas.png"
centerX = 295
centerY = 520
circleRadius = 70
rotationDegree = 180
outputImagePath = 'outputImage.png'

def verifyImage(imagePath):
    try:
        img = Image.open(imagePath) # open the image file
        img.verify() # verify that it is, in fact an image
        return True
    except (IOError, SyntaxError):
        print('Bad file:', imagePath)
        return False

def circle_rotate(imagePath, x, y, radius, degree):
    # reads the image into a numpy array
    image = imageio.imread(imagePath, pilmode = 'RGB')
    img_arr = np.asarray(image)
    # Creates the bounding box for the subset
    box = (x-radius, y-radius, x+radius+1, y+radius+1)
    crop_arr = img_arr[box[0]:box[2], box[1]:box[3]]#np.asarray(crop)
    # build the cirle mask
    mask = np.zeros((2*radius+1, 2*radius+1))
    for i in range(crop_arr.shape[0]):
        for j in range(crop_arr.shape[1]):
            if (i-radius)**2 + (j-radius)**2 <= radius**2:
                mask[i,j] = 1
    # create the new circular image
    sub_img_arr = np.empty(crop_arr.shape ,dtype='uint8')
    sub_img_arr = crop_arr
    # Rotates the image in the array
    sub_img = Image.fromarray(sub_img_arr, "RGB").rotate(degree)
    i2 = image.copy()
    xOffset = box[1]
    yOffset = box[0]
    # places the pixel values into the copy of the image after the rotation
    for idx, val in np.ndenumerate(sub_img):
        if mask[idx[:2]]:
            i2[idx[0]+yOffset, idx[1]+xOffset, idx[2]] = val
    
    return i2

if verifyImage(imagePath):
    i2 = circle_rotate(imagePath, centerX, centerY, circleRadius, rotationDegree)
    imageio.imwrite(outputImagePath, i2)