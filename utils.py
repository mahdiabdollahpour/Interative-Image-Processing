import numpy as np
import random


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
    if (joda[x + h, y] > thresh):
        return False
    if (joda[x, y + w] > thresh):
        return False
    if (joda[x + h, y + w] > thresh):
        return False
    if (joda[x + h, y + int(w / 2)] > thresh):
        return False
    if (joda[x + int(h / 2), y + w] > thresh):
        return False
    return True
