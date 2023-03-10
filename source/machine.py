#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Linkages_lib.FourBarLinkage as FourBarLinkage
import Linkages_2d.linkage_2d as linkage_2d
import os
import cv2

import math

import numpy as np
from moviepy.editor import ImageSequenceClip
#from mpl_toolkits.mplot3d import Axes3D

def link_machine():
    print("start four_bar_links")

    cv_2dview = linkage_2d()

    # リンクの長さ比
    # a : b : e = 100 : 160 : 100
    # f : g = 113.13 : 50
    # Z平面の位置
#    four_bar = FourBarLinkage(a=0.025313, b=0.04050137, e=0.025313, g=0.010, j=0.04, k=0.036, angle_phi=60, angle_delta=0)
#    four_bar = FourBarLinkage(a=0.025313, b=0.04050137, e=0.025313, g=0.010, j=0.025313, k=0.025313, angle_phi=60, angle_delta=0)
    four_bar = FourBarLinkage(a=0.025313, b=0.08, g=0.010, j=0.025313, k=0.01, angle_phi=60, angle_delta=0)
    four_bar.update_positions()

    four_bar2 = FourBarLinkage(a=0.025313, b=0.04050137, g=0.010, j=0.04, k=0.036, angle_phi=60, angle_delta=0, offset = 300)
    four_bar2.update_positions()

    cv2.namedWindow('panel')
    cv2.createTrackbar('mode', 'panel', 1, 3, lambda x: None)
    cv2.createTrackbar('phi', 'panel', 90, 360, lambda x: None)
    cv2.createTrackbar('delta', 'panel', 210, 360, lambda x: None)
    cv2.createTrackbar('gamma', 'panel', 120, 360, lambda x: None)
    cv2.createTrackbar('epsilon', 'panel', 120, 360, lambda x: None)
    cv2.createTrackbar('Ex', 'panel', 100, 200, lambda x: None)
    cv2.createTrackbar('Ey', 'panel', 79, 100, lambda x: None)

    while True:

        # 角度変更
        x_offset = cv2.getTrackbarPos('Ex', 'panel')
        y_offset = cv2.getTrackbarPos('Ey', 'panel')
        x_in = 0.001 * (x_offset - 100)
        y_in = -0.001 * y_offset

        # モードの切替
        mode = cv2.getTrackbarPos('mode', 'panel')
        if mode == 0:   # 自動で逆運動で楕円に動く
            four_bar.update_inverse_kinematics(x=four_bar.pos_ellipse[0] , y=four_bar.pos_ellipse[1] )
            four_bar.culc_ellipse()

            four_bar2.update_inverse_kinematics(x=four_bar2.pos_ellipse[0] , y=four_bar2.pos_ellipse[1] )
            four_bar2.culc_ellipse()

            # print(four_bar2.pos_ellipse[0], four_bar2.pos_ellipse[1])

        elif mode == 1: # 手動で逆運動で操作
            four_bar.update_inverse_kinematics(x=x_in, y=y_in)

        elif mode == 2: # 手動で角度Φ/角度δを操作
            phi = cv2.getTrackbarPos('phi', 'panel')
            delta = cv2.getTrackbarPos('delta', 'panel')
            four_bar.set_phi(phi)
            four_bar.set_delta(delta)

        elif mode == 3: # 手動で角度γ/角度δを操作（駆動軸で位置決定する）
            gamma = cv2.getTrackbarPos('gamma', 'panel')
            delta = cv2.getTrackbarPos('delta', 'panel')
            epsilon = cv2.getTrackbarPos('epsilon', 'panel')
            phi = gamma - (delta-180)
            four_bar.set_phi(phi)
            four_bar.set_delta(delta)
            four_bar.set_epsilon(epsilon)

        four_bar.update_positions()
        #four_bar.update_stand()
        four_bar.update_gravity()
        
        four_bar2.update_stand()

        #cv_2dview.draw(four_bar, four_bar2)
        cv_2dview.draw(four_bar, None)

        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    link_machine()
