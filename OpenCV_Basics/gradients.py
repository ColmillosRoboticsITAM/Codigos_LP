import numpy as np
import cv2 as cv

img = cv.imread('../Latas/lata1.png')
cv.imshow('lata', img)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('gray',gray)

#-----------------Laplacian-----------------#
lap = cv.Laplacian(gray, cv.CV_64F)
lap = np.uint8(np.absolute(lap))
cv.imshow('Laplacian', lap)

#-----------------Sobel-----------------#
sobelx = cv.Sobel(gray, cv.CV_64F,1,0)
sobely = cv.Sobel(gray, cv.CV_64F,0,1)

# cv.imshow('sobelx', sobelx)
# cv.imshow('sobely', sobely)
sobel_combined = cv.bitwise_or(sobelx, sobely)
cv.imshow('sobel_combined', sobel_combined)

#-----------------Canny-----------------#
canny = cv.Canny(gray, 150, 175)
cv.imshow('canny', canny)
#canny is better, makes it cleanner


cv.waitKey(0)