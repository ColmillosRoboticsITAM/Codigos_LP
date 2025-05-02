import cv2 as cv
import numpy as np

img = cv.imread('../Latas/Lata6.png')

cv.imshow('lata',img)

#-----------------Translation-----------------#
def translate(img, x, y):
    transMat = np.float32([[1,0,x],[0,1,y]])
    dims = (img.shape[1], img.shape[0])
    return cv.warpAffine(img, transMat, dims)

translated = translate(img, -100,-100)
#cv.imshow('translated',translated)

#-----------------Rotation-----------------#
def rotate(img, angle, rotpt=None):
    (h,w) = img.shape[:2]
    if rotpt is None:
        rotpt = (w//2,h//2)
    rotMat = cv.getRotationMatrix2D(rotpt,angle,1.0)
    dims = (w,h)

    return cv.warpAffine(img, rotMat, dims)
rotated = rotate(img, 90)
#cv.imshow('rotated',rotated)

#-----------------Rotation-----------------#
resized = cv.resize(img, (500,500), interpolation=cv.INTER_LINEAR)
#cv.imshow('resized',resized)

#-----------------flip-----------------#
fliped = cv.flip(img, 1)
cv.imshow('fliped',fliped)

#-----------------Crop-----------------#
Croped = img[200:400, 300:400]
cv.imshow('Croped',Croped)

cv.waitKey(0)
