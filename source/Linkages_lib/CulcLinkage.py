#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import numpy as np
import time

from typing import List, Tuple


# 任意の点centerを中心に点を回転させる
def rotate(point: Tuple[float, float], center: Tuple[float, float], angle: float) -> Tuple[Tuple[float, float], np.ndarray]:
    angle = np.deg2rad(angle)
    rotation_matrix: np.ndarray = np.matrix([[np.cos(angle), -np.sin(angle), 0],
                                            [np.sin(angle), np.cos(angle), 0],
                                            [0, 0, 1]])
    translate_matrix: np.ndarray = np.matrix([[1, 0, -center[0]],
                                              [0, 1, -center[1]],
                                              [0, 0, 1]])
    translate_back_matrix: np.ndarray = np.matrix([[1, 0, center[0]],
                                                   [0, 1, center[1]],
                                                   [0, 0, 1]])
    transform_matrix: np.ndarray = translate_back_matrix @ rotation_matrix @ translate_matrix
    transformed_point: np.ndarray = transform_matrix @ np.matrix([point[0], point[1], 1]).T
    return np.array(transformed_point[:2].T)[0], transform_matrix

# 任意の点centerを中心に点を回転させる行列を計算する
def culc_rotate_mat(center: Tuple[float, float], angle: float) -> np.ndarray:
    rad:float = np.deg2rad(angle)
    rotation_matrix: np.ndarray = np.matrix([[np.cos(rad), -np.sin(rad), 0],
                                            [np.sin(rad), np.cos(rad), 0],
                                            [0, 0, 1]])
    translate_matrix: np.ndarray = np.matrix([[1, 0, -center[0]],
                                              [0, 1, -center[1]],
                                              [0, 0, 1]])
    translate_back_matrix: np.ndarray = np.matrix([[1, 0, center[0]],
                                                   [0, 1, center[1]],
                                                   [0, 0, 1]])
    transform_matrix: np.ndarray = translate_back_matrix @ rotation_matrix @ translate_matrix

    return transform_matrix


# 円同士の距離を計算し、基準点から遠い方を選択する
def intersection_point(c1: tuple, r1: float, c2: tuple, r2: float, point: tuple):
    if not all(map(lambda x: isinstance(x, (int, float)), c1+c2+point)):
        raise TypeError("c1, c2 and point must be tuple of int or float")
    if not all(map(lambda x: isinstance(x, (int, float)), (r1, r2))):
        raise TypeError("r1, r2 must be int or float")

    x1, y1 = c1
    x2, y2 = c2
    d = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    if d > r1 + r2 or d < abs(r1 - r2):
        return None # no intersection
    else:
        a = (r1**2 - r2**2 + d**2) / (2 * d)
        h = math.sqrt(r1**2 - a**2)
        xm = x1 + a * (x2 - x1) / d
        ym = y1 + a * (y2 - y1) / d
        xs1 = xm + h * (y2 - y1) / d
        xs2 = xm - h * (y2 - y1) / d
        ys1 = ym - h * (x2 - x1) / d
        ys2 = ym + h * (x2 - x1) / d
        distance1 = math.sqrt((xs1 - point[0])**2 + (ys1 - point[1])**2)
        distance2 = math.sqrt((xs2 - point[0])**2 + (ys2 - point[1])**2)
        if ys2 > ys1:
            return xs1, ys1
        else:
            return xs2, ys2

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


# 原点ピンを中心に、リンクを回転させて、次のピンの位置を計算する
def culc_next_point(O:Tuple[float,float], l:float, delta: float) -> Tuple[float,float]:
    # O:原点ピンの位置
    # l:リンクの長さ
    # delta:原点ピンを中心にリンクを回転させる角度

    # 点Pの角度0度の座標
    P_org: Tuple[float, float] = (O[0] + l, O[1])

    #print('culc', O, l, delta)

    # theta1の回転行列
    T_O = culc_rotate_mat(O, delta)
    transformed_point: np.ndarray = T_O @ np.matrix([P_org[0], P_org[1], 1]).T
    P = np.array(transformed_point[:2].T)[0]
    #print('culd', P)

    return P


