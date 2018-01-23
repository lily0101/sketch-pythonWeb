# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 09:54:01 2018

@author: lily0101
"""

#doing all the relevant imports
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
from skimage.feature import match_template

# Read in the image and convert to grayscale
fig,axs = plt.subplots(1,3)
img1 = mpimg.imread('./data/student.png')
print(img1.shape)
img2 = mpimg.imread('./data/student.png')
axs = axs.ravel()#packed as 1-d array
axs[0].set_title("teacher")
axs[0].imshow(img1,plt.gray())
axs[1].set_title("student")
axs[1].imshow(img2,plt.gray())
'''
print(image.shape)
plt.imshow(image)
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
print(gray)
plt.imshow(gray,cmap='gray')
# Define a kernel size for Gaussian smoothing / blurring
# Note: this step is optional as cv2.Canny() applies a 5x5 Gaussian internally

# Define parameters for Canny and run it
# NOTE: if you try running this code you might want to change these!
low_threshold = 0
high_threshold = 3
edges = np.zeros_like(gray)
edges[gray == 1] = 0 
edges = cv2.Canny(blur_gray, low_threshold, high_threshold)
print(edges)

# Display the image
plt.imshow(edges, cmap='Greys_r')
'''
result = match_template(img1,img2)
print(result)