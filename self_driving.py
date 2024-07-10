import numpy as np
import cv2
from services.detection import detection
from services.svm import SVM
from services.utils import imwrite

# if you want print some log when your program is running,
# just append a string to this variable
log = []


def is_yellow(view, i, j):  # 判断view中位置(i,j)是不是黄色
    if view[i, j, 1] >= 240 and view[i, j, 2] >= 240:
        return True
    else:
        return False


def is_white(view, i, j):  # 判断view中位置(i,j)是不是白色
    if view[i, j, 0] >= 240 and view[i, j, 1] >= 240 and view[i, j, 2] >= 240:
        return True
    else:
        return False


def line_following(view1, dis):  # 巡线模式
    dif, li, ri = 0, 0, 140
    for j in range(140, 49, -1):
        if is_yellow(view1, dis, j):
            ri = j
            break
    for i in range(50):
        if is_yellow(view1, dis, i):
            li = i
            break
    dif = (ri + li) / 2.0 - 80
    if dif <= 5:
        k = 0.01
    elif dif <= 10:
        k = 0.02
    else:
        k = 0.05
    
    return dif, k


def adjust_pose(view1):  # 倒车入库后调整位姿
    li, ri = 0, 0
    for i in range(70):
        if is_yellow(view1, i, 40):
            li = i
            break
    for j in range(70):
        if is_yellow(view1, j, 120):
            ri = j
            break
    dif = li - ri
    
    return dif


def adjust_pose2(view1):  # 侧方停车后调整位姿
    li, ri = 0, 119
    for i in range(100, 50, -1):
        if is_white(view1, i, 70):
            li = i
            break
    for j in range(100, 50, -1):
        if is_white(view1, j, 90):
            ri = j
            break
    log.append(str(li) + "," + str(ri))
    if abs(li - ri) <= 5:
        return True
    else:
        return False


def change_state(view1):  # 侧方停车出来后回到巡线模式
    for i in range(24, 41):
        if is_yellow(view1, 0, i):
            return True
    return False


def image_to_speed(view1, view2, view3, state):
    """This is the function where you should write your code to
    control your car.

    You need to calculate your car wheels' speed based on the views.

    Whenever you need to print something, use log.append().

    Args:
        view1 (ndarray): The left-bottom view,
                          it is colorful, 3 * 120 * 160
        view2 (ndarray): The right-bottom view,
                          it is colorful, 3 * 120 * 160
        view3 (ndarray): The right-up view,
                          it is colorful, 3 * 120 * 160
        state: your car's state, initially None, you can
               use it by state.set(value) and state.get().
               It will persist during continuous calls of
               image_to_speed. It will not be reset to None
               once you have set it.

    Returns:
        (left, right): your car wheels' speed
    """
    dis = 35
    left_speed = right_speed = 0
    if state.get() is None:
        state.set(1)  # 开始时进入巡线模式
    
    # 标志识别模式
    if view2 is not None:
        detector = detection()
        im = view2  # 480*640*3的ndarray
        rect = detector.ensemble(im)  # 使用HSV+形态学处理提取标志牌检测框
        if rect:
            xmin, ymin, xmax, ymax = rect
            # log.append(str(xmin) + "," + str(ymin) + "," + str(xmax) + "," + str(ymax))
            if xmin > 510 and ymin > 75 and ymax < 230:
                if state.get() == 6:
                    state.set(7)
            if xmin > 110 and ymin > 170 and xmax < 220 and ymax < 275:
                if state.get() == 1:
                    state.set(6)
            if ymin > 30 and xmax < 100 and ymax < 150:
                if state.get() == 1:
                    state.set(2)
            if ymin > 60 and xmax < 130 and ymax < 190:
                if state.get() == 5:
                    state.set(1)
        if state.get() == 2:
            for i in range(420, 450):
                if is_white(im, 470, i):
                    state.set(3)
                    break
    if view1 is not None:
        if state.get() == 3 and is_yellow(view1, 90, 80):
            state.set(4)
        if state.get() == 4 and is_yellow(view1, 15, 80):
            state.set(5)
        if state.get() == 8 and adjust_pose2(view1):
            state.set(9)
        if state.get() == 9 and change_state(view1):
            state.set(10)
    # 控制车速
    if state.get() == 1:
        dif, k = line_following(view1, dis)
        if abs(dif) <= 2:
            left_speed = max(0, 0.7 + k * dif)
            right_speed = max(0, 0.7 - k * dif)
        elif abs(dif) > 2:
            left_speed = max(0, 0.4 + k * dif)
            right_speed = max(0, 0.4 - k * dif)
    elif state.get() == 2:
        left_speed = -0.5
        right_speed = -0.08
    elif state.get() == 3:
        dif = adjust_pose(view1)
        left_speed = min(-0.1 - 0.009 * dif, 0)
        right_speed = min(-0.1 + 0.009 * dif, 0)
    elif state.get() == 4:
        left_speed = 0.4
        right_speed = 0.4
    elif state.get() == 5:
        left_speed = 0.58
        right_speed = 0.08
    elif state.get() == 6:
        left_speed = -0.5
        right_speed = -0.1
    elif state.get() == 7:
        left_speed = -1.4
        right_speed = -1.4
        state.set(8)
    elif state.get() == 8:
        left_speed = -0.1
        right_speed = -0.5
    elif state.get() == 9:
        left_speed = 0.1
        right_speed = 0.5
    elif state.get() == 10:
        left_speed = 1.3
        right_speed = 1.3
        state.set(1)
    log.append("#" + str(state.get()))
    log.append("left_speed:" + str(left_speed))
    log.append("right_speed:" + str(right_speed))
    
    return left_speed, right_speed