# 精度の高い逆運動学の計算を行う
def improved_function(x: float, y: float, l1: float, l2: float) -> Tuple[float, float, float, float]:

    # Θ1を計算
    numerator = np.square(x) + np.square(y) + np.square(l1) - np.square(l2)
    denominator = 2 * l1 * np.sqrt(np.square(x) + np.square(y))

    denominator = abs(denominator)

    if denominator == 0:
        delta_rad = np.pi/2
    else:
        delta_rad = np.arccos(numerator / denominator)
        
    a_tan_rad = np.arctan2(y,x)

    theta_rad = a_tan_rad + delta_rad
    theta_rad_m = a_tan_rad - delta_rad

    theta1_p = np.degrees(theta_rad)
    theta1_m = np.degrees(theta_rad_m)

    # Θ2を計算    
    numerator   = y - l1*np.sin(theta_rad)
    denominator = abs(x - l1*np.cos(theta_rad))
    theta2_rad = np.arctan(numerator / denominator)
    theta2_p = np.degrees(theta2_rad)

    numerator   = y - l1*np.sin(theta_rad_m)
    denominator = abs(x - l1*np.cos(theta_rad_m))
    theta2_rad = np.arctan(numerator / denominator)
    theta2_m = np.degrees(theta2_rad)

    #print(numerator,denominator,l1)

    if(numerator == np.nan or denominator == np.nan):
        return None,None,None,None

    return theta1_p, theta1_m, theta2_p, theta2_m

# 楕円軌道を作る。カウンタは外から入れる。
def culc_ellipse(t:float) -> tuple:

        a = 0.045
        b = 0.020
        
        r = -math.pi * (1/1000)*(t) *5
        x = a * math.cos(r) + 0.00
        y = b * math.sin(r) - 0.16  # 0.12

        return x,y

import numpy as np

class Linkage:
    def __init__(self, l1, l2, l3, l4):
        self.link_lengths = np.array([l1, l2, l3, l4])

    def calculate_positions(self, theta1, theta4):
        theta1_rad = np.radians(theta1)
        theta4_rad = np.radians(180 - theta4)

        rot_matrix1 = self.get_rot_matrix(theta1_rad)
        rot_matrix4 = self.get_rot_matrix(theta4_rad)

        p1 = np.dot(rot_matrix1, [self.link_lengths[0], 0])
        p5 = np.dot(rot_matrix4, [-self.link_lengths[3], 0]) + [self.link_lengths[1], 0]

        p3_conn_vec = self.link_lengths[2] * (p5 - p1) / np.linalg.norm(p5 - p1)
        p2_conn_vec = (self.link_lengths[1] ** 2 - self.link_lengths[2] ** 2 + np.linalg.norm(p5 - p1) ** 2) / (2 * np.linalg.norm(p5 - p1)) * (p5 - p1) / np.linalg.norm(p5 - p1)

        rot_theta2 = np.arccos((self.link_lengths[1] ** 2 + np.linalg.norm(p5 - p1) ** 2 - self.link_lengths[2] ** 2) / (2 * self.link_lengths[1] * np.linalg.norm(p5 - p1))) - np.arctan2((p5 - p1)[1], (p5 - p1)[0]) + np.arctan2(p1[1], p1[0])

        rot_matrix2 = self.get_rot_matrix(rot_theta2)

        p2 = np.dot(rot_matrix2, [self.link_lengths[1], 0])
        p3 = p1 + p3_conn_vec

        return p1, p2, p3, p5

    def get_rot_matrix(self, theta):
        return np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])




if __name__ == '__main__':

    # X,Y =  (0.004719464217149496 -0.10051644671340068) - (0.01007, -0.010)
    # a,b,e,l1 = 0.02, 0.050, 0.044, 0.015
    # (l1 ,l2) = (b, a+e+l1) = (0.05, 0.079)
    # -36.69498038837119 63.400837262331414 -137.92864690663993 -58.02446455734254
    theta1_p, theta1_m, theta2_p, theta2_m = improved_function(0.004719464217149496-0.01007, -0.10051644671340068+0.010, 0.05, 0.079)

    print(theta1_p, theta2_p, theta1_m, theta2_m)

    # 原点を考慮するの忘れてないか？
    # Eからの逆算は、B1を引く必要がある。

    # Genie
    # 使用例
    linkage = Linkage(1, 2, 3, 4)
    p1, p2, p3, p5 = linkage.calculate_positions(30, 120)

    print("P1:", p1)
    print("P2:", p2)
    print("P3:", p3)
    print("P5:", p5)

