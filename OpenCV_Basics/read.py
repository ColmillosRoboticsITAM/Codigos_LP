import cv2 as cv
import numpy as np

img = cv.imread('../Latas/Lata1.png')
cv.imshow('lata',img)

blank = np.zeros(img.shape, dtype='uint8')



cv.waitKey(0)

