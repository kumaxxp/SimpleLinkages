#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Linkages_lib.FiveBarLinkage as FiveBarLinkage
import Linkages_lib.FourBarSubLinkage as FourBarSubLinkage
import Linkages_2d.linkage_2d_five as linkage_2d_five
import Linkages_lib.CulcLinkage as lculc
import os
import cv2

import math

import numpy as np
from moviepy.editor import ImageSequenceClip
#from mpl_toolkits.mplot3d import Axes3D

def link_machine():
    print("start five_bar_links")

    cv_2dview = linkage_2d_five()

    diffM: float = 0.01

    B1: tuple(float,float) = (0.02010 , -diffM)
    B2: tuple(float,float) = (-(0.02010), -diffM)
    l1:float = 0.025
    l2:float = 0.025
    m1:float = 0.050
    m2:float = 0.035    #0.025

    a:float = 0.025
    b:float = 0.080
    e:float = 0.080

    five_bar = FiveBarLinkage(B1, B2, [l1, l2, m1, m2])
    four_bar = FourBarSubLinkage(B1, a, b, e, l1, m1)

    # モーター左上、右下
    MotorLT: tuple(float,float) = (-(diffM/2 + 0.02009),0.0195)
    MotorRB: tuple(float,float) = ((diffM/2 + 0.02009),-0.0205)

    cv2.namedWindow('panel')
    cv2.createTrackbar('mode', 'panel', 0, 3, lambda x: None)
    cv2.createTrackbar('theta1', 'panel', 300, 360, lambda x: None)
    cv2.createTrackbar('theta2', 'panel', 200, 360, lambda x: None)
    cv2.createTrackbar('x', 'panel', 104, 360, lambda x: None)
    cv2.createTrackbar('y', 'panel', 100, 360, lambda x: None)

    t:float = 0.0
 
    while True:

        mode = cv2.getTrackbarPos('mode', 'panel')
        if mode == 0:   # 自動で逆運動で楕円に動く
            x_in,y_in = lculc.culc_ellipse(t)
            t=t+1
            #print(x_in, y_in)

            four_bar.update_inverse_kinematics(x_in-five_bar.B1[0], y_in-five_bar.B1[1])
            if five_bar.update_inverse_kinematics(four_bar.X, four_bar.M1) == True:
                five_bar.set_theta(four_bar.phi2_m, five_bar.theta2i)
                five_bar.update_positions()

                cv_2dview.draw(five_bar, four_bar, MotorLT, MotorRB)

        elif mode == 1: # 手動で逆運動で操作
            x = cv2.getTrackbarPos('x', 'panel')
            y = cv2.getTrackbarPos('y', 'panel')
            x_in = 0.001 * (x - 100)
            y_in = -0.001 * y
           
            #x,y = 0.00471946, -0.10051645
            #print(x_in, y_in)

            try:
                four_bar.update_inverse_kinematics(x_in-five_bar.B1[0], y_in-five_bar.B1[1])
                if five_bar.update_inverse_kinematics(four_bar.X, four_bar.M1) == True:
                    five_bar.set_theta(four_bar.phi2_m, five_bar.theta2i)
                    five_bar.update_positions()

                    cv_2dview.draw(five_bar, four_bar, MotorLT, MotorRB)

            except ValueError as e:
                print(e)

        elif mode == 2: # 手動で角度Φ/角度δを操作
            theta1 = cv2.getTrackbarPos('theta1', 'panel')
            theta2 = cv2.getTrackbarPos('theta2', 'panel')

            five_bar.set_theta(theta1, theta2)
            five_bar.update_positions()

            four_bar.set_points(five_bar.M1, five_bar.X)
            four_bar.set_theta(theta1)
            four_bar.update_positions()

            cv_2dview.draw(five_bar, four_bar, MotorLT, MotorRB)

    #    cv_2dview.draw(five_bar, four_bar)

        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    link_machine()
