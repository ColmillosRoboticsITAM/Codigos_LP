import cv2 as cv

capture =  cv.VideoCapture(0)
while True:
    isTrue, frame = capture.read()
    cv.imshow('vid', frame)
    if cv.waitKey(20) & 0xFF==ord('d'):
        break
capture.release()
cv.destroyAllWindows()

#If -215 error appears it means cv cannot find the image or video

