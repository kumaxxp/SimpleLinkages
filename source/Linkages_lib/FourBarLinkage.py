#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import numpy as np

#モータの短辺の長さ(m)
RECT_LEN:float = 0.020
MOTOR_DEF:float = 0.01986
MOTOR_GUIDE:float = 0.004

# 四節リンクを表すクラス
class FourBarLinkage:
    def __init__(self, a, b, e, g, angle_phi, angle_delta, offset = 0):
        self.a : float = a
        self.b : float = b
        self.c : float = a
        self.d : float = b
        self.e : float = e

        self.f : float = math.sqrt((MOTOR_DEF ** 2) + (MOTOR_DEF + MOTOR_GUIDE)**2)    # 113.13
        self.g : float = g

        self.offset : float = offset

        self.t = 0
        self.pos_ellipse = (100, 100)

        self.angle_phi = angle_phi
        self.angle_delta = angle_delta
        self.angle_gamma = self.angle_phi + self.angle_delta

        self.phi = math.radians(angle_phi)
        self.delta = math.radians(angle_delta)
        self.gamma = math.radians(self.angle_gamma)
        self.phi_delta = math.radians(angle_phi + angle_delta)

        self.angle_alpha = 0.0
        self.alpha = 0.0

        # 各点の座標を表す変数を定義する
        self.D = (0, 0)
        self.A = (a * math.cos(self.delta), a * math.sin(self.delta))
        self.B = (a * math.cos(self.delta) + b * math.cos(self.phi_delta), 
                a * math.sin(self.delta) + b * math.sin(self.phi_delta))
        self.C = (b * math.cos(self.phi) * math.cos(self.delta) - b * math.sin(self.phi) * math.sin(self.delta),
                b * math.cos(self.phi) * math.sin(self.delta) + b * math.sin(self.phi) * math.cos(self.delta))

        self.E = (a * math.cos(self.delta) + (b + e) * math.cos(self.phi_delta),
                a * math.sin(self.delta) + (b + e) * math.sin(self.phi_delta))


        #self.F = (self.D[0] + self.f * math.cos(self.delta), self.D[1] + self.f * math.sin(self.delta))
        self.F = (self.D[0] + MOTOR_DEF, self.D[1] + MOTOR_DEF + MOTOR_GUIDE)
        self.G = (self.F[0] + self.g * math.cos(self.gamma), self.F[1] + self.g * math.sin(self.gamma))
        self.H = (self.D[0] + self.g * math.cos(self.gamma), self.D[1] + self.g * math.sin(self.gamma))

        # 各点の角度を表す変数を定義する
        self.angle_A = 180 - angle_phi
        self.angle_B = angle_phi
        self.angle_C = 180 - angle_phi
        self.angle_phi  = angle_phi

        self.angle_phi1 = 0
        self.angle_phi2 = 0

        self.L = math.sqrt((self.E[0] - self.E[0])**2 + (self.E[1] - self.E[1])**2)

        self.update_positions()


    def update_positions(self):

        # 各点の座標を計算する
        self.phi_delta = math.radians(self.angle_phi + self.angle_delta)
        self.angle_gamma = self.angle_phi + self.angle_delta - 180
        self.gamma = math.radians(self.angle_gamma)

        # 各点の座標を表す変数を定義する
        self.D = (0, 0)
        self.A = (self.a * math.cos(self.delta), self.a * math.sin(self.delta))
        self.B = (self.a * math.cos(self.delta) + self.b * math.cos(self.phi_delta), 
                self.a * math.sin(self.delta) + self.b * math.sin(self.phi_delta))
        self.C = (self.b * math.cos(self.phi) * math.cos(self.delta) - self.b * math.sin(self.phi) * math.sin(self.delta),
                self.b * math.cos(self.phi) * math.sin(self.delta) + self.b * math.sin(self.phi) * math.cos(self.delta))

        self.E = (self.a * math.cos(self.delta) + (self.b + self.e) * math.cos(self.phi_delta),
                self.a * math.sin(self.delta) + (self.b + self.e) * math.sin(self.phi_delta))

        self.L = math.sqrt((self.E[0] - self.E[0])**2 + (self.E[1] - self.E[1])**2)

        self.G = (self.F[0] + self.g * math.cos(self.gamma), self.F[1] + self.g * math.sin(self.gamma))
        self.H = (self.D[0] + self.g * math.cos(self.gamma), self.D[1] + self.g * math.sin(self.gamma))

        self.I = ((self.F[0] - self.D[0]) /2 ,(self.F[1] - self.D[1]) /2) 

        # 各点の角度を表す変数を定義する
        self.angle_A = 180 - self.angle_phi
        self.angle_B = self.angle_phi
        self.angle_C = 180 - self.angle_phi
        self.angle_phi  = self.angle_phi

        # 各点の図上の角度を表す変数を定義する
        self.angle_D_st = 0 + self.angle_delta
        self.angle_D_ed = self.angle_D_st + self.angle_phi

        self.angle_A_st = self.angle_phi + self.angle_delta
        self.angle_A_ed = self.angle_A_st + self.angle_A

        self.angle_B_st = self.angle_A_ed
        self.angle_B_ed = self.angle_B_st + self.angle_B

        self.angle_C_st = self.angle_B_ed
        self.angle_C_ed = self.angle_C_st + self.angle_C

    def update_inverse_kinematics(self, x: float, y: float):
        data:float
        a_cos:float
        a_tan:float

        # δを計算
        data = (x ** 2 + y ** 2 + self.a ** 2 - (self.b + self.e) ** 2) / (2 * self.a * math.sqrt(x**2 + y**2))
        if data > 1 or data < -1:
            return

        a_cos = math.acos(data)
        a_tan = math.atan2(y,x)

        # マイナス側を採用
        delta_p =  a_cos + a_tan
        delta_m = -a_cos + a_tan

        self.set_delta(math.degrees(delta_m))

        # Φを計算
        a_tan_phi:float
        a_tan_phi = math.atan2((y - self.a * math.sin(self.delta)) , (x - self.a * math.cos(self.delta)))
        angle_phi = math.degrees(a_tan_phi) - self.angle_delta

        self.set_phi(angle_phi)


    def set_phi(self, angle):
        # Φの角度は頂点Dの角度として保存する
        self.angle_phi = angle
        self.phi = math.radians(angle)

        self.update_positions()

    def set_delta(self, angle):
        # Δの角度は全体の角度として保存する
        self.angle_delta = angle
        self.delta = math.radians(angle)

        self.update_positions()

    def culc_ellipse(self):
        self.pos_ellipse = self.ellipse_xy(self.t)
        self.t += 1

    def ellipse_xy(self, t:float) -> tuple:
        a = 0.04
        b = 0.01
        
        r = -math.pi * (1/1000)*(t+self.offset) *5
        x = a * math.cos(r)
        y = b * math.sin(r) - 0.070

        return x,y

    def update_gravity(self):
        x : float = self.E[0] - self.I[0]
        y : float = self.E[1] - self.I[1]
        self.alpha = math.atan2(y, x)
        self.angle_alpha = math.degrees(self.alpha)

        angle_def = -(self.angle_alpha - (-90.0))
        print(angle_def)
        d_rad = math.radians(angle_def)

        # D(0, 0) を中心に固定し、
        # DEの角度を算出
        # DEの角度を-90度になるようにポイントを座標変換する

        self.rA = self.rotation(d_rad, self.I[0], self.I[1], self.A[0], self.A[1])
        self.rB = self.rotation(d_rad, self.I[0], self.I[1], self.B[0], self.B[1])
        self.rC = self.rotation(d_rad, self.I[0], self.I[1], self.C[0], self.C[1])
        self.rD = self.rotation(d_rad, self.I[0], self.I[1], self.D[0], self.D[1])
        self.rE = self.rotation(d_rad, self.I[0], self.I[1], self.E[0], self.E[1])
        self.rF = self.rotation(d_rad, self.I[0], self.I[1], self.F[0], self.F[1])
        self.rG = self.rotation(d_rad, self.I[0], self.I[1], self.G[0], self.G[1])
        self.rH = self.rotation(d_rad, self.I[0], self.I[1], self.H[0], self.H[1])
        self.rI = self.rotation(d_rad, self.I[0], self.I[1], self.I[0], self.I[1])

        std_x  = self.rE[0]
        std_y  = self.rE[1]

        self.rA = self.shift_point(std_x, std_y, self.rA[0], self.rA[1])
        self.rB = self.shift_point(std_x, std_y, self.rB[0], self.rB[1])
        self.rC = self.shift_point(std_x, std_y, self.rC[0], self.rC[1])
        self.rD = self.shift_point(std_x, std_y, self.rD[0], self.rD[1])
        self.rE = self.shift_point(std_x, std_y, self.rE[0], self.rE[1])
        self.rF = self.shift_point(std_x, std_y, self.rF[0], self.rF[1])
        self.rG = self.shift_point(std_x, std_y, self.rG[0], self.rG[1])
        self.rH = self.shift_point(std_x, std_y, self.rH[0], self.rH[1])
        self.rI = self.shift_point(std_x, std_y, self.rI[0], self.rI[1])


    def rotation(self, d_rad:float, Cx:float, Cy:float, x:float, y:float):
        # ラジアンで角度を指定してポイントを回転する

        rot = np.array([[np.cos(d_rad), -np.sin(d_rad), Cx - Cx * np.cos(d_rad)+Cy*np.sin(d_rad)],
                        [np.sin(d_rad), np.cos(d_rad), Cy-Cx * np.sin(d_rad)-Cy*np.cos(d_rad)],
                        [0, 0, 1]])

        #print(rot)

        return np.dot(rot, (x, y, 1))

    def shift_point(self, Cx:float, Cy:float, x:float, y:float, offset_y:float = -0.08):
        # 基準位置を指定して、ポイントをオフセットする
        Sx = x - Cx
        Sy = y - Cy + offset_y

        return Sx, Sy

