## 自动驾驶小车仿真
根据小车不同视角的三张图片控制其左右车轮的速度，完成巡线、倒车入库和侧方停车任务。

+ calib.py和nor_img.py用于实现图像矫正等预处理
+ cameraTest.py用于获取并处理图像
+ car_run.py用于差分小车左右轮控制
+ self_driving.py用于控制小车任务执行流程

在self_driving.py中定义了9个状态，巡线、倒车入库和侧方停车任务分别对应状态1，状态2至5，状态6至10。巡线中主要采用预瞄点的比例控制算法，俯视图里在车辆前的某个距离计算与两条黄线交点的中点，并将其与车辆中线距离比较，由此控制左右轮的速度。

在状态1时检测后视图里标志牌的位置，满足一定条件时（图1）进入状态2，车辆开始倒车入库，向右后方倒车（图2）。

![img](https://github.com/WillianYe/Autonomous-driving-simulation/blob/main/img/img1.jpg)
![img](https://github.com/WillianYe/Autonomous-driving-simulation/blob/main/img/img2.jpg)

倒车时检测后视图里白线的位置，随着车辆运动白线向右偏移，满足一定条件时（图3）进入状态3，开始调用adjust_pose()函数调整位姿。该函数主要通过判断俯视图里上面的黄线是否平行（图4）来调整车轮速度，最终使黄线平行。

![img](https://github.com/WillianYe/Autonomous-driving-simulation/blob/main/img/img3.jpg)
![img](https://github.com/WillianYe/Autonomous-driving-simulation/blob/main/img/img4.jpg)

当俯视图里小车进入车位后，小车前的黄线到达指定位置后倒车入库成功（图5），小车直线开出来，进入状态4。小车前面的黄线到达一定位置后（图6），开始右转弯，进入状态5。小车右转后，根据后视图里标志牌位置判断，满足一定条件时（图7），回到状态1，重新进入巡线模式。

<img width="300" src="https://github.com/WillianYe/Autonomous-driving-simulation/blob/main/img/img5.jpg"/></div>
<img width="300" src="https://github.com/WillianYe/Autonomous-driving-simulation/blob/main/img/img6.jpg"/></div>
<img width="300" src="https://github.com/WillianYe/Autonomous-driving-simulation/blob/main/img/img7.jpg"/></div>

在状态1时检测后视图里标志牌的位置，满足一定条件时进入状态6，车辆开始侧方停车，先向右后方倒车（图8）。倒车到一定程度时，再次根据标志牌位置进入状态7（图9），车辆直线后退一段距离后进入状态8，从而使车辆更好地进入车位。

![img](https://github.com/WillianYe/Autonomous-driving-simulation/blob/main/img/img8.jpg)
![img](https://github.com/WillianYe/Autonomous-driving-simulation/blob/main/img/img9.jpg)

在状态8，车辆向左后方倒车，并调用adjust_pose2()函数，车前方的白线平行时视为侧方停车成功（图10），进入状态9。在状态9，车辆先向左前方行驶，调用change_state()函数，判断俯视图中指定的一片区域中是否有黄线，满足条件时（图11，图12）进入状态10，车辆直线行驶一段距离，以免撞到前方车位里的车辆。行驶后重新回到状态1巡线模式，车辆将自动摆正其位姿。

<img width="300" src="https://github.com/WillianYe/Autonomous-driving-simulation/blob/main/img/img10.jpg"/></div>
<img width="300" src="https://github.com/WillianYe/Autonomous-driving-simulation/blob/main/img/img11.jpg"/></div>
<img width="300" src="https://github.com/WillianYe/Autonomous-driving-simulation/blob/main/img/img12.jpg"/></div>
