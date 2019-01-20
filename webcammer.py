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
rain_Image = cv.imread('files\drop.png')
snow_Image = cv.imread('files\snow.png')
rain_Image = cv.resize(rain_Image, (0, 0), fx=drop_scale, fy=drop_scale)
snow_Image = cv.resize(snow_Image, (0, 0), fx=drop_scale * 3, fy=drop_scale * 3)
global added_image

rain_type = 0
snow_type = 1


def overlay_drop(d):
    global added_image
    if (d.type == rain_type):
        added_image = write_image(rain_Image, added_image, d.x, d.y)
    else:
        added_image = write_image2(snow_Image, added_image, d.x, d.y)
    return added_image


print(np.shape(rain_Image))
print(np.shape(snow_Image))

cnt = 0
rain_size = np.shape(rain_Image)
snow_size = np.shape(snow_Image)
max_drop_num = 50
drop_num = 0
max_drop_speed = 10
min_drop_speed = 5
drops = []
melt_time_min = 6
melt_time_max = 12
# pool = Pool(processes=max_drop_num)
while (True):
    global added_image
    ret, l_img = cap.read()

    t = time()
    joda = separate(l_img)
    lsize = np.shape(l_img)
    cnt += 1
    for dr in drops:
        # if (joda[dr.x + int(ssize[0] / 2), dr.y + int(ssize[1] / 2)] < 50):
        if (can_pass(dr.x, dr.y, joda, dr.shape[0], dr.shape[1], 50)):
            dr.x += dr.speed
        else:
            dr.sf += 1
            if (dr.sf > dr.melt_time):
                dr.type = rain_type
                dr.shape = rain_size

        if (dr.x + dr.shape[0] >= lsize[0]):
            drops.remove(dr)

    added_image = l_img.copy()
    for i in range(0, 20):
        d = Drop(0, random.randint(0, lsize[1] - snow_size[1]), min_drop_speed, max_drop_speed, snow_type,
                 random.randint(melt_time_min, melt_time_max), snow_size)
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

cv.destroyAllWindows()
