import cv2 as cv
import numpy as np

# img = cv.imread('Latas/Lata1.png')
# cv.imshow('lata',img)

blank = np.zeros((400,400), dtype='uint8')

rect = cv.rectangle(blank.copy(), (30,30), (370,370), 255, -1)
circ = cv.circle(blank.copy(), (200,200), 200, 255, -1)

cv.imshow('rec', rect)
cv.imshow('circ', circ)

#-----------------AND-----------------#
bit_and = cv.bitwise_and(rect, circ)
cv.imshow('bit_and', bit_and)

#-----------------OR-----------------#
bit_or = cv.bitwise_or(rect, circ)
cv.imshow('bit_or', bit_or)

#-----------------XOR-----------------#
bit_xor = cv.bitwise_xor(rect, circ)
cv.imshow('bit_xor', bit_xor)

#-----------------NOT-----------------#
bit_not = cv.bitwise_not(rect)
cv.imshow('bit_not', bit_not)

cv.waitKey(0)

