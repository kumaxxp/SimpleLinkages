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
