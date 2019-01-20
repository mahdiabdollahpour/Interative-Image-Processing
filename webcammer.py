import numpy as np
import cv2 as cv
import random
from utils import Drop
from utils import *
from time import time

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
s2_img = cv.imread('files\snow.png')
s_img = cv.resize(s_img, (0, 0), fx=drop_scale, fy=drop_scale)
s2_img = cv.resize(s2_img, (0, 0), fx=drop_scale * 3, fy=drop_scale * 3)
global added_image


def overlay_drop(d):
    global added_image
    if (d.type == 0):
        added_image = write_image(s_img, added_image, d.x, d.y)
    else:
        added_image = write_image2(s2_img, added_image, d.x, d.y)
    return added_image


print(np.shape(s_img))
print(np.shape(s2_img))

cnt = 0
ssize = np.shape(s_img)
s2size = np.shape(s2_img)
max_drop_num = 70
drop_num = 0
max_drop_speed = 10
min_drop_speed = 5
drops = []
melt_time = 0
# pool = Pool(processes=max_drop_num)
while (True):
    global added_image
    ret, l_img = cap.read()
    # print(np.shape(l_img))
    # l_img = cv.resize(l_img, (0, 0), fx=0.5, fy=0.5)
    t = time()
    joda = separate(l_img)
    # print(np.shape(l_img))
    lsize = np.shape(l_img)
    cnt += 1
    for dr in drops:
        if (joda[dr.x + int(ssize[0] / 2), dr.y + int(ssize[1] / 2)] < 50):
            dr.x += dr.speed
        else:
            dr.sf += 1
            if(dr.sf > melt_time):
                dr.type = 0
        if (dr.type == 0):
            if (dr.x + ssize[0] >= lsize[0]):
                drops.remove(dr)
        else:
            if (dr.x + s2size[0] >= lsize[0]):
                drops.remove(dr)
    added_image = l_img.copy()
    for i in range(0, 20):
        if (random.randint(0, 2) % 2 == 0 and False):
            d = Drop(0, random.randint(0, lsize[1] - ssize[1]), min_drop_speed, max_drop_speed, 0)
        else:
            d = Drop(0, random.randint(0, lsize[1] - s2size[1]), min_drop_speed, max_drop_speed, 1)

        drops.append(d)
        if (len(drops) >= max_drop_num):
            break
    drop_num = len(drops)
    threads = []
    for d in drops:
        overlay_drop(d)
    print(time() - t)
    cv.imshow('image', added_image)
    cv.imshow('joda', joda)
    cv.waitKey(3)

# ret, l_img = cap.read()
# cap.release()
cv.destroyAllWindows()
