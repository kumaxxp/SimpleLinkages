#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import numpy as np

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

        self.leg = Leg(self.linkage5bar_params, self.linkage4bar_params)

    def convert_coordinates(self, coord):
        x, y = coord
        x_transformed = int((x * self.scale_factor) + self.screen_width // 2)
        y_transformed = int((-y * self.scale_factor) + self.screen_height // 2)
        return x_transformed, y_transformed
    
    def convert_length(self, len):
        transformed = int(len * self.scale_factor)
        return transformed

    def create_links(self, links, coordinates):
        link_coordinates = []
        for vertex1, vertex2 in links:
            if vertex1 in coordinates and vertex2 in coordinates:
                coord1 = coordinates[vertex1]
                coord2 = coordinates[vertex2]
                link_coordinates.append((coord1, coord2))
        return link_coordinates

    def draw_2d(self, screen, font, theta_1, theta_2):
        endeffector_position = self.leg.compute_endeffector_position(theta_1, theta_2)
        positions = self.leg.get_positions()

        transformed_coordinates = {key: self.convert_coordinates(coord) for key, coord in positions.items()}

        links_coordinates = self.create_links(self.link_list, transformed_coordinates)

        # ここから、pygameを使った2D表示を行います
        screen.fill((0, 0, 0))
        origin = np.array([self.screen_width // 2, self.screen_height // 2])

        # X=0, Y=0 の線を引く
        pygame.draw.line(screen, (128, 128, 128), (0, origin[1]), (self.screen_width, origin[1]), 3)
        pygame.draw.line(screen, (128, 128, 128), (origin[0], 0), (origin[0], self.screen_height), 3)

        # 座標軸の目盛りとラベルを描画
        marker_length = 0.02
        text_offset = 15
        scaled_step = int(self.convert_length(marker_length))

        for coord_val in range(0, self.screen_height//2, scaled_step):
            # X 軸
            pygame.draw.line(screen, (128, 128, 128), (0, origin[1] + coord_val), (self.screen_width, origin[1] + coord_val))
            pygame.draw.line(screen, (128, 128, 128), (0, origin[1] - coord_val), (self.screen_width, origin[1] - coord_val))

        for coord_val in range(0, self.screen_width//2, scaled_step):
            # Y 軸
            pygame.draw.line(screen, (128, 128, 128), (origin[0] + coord_val, 0), (origin[0] + coord_val, self.screen_height))
            pygame.draw.line(screen, (128, 128, 128), (origin[0] - coord_val, 0), (origin[0] - coord_val, self.screen_height))

        # 各頂点やリンクの描画は以下の部分で実装されています

        # 頂点を描画
        for vertex_name, coord in transformed_coordinates.items():

            pygame.draw.circle(screen, (255, 0, 0), coord, 5)
            
            if(vertex_name != 'A'):
                original_coord_mm = (positions[vertex_name][0] * 1000, positions[vertex_name][1] * 1000)
                label_text = f"{vertex_name} ({original_coord_mm[0]:.2f}, {original_coord_mm[1]:.2f})"
                label = font.render(label_text, True, (255, 255, 255))
                screen.blit(label, (coord[0] + 10, coord[1] - 10))

        # リンクを描画
        for link in links_coordinates:
            pygame.draw.line(screen, (0, 255, 0), link[0], link[1], 2)

if __name__ == "__main__":

    robot = Robot()

    theta_1 = math.radians(-45)
    theta_2 = math.radians(-115)

    # Pygame 初期化
    pygame.init()

    # 画面設定
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

        robot.draw_2d(screen, font, theta_1, theta_2)  # この関数を呼び出すだけで2D表示が可能になります

        pygame.display.flip()

    # Pygame 終了
    pygame.quit()
    sys.exit()