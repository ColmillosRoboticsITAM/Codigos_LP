import cv2 as cv
import numpy as np

img = cv.imread('../Latas/Lata1.png')
cv.imshow('lata',img)

blank = np.zeros(img.shape, dtype='uint8')

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('gray',gray)

hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
cv.imshow('hsv',hsv)

lab = cv.cvtColor(img, cv.COLOR_BGR2LAB)
cv.imshow('lab',lab)

cv.waitKey(0)

