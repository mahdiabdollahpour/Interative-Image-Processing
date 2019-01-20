import numpy as np
import cv2 as cv
import random

# cap = cv.VideoCapture('sample.mp4')
cap = cv.VideoCapture('files\cars.mp4')

# fgbg = cv.bgsegm.createBackgroundSubtractorMOG()
# fgbg = cv.createBackgroundSubtractorMOG2()


kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
fgbg = cv.bgsegm.createBackgroundSubtractorGMG()
cnt = 0
while (1):
    cnt += 1
    print("frame :", cnt)
    ret, frame = cap.read()  # Grabs, decodes and returns the next video frame.
    # print(np.shape(frame))
    frame = cv.resize(frame, (0, 0), fx=0.25, fy=0.25)
    fgmask = fgbg.apply(frame)
    # print(np.shape(fgmask))
    shape = np.shape(fgmask)
    print(fgmask)
    idx = 1
    for i in range(shape[0]):
        for j in range(shape[1]):
            if fgmask[i][j] > 230:
                frame[i][j][idx] = 255
                frame[i][j][(idx + 1) % 3] = 0
                frame[i][j][(idx + 2) % 3] = 0
            # if i % 30 == 0:
            #     idx = (idx + 1) % 3
            # print("doing it")

    cv.imshow('frame', frame)
    cv.imshow('frame2', fgmask)
    k = cv.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv.destroyAllWindows()
