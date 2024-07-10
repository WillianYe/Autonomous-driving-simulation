# -*- coding: UTF-8 -*-
import numpy as np
import cv2
from driver import driver

car = driver()


def one_same():
    x = 80
    y = 80
    return x, y


def diff_left():
    x = 40
    y = 80
    return x, y


def diff_right():
    x = 80
    y = 40
    return x, y


while True:
    for i in range(20): car.set_speed(one_same()[0], one_same()[1])

    #for i in range(20): car.set_speed(diff_left()[0], diff_left()[1])

    #for i in range(20): car.set_speed(diff_right()[0], diff_right()[1])
