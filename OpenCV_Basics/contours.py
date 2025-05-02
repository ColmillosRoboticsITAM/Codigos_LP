import cv2 as cv
import numpy as np

img = cv.imread('../Latas/Lata5.png')
cv.imshow('lata',img)

blank = np.zeros(img.shape, dtype='uint8')
#cv.imshow('blank',blank)


gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
#cv.imshow('gray',gray)

blur = cv.GaussianBlur(gray, (5,5), cv.BORDER_DEFAULT)
cv.imshow('blur',blur)

# canny = cv.Canny(blur, 125, 175)
# cv.imshow('canny',canny)

ret, thresh = cv.threshold(blur, 170, 255, cv.THRESH_BINARY)
# cv.imshow('thresh',thresh)

inv_thresh = cv.bitwise_not(thresh)
cv.imshow('inv_thresh',inv_thresh)


contours, hierarchies = cv.findContours(inv_thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
print(f'{len(contours)} contours(s) found!')

cv.drawContours(blank, contours,-1, (255,255,0), 1)
cv.imshow('drawn',blank)

cv.waitKey(0)

