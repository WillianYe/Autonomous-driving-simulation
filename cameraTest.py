# -*- coding: UTF-8 -*-
import cv2
import os
import numpy as np
from nor_img import undistort, warp, process
from driver import driver

#cap1 = cv2.VideoCapture(0) #后摄像头
cap2 = cv2.VideoCapture(1) #前摄像头

car = driver()
e_i = 0
e_p = 0
e_d = 0

tt = 0

while True:
    #_, frame1 = cap1.read()
    _, frame2 = cap2.read()
    img2 = undistort(frame2)
    #cv2.imshow("frame",frame2)
    cv2.imshow("img2",img2)
    warp2 = warp(img2)
    bina2 = process(warp2)
    #cv2.imshow("binary",bina2)
    
    max_v = np.zeros(6)
    max_l = np.zeros(6)
    
    
    for j in range(6):
        for i in range(0,520,40):
            tmp = bina2[j*80:j*80+80,i:i+120].mean()
            if tmp > max_v[j]:
                max_v[j] = tmp
                max_l[j] = i+40
            
    #_, ws = np.where(bina2>200)
    error = 0
    cnt = 0
    for i in range(6):
        if max_v[i] > 0:
            cnt = cnt + 1
            error = error + (max_l[i]-320) / 320.0
            #im = cv2.rectangle(warp2,(int(max_l[i]-40),int(i*80)),(int(max_l[i]+80),int((i+1)*80)),(0,0,255),2)
            
            
    
    #cv2.imshow("im",im)
    if cnt > 0:
        error = error / cnt
    else:
        error = 0
        
    e_i = e_i + error
    e_d = error - e_p
    e_p = error
    
    kp = 1.0
    ki = 0.0
    kd = 0.0
    
    v = 40
    w = int(20 * (kp * error + ki * e_i + kd * e_d))
    
    
    l_s = v - w
    r_s = v + w
    if l_s < 0:
        l_s = 5
    if r_s < 0:
        r_s = 5
    #print(error,l_s,r_s)
    
    #for i in range(20):
    #car.set_speed(l_s, r_s)
    #print(car.get_sensor())
    #print(car.read_battery())
    #print("@@@")
    key = cv2.waitKey(1)
    
    if key == ord('q'):
        tt = tt + 1
        filepath = "./imgs/img_" + str(tt) + '.jpg'
        cv2.imwrite(filepath, img2)
        print('saved in:',filepath)
    if key == ord('s'):
        break
    
