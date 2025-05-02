import cv2 as cv
import numpy as np

img = cv.imread('../Latas/Lata5.png')
cv.imshow('lata',img)

blank = np.zeros(img.shape, dtype='uint8')

mask = cv.circle(blank, (img.shape[1]//2, img.shape[0]//2), 100, (255,255,255), -1)
cv.imshow('mask',mask)

masked = cv.bitwise_and(img, mask)
cv.imshow('masked',masked)


cv.waitKey(0)

