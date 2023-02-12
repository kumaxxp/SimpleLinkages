#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Linkages_lib.FiveBarLinkage as FiveBarLinkage
import Linkages_lib.FourBarSubLinkage as FourBarSubLinkage
import Linkages_2d.linkage_2d_five as linkage_2d_five
import os
import cv2

import math

import numpy as np
from moviepy.editor import ImageSequenceClip
#from mpl_toolkits.mplot3d import Axes3D


def ellipse_xy(ct:float) -> tuple:
    a = 0.04
    b = 0.01
    
    r = -math.pi * (1/1000)*(ct+0) *5
    x = a * math.cos(r)
    y = b * math.sin(r) - 0.070

    return x,y

def link_machine():
    print("start five_bar_links")

    ct = 0

    cv_2dview = linkage_2d_five()

    five_bar = FiveBarLinkage((0.01007, -0.010), (-0.01007, -0.010), [0.015, 0.025, 0.03, 0.03])
    four_bar = FourBarSubLinkage(0.02, 0.050, 0.044, five_bar.l1)

    cv2.namedWindow('panel')
    cv2.createTrackbar('mode', 'panel', 1, 3, lambda x: None)
    cv2.createTrackbar('theta1', 'panel', 300, 360, lambda x: None)
    cv2.createTrackbar('theta2', 'panel', 200, 360, lambda x: None)
    cv2.createTrackbar('Ex', 'panel', 110, 200, lambda x: None)
    cv2.createTrackbar('Ey', 'panel', 50, 200, lambda x: None)

    while True:

        # モードの切替
        mode = cv2.getTrackbarPos('mode', 'panel')
        if mode == 0:   # 自動で逆運動で楕円に動く

            x,y = ellipse_xy(ct)

            four_bar.update_inverse_kinematics(x, y)
            #four_bar.update_inverse_kinematics(four_bar.E[0]-five_bar.B1[0], four_bar.E[1]-five_bar.B1[1])
            five_bar.update_inverse_kinematics(four_bar.theta1_m, four_bar.phi_m)

            five_bar.update_positions()
            four_bar.set_points(five_bar.B1, five_bar.M1, five_bar.X)
            four_bar.update_positions()

        elif mode == 1: # 手動で逆運動で操作

            x_offset = cv2.getTrackbarPos('Ex', 'panel')
            y_offset = cv2.getTrackbarPos('Ey', 'panel')
            x_in = 0.001 * (x_offset - 100)
            y_in = -0.001 * y_offset

            #print(x_in,y_in)

            #x_in,y_in = (0.004719464217149496, -0.10051644671340068)

            four_bar.update_inverse_kinematics(x_in, y_in)
            #four_bar.update_inverse_kinematics(four_bar.E[0]-five_bar.B1[0], four_bar.E[1]-five_bar.B1[1])
            five_bar.update_inverse_kinematics(four_bar.theta1_m, four_bar.phi_m)

            five_bar.update_positions()
            print(five_bar.B1, five_bar.M1, five_bar.X)
            four_bar.set_points(five_bar.B1, five_bar.M1, five_bar.X)
            four_bar.update_positions()

        elif mode == 2: # 手動で角度Φ/角度δを操作

            theta1 = cv2.getTrackbarPos('theta1', 'panel')
            theta2 = cv2.getTrackbarPos('theta2', 'panel')

            five_bar.set_theta(theta1, theta2)
            five_bar.update_positions()

            print(five_bar.B1, five_bar.M1, five_bar.X)
            four_bar.set_points(five_bar.B1, five_bar.M1, five_bar.X)
            four_bar.set_theta(theta1)
            four_bar.update_positions()

        
        cv_2dview.draw(five_bar, four_bar)

        if cv2.waitKey(1) == ord('q'):
            break

        ct = ct + 1

    cv2.destroyAllWindows()


if __name__ == '__main__':
    link_machine()
