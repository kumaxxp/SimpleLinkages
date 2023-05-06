#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import numpy as np

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import pygame
import sys

from leg import Leg

class Robot:
    def __init__(self):
        self.screen_width, self.screen_height = 1000, 800
        self.scale_factor = 4000

        self.linkage5bar_params = {
            'b': 0.020,
            'l1': 0.015,
            'l2': 0.025,
            'm1': 0.040,
            'm2': 0.025
        }

        self.linkage4bar_params = {
            'a': 0.020,
            'b': 0.050,
            'e': 0.040
        }

        self.link_list = {
            ('A', 'B'),
            ('B', 'C'),
            ('C', 'D'),
            ('D', 'A'),
            ('C', 'E'),
            ('B1', 'B2'),
            ('B1', 'M1'),
            ('B2', 'M2'),
            ('M2', 'X'),
            ('M1', 'X')
        }

        theta_1 = math.radians(-45)
        theta_2 = math.radians(-115)

        self.leg = Leg(self.linkage5bar_params, self.linkage4bar_params)
        endeffector_position = self.leg.compute_endeffector_position(theta_1, theta_2)

    def convert_coordinates(self, coord, screen_width, screen_height):
        x, y = coord
        x_transformed = int((x * self.scale_factor) + screen_width // 2)
        y_transformed = int((-y * self.scale_factor) + screen_height // 2)
        return x_transformed, y_transformed
    
    def convert_length(self, len):
        transformed = int(len * self.scale_factor)
        return transformed

    def create_links_2D(self, links, coordinates):
        link_coordinates = []
        for vertex1, vertex2 in links:
            if vertex1 in coordinates and vertex2 in coordinates:
                coord1 = coordinates[vertex1]
                coord2 = coordinates[vertex2]
                link_coordinates.append((coord1, coord2))
        return link_coordinates

    # 座標からリンクのリストを作成する。三次元に拡張する
    def create_links(self, links, coordinates, t):
        link_coordinates = []
        for vertex1, vertex2 in links:
            if vertex1 in coordinates and vertex2 in coordinates:
                coord1 = coordinates[vertex1][0], coordinates[vertex1][1], t
                coord2 = coordinates[vertex2][0], coordinates[vertex2][1], t
                link_coordinates.append((coord1, coord2))
        return link_coordinates

if __name__ == "__main__":
    # ロボットの初期化
    robot = Robot()

    # このフラグをTrueにすると3D表示になり、Falseにすると2D表示になります
    use_3d_view = True

    # 画面設定
    if use_3d_view:
        # OpenGL Utility Toolkit(GLUT)の初期化
        glutInit(sys.argv)
        # Pygame 初期化
        pygame.init()
        
        screen = pygame.display.set_mode((robot.screen_width, robot.screen_height), pygame.DOUBLEBUF | pygame.OPENGL)
        robot.init_3d_view()  # 3Dビューの初期化をメソッドで行う
    else:
        # Pygame 初期化
        pygame.init()

        screen = pygame.display.set_mode((robot.screen_width, robot.screen_height))

    # 初期設定の追加
    font = pygame.font.Font(None, 24)

    # 描画ループ
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        if use_3d_view:
            robot.display_gl(screen)

        else:
            robot.draw_2d(screen, font)  # この関数を呼び出すだけで2D表示が可能になります            

    # Pygame 終了
    pygame.quit()
    sys.exit()

