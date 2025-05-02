import cv2 as cv
import numpy as np

img = cv.imread('../Latas/Lata1.png')
cv.imshow('lata',img)

blank = np.zeros(img.shape, dtype='uint8')

#-----------------Average-----------------#
average = cv.blur(img, (7,7))
cv.imshow('average',average)

#-----------------Gaussian-----------------#
Gaussian = cv.GaussianBlur(img, (7,7), 0)
#cv.imshow('Gaussian blur',Gaussian)

#-----------------Median-----------------#
Median = cv.medianBlur(img, 7)
#cv.imshow('Median blur',Median)

#-----------------Bilateral-----------------#
Bilateral = cv.bilateralFilter(img, 10, 35, 25)
cv.imshow('Bilateral blur',Bilateral)

cv.waitKey(0)

