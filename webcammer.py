import numpy as np
import cv2 as cv
import random
from utils import Drop
from utils import *

# cap = cv.VideoCapture('files\sample.mp4')
cap = cv.VideoCapture(0)

# fgbg = cv.bgsegm.createBackgroundSubtractorMOG()
# fgbg = cv.bgsegm.createBackgroundSubtractorGMG()
fgbg = cv.createBackgroundSubtractorMOG2()

kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))

def separate(img):
    return fgbg.apply(img)

drop_scale = 0.025
s_img = cv.imread('files\drop.png')
s_img = cv.resize(s_img, (0, 0), fx=drop_scale, fy=drop_scale)
print(np.shape(s_img))



cnt = 0
ssize = np.shape(s_img)
max_drop_num = 50
drop_num = 0
drop_speed = 10
drops = []

while (True):
    ret, l_img = cap.read()
    # print(np.shape(l_img))
    # l_img = cv.resize(l_img, (0, 0), fx=0.5, fy=0.5)

    joda = separate(l_img)
    # print(np.shape(l_img))
    lsize = np.shape(l_img)
    cnt += 1
    for dr in drops:
        if (joda[dr.x + int(ssize[0] / 2), dr.y + int(ssize[1] / 2)] < 50):
            dr.x += drop_speed
        if (dr.x + ssize[0] >= lsize[0]):
            drops.remove(dr)
    added_image = l_img.copy()
    for i in range(drop_num, max_drop_num):
        d = Drop(0, random.randint(0, lsize[1] - ssize[1]))
        drops.append(d)
    drop_num = len(drops)
    for d in drops:
        added_image = write_image(s_img, added_image, d.x, d.y)

    cv.imshow('image', added_image)
    cv.imshow('joda', joda)
    cv.waitKey(50)

# ret, l_img = cap.read()
# cap.release()
cv.destroyAllWindows()
