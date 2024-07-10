# -*- coding: UTF-8 -*-
import cv2
import numpy as np


"""
DIM=(640, 480)
K=np.array([[499.05021523540756, 0.0, 333.3412892374512], [0.0, 483.81654015414097, 242.69653225978055], [0.0, 0.0, 1.0]])
D=np.array([[-0.869900379788289], [1.3590213730501584], [-1.820747530181677], [1.1118149732028872]])
"""
DIM=(640, 480)
K=np.array([[-5198.347002578433, -0.0, 322.2498961240888], [0.0, -5256.783989831324, 245.62154951821046], [0.0, 0.0, 1.0]])
D=np.array([[-128.930840598615], [22976.1473011057], [-2773014.037028126], [143281119.86853617]])


def undistort_up(img_path,scale=0.5,imshow=False):
    img = cv2.imread(img_path)
    dim1 = img.shape[:2][::-1]  #dim1 is the dimension of input image to un-distort
    assert dim1[0]/dim1[1] == DIM[0]/DIM[1], "Image to undistort needs to have same aspect ratio as the ones used in calibration"
    if dim1[0]!=DIM[0]:
        img = cv2.resize(img,DIM,interpolation=cv2.INTER_AREA)
    Knew = K.copy()
    if scale:#change fov
        Knew[(0,1), (0,1)] = scale * Knew[(0,1), (0,1)]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), Knew, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    if imshow:
        cv2.imshow("undistorted", undistorted_img)
    cv2.imwrite('unfisheyeImage_up.png', undistorted_img)
    return undistorted_img


def undistort(img):

    img = cv2.resize(img, DIM)
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM,cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT)    

    return undistorted_img

def warp(img):
    x = 300
    y = 180
    img_info = img.shape
    height = img_info[0]
    width = img_info[1]
    #获取原图像的左上角，左下角，右上角三个点的坐标  （三点确定图像所在二维平面）
    pts1 = np.float32([[250, 280],[400,280],[0, height],[width,height]])
    
    pts2 = np.float32([[0, 0],[width,0],[0, height],[width,height]])
    # 生成透视变换矩阵；进行透视变换
    M = cv2.getPerspectiveTransform(pts1, pts2)
    dst = cv2.warpPerspective(img, M, (width,height))
    
    #cv2.imshow('dst',dst)

    return dst


def process(img):
    
    black = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(black,(5,5),0)

    ret,th = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    canny = cv2.Canny(th, 50, 150)
    
    return canny
#cv2.namedWindow(window_name)

#创建滑动条
#cv2.createTrackbar( trackbar_value_x, window_name, min_x, max_x, warp)
#cv2.createTrackbar( trackbar_value_y, window_name, min_y, max_y, warp)

#while(True):
if __name__=='__main__':
    
    for cnt in range(1,9):
        #cnt = 1
    
        img = cv2.imread('./imgs/img_'+str(cnt)+'_calib.jpg')

        warp_img = warp(img)
        
        th, ca = process(warp_img)
        
        cv2.imwrite('./imgs/img_edge_'+str(cnt)+'.jpg',ca)
        cv2.imwrite('./imgs/img_black_'+str(cnt)+'.jpg',th)
    
    print("yes")
    
