#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import numpy as np
import time

from typing import List, Tuple

import Linkages_lib.CulcLinkage as lculc

# 四節リンク(サブ)を表すクラス
class FourBarSubLinkage:
    def __init__(self, a: float, b: float, e: float, l1: float):
        self.a : float = a
        self.b : float = b
        self.c : float = a
        self.d : float = b
        self.e : float = e
        self.l1 : float = l1

        self.A : Tuple[float, float] = (0, 0)
        self.B : Tuple[float, float] = (0, 0)
        self.C : Tuple[float, float] = (0, 0)
        self.D : Tuple[float, float] = (0, 0)
        self.E : Tuple[float, float] = (0, 0)

        self.theta1 : float = 0.0

    def set_points(self, B1: Tuple[float, float], M1: Tuple[float, float], X: Tuple[float, float]):
        self.B1 = B1
        self.M1 = M1
        self.X  = X

        # M1->Xへの角度を計算して、行列式を作る
        rad = math.atan2(self.X[1] - self.M1[1], self.X[0] - self.M1[0])
        self.angle_AB = math.degrees(rad)



    def set_theta(self, theta1 : float):
        self.theta1 = theta1

    def update_positions(self):

        self.A_org: Tuple[float, float] = (self.B1[0] + self.l1, self.B1[1])
        self.D_org: Tuple[float, float] = (self.B1[0] + (self.l1 + self.a), self.B1[1])

        # theta1の回転行列
        self.T_B1 = lculc.culc_rotate_mat(self.B1, self.theta1)

        transformed_point: np.ndarray = self.T_B1 @ np.matrix([self.A_org[0], self.A_org[1], 1]).T
        self.A = np.array(transformed_point[:2].T)[0]                

        transformed_point: np.ndarray = self.T_B1 @ np.matrix([self.D_org[0], self.D_org[1], 1]).T
        self.D = np.array(transformed_point[:2].T)[0]                

        self.T_B = lculc.culc_rotate_mat(self.A, self.angle_AB)
        self.T_C = lculc.culc_rotate_mat(self.D, self.angle_AB)
        self.T_E = lculc.culc_rotate_mat(self.B, self.theta1)

        # 各点の座標を計算する
        self.B_org: Tuple[float, float] = (self.A[0] + self.b, self.A[1])
        self.C_org: Tuple[float, float] = (self.D[0] + self.b, self.D[1])
        self.E_org: Tuple[float, float] = (self.B[0] + (self.a + self.e), self.B[1])

        transformed_point: np.ndarray = self.T_B @ np.matrix([self.B_org[0], self.B_org[1], 1]).T
        self.B = np.array(transformed_point[:2].T)[0]                

        transformed_point: np.ndarray = self.T_C @ np.matrix([self.C_org[0], self.C_org[1], 1]).T
        self.C = np.array(transformed_point[:2].T)[0]                

        transformed_point: np.ndarray = self.T_E @ np.matrix([self.E_org[0], self.E_org[1], 1]).T
        self.E = np.array(transformed_point[:2].T)[0]                


    # A, B 二点の直線延長上に B から l の距離にある点を計算する
    def point_on_extension(self, A, B, l):
        A = np.array(A)
        B = np.array(B)
        AB = B - A
        AB_unit = AB / np.linalg.norm(AB)
        return B + l * AB_unit

    def point_on_extension_by_angle_AB(self, A, B, angle, l):
        AB = np.array(B) - np.array(A)
        AB = AB / np.linalg.norm(AB)
        R = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
        unit_vector = np.dot(AB, R)
        return B + l * unit_vector


if __name__ == '__main__':
    four_bar = FourBarSubLinkage(a=0.025313, b=0.04050137, e=0.025313, g=0.010, angle_phi=60, angle_delta=0)

    while True:
        x_in = 0.0
        y_in = -0.076

        four_bar.update_inverse_kinematics(x=x_in, y=y_in)
        four_bar.update_positions()
        four_bar.update_stand()

        time.sleep(0.1)
