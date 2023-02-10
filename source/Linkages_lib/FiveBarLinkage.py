#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import numpy as np
import time
from typing import List, Tuple

import Linkages_lib.CulcLinkage as lculc


#モータの短辺の長さ(m)
RECT_LEN:float = 0.020
MOTOR_DEF:float = 0.01986
MOTOR_GUIDE:float = 0.004

# 5節リンク（2点固定）を表すクラス
class FiveBarLinkage:
    def __init__(self, B1: Tuple[float, float], B2: Tuple[float, float], link_lengths: List[float]):
        self.B1: Tuple[float, float] = B1
        self.B2: Tuple[float, float] = B2

        self.M1: Tuple[float, float] = (0, 0)
        self.M2: Tuple[float, float] = (0, 0)

        self.X: Tuple[float, float] = (0, 0)

        self.l1, self.l2, self.m1, self.m2 = link_lengths 

        print(self.l1, self.l2, self.m1, self.m2)

    def update_positions(self):
        pass

    def calculate_coordinates(self, theta1: float, theta2:float):
        self.theta1:float = theta1
        self.theta2:float = theta2

        # Θ1=0のときの点M1の座標(l1,0)と
        # Θ2=0のときの点M2の座標(l2,0)
        self.M1_org: Tuple[float, float] = (self.B1[0] + self.l1, self.B1[1])
        self.M2_org: Tuple[float, float] = (self.B2[0] + self.l2, self.B2[1])

        # 任意の点を中心に回転させる座標を計算する
        self.T_B1 = lculc.culc_rotate_mat(self.B1, self.theta1)
        self.T_B2 = lculc.culc_rotate_mat(self.B2, self.theta2)

        # 回転処理
        transformed_point: np.ndarray = self.T_B1 @ np.matrix([self.M1_org[0], self.M1_org[1], 1]).T
        self.M1 = np.array(transformed_point[:2].T)[0]                

        transformed_point: np.ndarray = self.T_B2 @ np.matrix([self.M2_org[0], self.M2_org[1], 1]).T
        self.M2 = np.array(transformed_point[:2].T)[0]

        # M1,M2からリンクの交点Xを求める
        self.X = lculc.intersection_point(self.M1, self.m1, self.M2, self.m2, self.B1)

        #print(self.B1, self.B2, self.M1, self.M2, self.X )

    def set_theta(self, theta1: float, theta2: float):

        self.theta1:float = theta1
        self.theta2:float = theta2

        self.calculate_coordinates(theta1=theta1, theta2=theta2)

if __name__ == '__main__':

    point: Tuple[float, float] = (10, 20)
    center: Tuple[float, float] = (100, 200)
    angle: float = 30
    #rotated_point, transform_matrix = rotate(point, center, angle)

    five_bar_linkage = FiveBarLinkage( (-0.01007, -0.010), (0.01007, -0.010),[0.02, 0.02, 0.044, 0.044])

    five_bar_linkage.calculate_coordinates(60, 90)


