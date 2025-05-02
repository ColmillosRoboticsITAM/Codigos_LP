import cv2 as cv

img = cv.imread('../Latas/Lata6.png')
#cv.imshow('lata',img)
#convert to grayscale

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('grayscale', gray)

#blur
blur = cv.GaussianBlur(img, (3,3), cv.BORDER_DEFAULT)
#cv.imshow('blur', blur)

#edge cascade
edge = cv.Canny(blur, 125, 175)
cv.imshow('canny', edge)

dilated = cv.dilate(edge, (7,7), iterations=3)
#cv.imshow('dilated', dilated)

erode = cv.erode(dilated, (7,7), iterations=3)
#cv.imshow('eroded', erode)

resized = cv.resize(img, (500,500), interpolation=cv.INTER_CUBIC)
cv.imshow('resized', resized)

croped = img[50:200, 200:400]
cv.imshow('croped', croped)

cv.waitKey(0)

