import numpy as np
import cv2 as cv
import random
from utils import Drop
from utils import *
from time import time

cap = cv.VideoCapture('files\sample.mp4')
ret, l_img = cap.read()
l_img = cv.resize(l_img, (0, 0), fx=0.5, fy=0.5)
shape = np.shape(l_img)
print(shape)
print('0 :', shape[0])
print('1 :', shape[1])
#
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('output.avi', fourcc, 20.0, (640,360))

algo = 'knn'

if (algo == 'mog'):
    fgbg = cv.bgsegm.createBackgroundSubtractorMOG()
elif (algo == 'gmg'):
    fgbg = cv.bgsegm.createBackgroundSubtractorGMG()
elif (algo == 'mog2'):
    fgbg = cv.createBackgroundSubtractorMOG2()
else:
    fgbg = cv.createBackgroundSubtractorKNN()

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
max_drop_num = 20
drop_num = 0
max_drop_speed = 5
min_drop_speed = 3
drops = []
melt_time_min = 6
melt_time_max = 12

while (cap.isOpened()):
    global added_image
    ret, l_img = cap.read()
    if (not ret):
        break
    l_img = cv.resize(l_img, (0, 0), fx=0.5, fy=0.5)
    t = time()
    joda = separate(l_img)
    joda = cv.GaussianBlur(joda, (5, 5), 0)
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
    for i in range(0, 7):
        if (len(drops) >= max_drop_num):
            break
        d = Drop(0, random.randint(0, lsize[1] - snow_size[1]), min_drop_speed, max_drop_speed, snow_type,
                 random.randint(melt_time_min, melt_time_max), snow_size)
        drops.append(d)

    drop_num = len(drops)
    threads = []
    for d in drops:
        overlay_drop(d)
    print(time() - t)
    out.write(added_image)
    print(np.shape(added_image))


    cv.imshow('video', added_image)
    cv.imshow('background subtracted', joda)
    cv.waitKey(3)


out.release()
print('it was released')
cap.release()
cv.destroyAllWindows()
