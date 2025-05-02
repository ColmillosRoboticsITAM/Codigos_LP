import cv2 as cv

# img = cv.imread('Latas/Lata2.png')
# cv.imshow('lata', img)

def rescaleFrame(frame, scale=0.75):
    #work with images, videos, live video
    width = int(frame.shape[1]*scale)
    height = int(frame.shape[0]*scale)
    dimensions = (width, height)
    return cv.resize(frame,dimensions,interpolation=cv.INTER_AREA)

capture =  cv.VideoCapture('../Vids/vid1.mp4')


def changeRes(width, height):
    #only work with live video
    capture.set(3,width)
    capture.set(4,height)


while True:
    isTrue, frame = capture.read()
    
    frame_resized = rescaleFrame(frame,scale=.2)
    
    cv.imshow('vid', frame)
    cv.imshow('vid2', frame_resized)
    
    if cv.waitKey(20) & 0xFF==ord('d'):
        break
capture.release()
cv.destroyAllWindows()



cv.waitKey(0)