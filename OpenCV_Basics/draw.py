import cv2 as cv
import numpy as np 

blank = np.zeros((500,500,3), dtype='uint8')
cv.imshow('blank',blank)

# img  = cv.imread('../Latas/Lata1.png')
# cv.imshow('image', img)

#Paint the image certain color

# blank[200:300, 400:499] = 100,255,125
# cv.imshow('green',blank)

# cv.rectangle(blank, (0,0), (250,250), (200,100,200), thickness=4)
# #thickness=cv.FILLED == thickness=-1
# cv.imshow('rec', blank)

cv.rectangle(blank, (0,0), (blank.shape[1]//2, blank.shape[0]//2), (200,100,200), thickness=1)
#thickness=cv.FILLED == thickness=-1
cv.imshow('rec', blank)

cv.circle(blank, (250,250), 40, (255,0,0), thickness=1)
cv.imshow('circ', blank)

cv.line(blank, (250,250), (400,450), (0,0,255), thickness=1)
cv.imshow('line', blank)

cv.waitKey(0)
