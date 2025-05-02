import cv2
import cv2 as cv
import imutils

capture =  cv.VideoCapture(1, cv.CAP_DSHOW)
while True:
    isTrue, frame = capture.read()
    #cv.imshow('vid', frame)

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow('gray', gray)

    threshold, thresh = cv.threshold(gray, 15, 100, cv.THRESH_BINARY_INV)
    cv.imshow('thresh', thresh)

    #th, thresh_inv = cv.threshold(gray, 100, 255, cv.THRESH_BINARY_INV)
    #cv.imshow('thresh_inv', thresh_inv)

    conto = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    conto = imutils.grab_contours(conto)
    count = 1
    for c in conto:
        area = cv2.contourArea(c)
        count = count + 1
        if area > 2700 and area < 9500:
            cv2.drawContours(frame, [c], -1,(0,255,0),3)
            M = cv2.moments(c)

            cx = int(M["m10"]/ M["m00"])
            cy = int(M["m01"]/ M["m00"])

            cv2.circle(frame, (cx,cy),7,(255,255,255),-1)
            cv2.imshow("centre", frame)
            print("Centroid: ",count, cx,cy,area)
    if cv.waitKey(20) & 0xFF==ord('d'):
        break
capture.release()
cv.destroyAllWindows()