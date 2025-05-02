import cv2 as cv

img = cv.imread('../Latas/Lata1.png')
cv.imshow('lata',img)


gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('gray', gray)

#-----------------Simple-----------------#
threshold, thresh = cv.threshold(gray, 150, 255, cv.THRESH_BINARY)
cv.imshow('thresh', thresh )

#-----------------Inverse-----------------#
threshold_inv, thresh_inv = cv.threshold(gray, 150, 255, cv.THRESH_BINARY_INV)
cv.imshow('thresh_inv', thresh_inv)

cv.waitKey(0)

