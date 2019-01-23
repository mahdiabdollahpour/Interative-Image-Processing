import numpy as np
import random
import cv2 as cv


class Drop:
    def __init__(self, x, y, min_speed, max_speed, type, melt_time, shape):
        self.x = x
        self.y = y
        self.speed = random.randint(min_speed, max_speed)
        self.type = type
        self.sf = 0
        self.melt_time = melt_time
        self.shape = shape


def write_image(small, large, upleftx, uplefty):
    newimg = large.copy()
    sd = np.shape(small)
    for i in range(upleftx, upleftx + sd[0]):
        for j in range(uplefty, uplefty + sd[1]):
            rgb = small[i - upleftx, j - uplefty, :]
            inten = np.sum([x * x for x in rgb])
            if (inten > 15):
                newimg[i, j, :] = small[i - upleftx, j - uplefty, :]
    return newimg


def write_image2(small, large, upleftx, uplefty):
    newimg = large.copy()
    sd = np.shape(small)
    for i in range(upleftx, upleftx + sd[0]):
        for j in range(uplefty, uplefty + sd[1]):
            rgb = small[i - upleftx, j - uplefty, :]
            inten = np.sum([x * x for x in rgb])
            if (inten > 40):
                newimg[i, j, :] = small[i - upleftx, j - uplefty, :]
    return newimg


def can_pass(x, y, joda, w, h, thresh):

    if (joda[x, y] > thresh):
        return False
    if (joda[x + int(h / 2), y] > thresh):
        return False
    if (joda[x, y + int(w / 2)] > thresh):
        return False
    if (joda[x + int(h / 2), y + int(w / 2)] > thresh):
        return False
    if (joda[x + h - 1, y] > thresh):
        return False
    if (joda[x, y + w - 1] > thresh):
        return False
    if (joda[x + h - 1, y + w - 1] > thresh):
        return False
    if (joda[x + h - 1, y + int(w / 2)] > thresh):
        return False
    if (joda[x + int(h / 2), y + w - 1] > thresh):
        return False
    return True


def cluster(img):
    Z = img.reshape((-1, 3))

    # convert to np.float32
    Z = np.float32(Z)

    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = 2
    ret, label, center = cv.kmeans(Z, K, None, criteria, 10, cv.KMEANS_RANDOM_CENTERS)

    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape((img.shape))
    return res2
