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
        self.phi : float = 0.0


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

    def update_inverse_kinematics_debug(self, x: float, y: float):
        l = self.l1 + self.a + self.e
        theta1_p, theta1_m, theta2_p, theta2_m = lculc.improved_function(x, y, self.b, l)

        self.theta1 = theta1_p
        self.phi = theta2_p

        self.theta1_m = theta1_m
        self.phi_m = theta2_m

        #print(x, y, self.theta1, self.phi,self.theta1_m, self.phi_m)

        # 点M1 または、点Aを計算する
        B1_org: Tuple[float, float] = (self.B1[0] + self.b, self.B1[1])

        # theta1の回転行列
        #T_B1 = lculc.culc_rotate_mat(self.B1, self.theta1)
        T_B1 = lculc.culc_rotate_mat(self.B1, self.theta1)
        transformed_point: np.ndarray = T_B1 @ np.matrix([B1_org[0], B1_org[1], 1]).T
        self.Gi = np.array(transformed_point[:2].T)[0]                
        
        # 点Gをもとに点Eの基準点を計算する
        E_org: Tuple[float, float] = (self.Gi[0] + l, self.Gi[1])

        T_G = lculc.culc_rotate_mat(self.Gi, self.phi)
        transformed_point: np.ndarray = T_G @ np.matrix([E_org[0], E_org[1], 1]).T
        self.Ei = np.array(transformed_point[:2].T)[0]

        # theta1_mの回転行列
        T_B1_m = lculc.culc_rotate_mat(self.B1, self.theta1_m)
        transformed_point: np.ndarray = T_B1_m @ np.matrix([B1_org[0], B1_org[1], 1]).T
        self.Gim = np.array(transformed_point[:2].T)[0]                

        # 点Gmをもとに点Emの基準点を計算する
        Em_org: Tuple[float, float] = (self.Gim[0] + l, self.Gim[1])

        T_G_m = lculc.culc_rotate_mat(self.Gim, self.phi_m)
        transformed_point: np.ndarray = T_G_m @ np.matrix([Em_org[0], Em_org[1], 1]).T
        self.Eim = np.array(transformed_point[:2].T)[0]

    def update_inverse_kinematics(self, x: float, y: float):
        l = self.l1 + self.a + self.e
        theta1_p, theta1_m, theta2_p, theta2_m = lculc.improved_function(x, y, self.b, l)

        self.theta1_p = theta1_p
        self.phi_p = theta2_p

        self.theta1_m = theta1_m
        self.phi_m = theta2_m

        #print(x, y, self.theta1, self.phi,self.theta1_m, self.phi_m)


if __name__ == '__main__':
    four_bar = FourBarSubLinkage(a=0.025313, b=0.04050137, e=0.025313, g=0.010, angle_phi=60, angle_delta=0)

    while True:
        x_in = 0.0
        y_in = -0.076

        four_bar.update_inverse_kinematics(x=x_in, y=y_in)
        four_bar.update_positions()
        four_bar.update_stand()

        time.sleep(0.1)
