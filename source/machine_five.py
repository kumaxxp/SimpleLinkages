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

def link_machine():
    print("start five_bar_links")

    cv_2dview = linkage_2d_five()

    five_bar = FiveBarLinkage((0.01007, -0.010), (-0.01007, -0.010), [0.015, 0.025, 0.03, 0.03])
    four_bar = FourBarSubLinkage(0.02, 0.050, 0.044, five_bar.l1)

    cv2.namedWindow('panel')
    cv2.createTrackbar('mode', 'panel', 1, 3, lambda x: None)
    cv2.createTrackbar('theta1', 'panel', 300, 360, lambda x: None)
    cv2.createTrackbar('theta2', 'panel', 200, 360, lambda x: None)

    while True:

        theta1 = cv2.getTrackbarPos('theta1', 'panel')
        theta2 = cv2.getTrackbarPos('theta2', 'panel')

        five_bar.set_theta(theta1, theta2)
        five_bar.update_positions()

        four_bar.set_points(five_bar.B1, five_bar.M1, five_bar.X)
        four_bar.set_theta(theta1)
        four_bar.update_positions()
        
        cv_2dview.draw(five_bar, four_bar)

        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    link_machine()
