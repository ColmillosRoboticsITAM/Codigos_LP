import cv2 as cv

capture =  cv.VideoCapture(1, cv.CAP_DSHOW)
while True:
    isTrue, frame = capture.read()
    cv.imshow('vid', frame)
    if cv.waitKey(20) & 0xFF==ord('d'):
        break
capture.release()
cv.destroyAllWindows()

#If -215 error appears it means cv cannot find the image or video

