#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import numpy as np

import pygame
import sys

from leg import Leg

# 画面サイズ
screen_width, screen_height = 1000, 800

# 座標を拡大する係数
scale_factor = 4000

# 座標を変換する関数（原点を画面中央に移動し、拡大）
def convert_coordinates(coord):
    x, y = coord
    x_transformed = int((x * scale_factor) + screen_width // 2)
    y_transformed = int((-y * scale_factor) + screen_height // 2)
    return x_transformed, y_transformed

# 座標からリンクのリストを作成する
def create_links(links, coordinates):
    link_coordinates = []
    for vertex1, vertex2 in links:
        if vertex1 in coordinates and vertex2 in coordinates:
            coord1 = coordinates[vertex1]
            coord2 = coordinates[vertex2]
            link_coordinates.append((coord1, coord2))
    return link_coordinates

if __name__ == "__main__":

    linkage5bar_params = {
        'b': 0.020,
        'l1': 0.015,
        'l2': 0.025,
        'm1': 0.040,
        'm2': 0.025
    }

    linkage4bar_params = {
        'a': 0.020,
        'b': 0.050,
        'e': 0.040
    }

    leg = Leg(linkage5bar_params, linkage4bar_params)
    theta_1 = math.radians(-45)
    theta_2 = math.radians(-115)

    endeffector_position = leg.compute_endeffector_position(theta_1, theta_2)
    print("エンドエフェクタの位置:", endeffector_position)

    positions = leg.get_positions()

    print(positions)


    # Pygame 初期化
    pygame.init()

    # 画面設定
    screen = pygame.display.set_mode((screen_width, screen_height))

    # 色の定義
    vertex_color = (255, 0, 0)
    link_color = (0, 255, 0)

    # 初期設定の追加
    font = pygame.font.Font(None, 24)  # フォントオブジェクトの生成（デフォルトフォント、サイズ24）
    origin = (screen_width // 2, screen_height // 2)  # 画面の中心を原点座標とします。

    # 辞書内の座標を変換
    transformed_coordinates = {key: convert_coordinates(coord) for key, coord in positions.items()}

    # リンクのリスト
    link_list = {
        ('A', 'B'),
        ('B', 'C'),
        ('C', 'D'),
        ('D', 'A'),
        ('C', 'E'),
        ('B1', 'B2'),
        ('B1', 'M1'),
        ('B2', 'M2'),
        ('M2', 'X'),
        ('M1', 'X')}

    # 座標からリンクのリストを生成
    links_coordinates = create_links(link_list, transformed_coordinates)

    # 描画ループ
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        screen.fill((0, 0, 0))  # 画面を黒色でクリア

        # X=0, Y=0 の線を引く
        pygame.draw.line(screen, (128, 128, 128), (0, origin[1]), (screen_width, origin[1]), 1)
        pygame.draw.line(screen, (128, 128, 128), (origin[0], 0), (origin[0], screen_height), 1)

        # 座標軸の目盛りとラベルを描画
        marker_length = 10
        text_offset = 15
        for coord_val in range(-origin[0]//50*50, screen_width//2, 50):
            # X 軸
            pygame.draw.line(screen, (128, 128, 128), (origin[0] + coord_val, origin[1] - marker_length), (origin[0] + coord_val, origin[1] + marker_length))
            #x_label = font.render(str(coord_val), True, (128, 128, 128))
            #screen.blit(x_label, (origin[0] + coord_val - text_offset, origin[1] + text_offset))

            # Y 軸
            pygame.draw.line(screen, (128, 128, 128), (origin[0] - marker_length, origin[1] - coord_val), (origin[0] + marker_length, origin[1] - coord_val))
            #y_label = font.render(str(coord_val), True, (128, 128, 128))
            #screen.blit(y_label, (origin[0] - text_offset * 2, origin[1] - coord_val - text_offset))

        # 頂点を描画
        for vertex_name, coord in transformed_coordinates.items():
            pygame.draw.circle(screen, vertex_color, coord, 5)    

            original_coord = positions[vertex_name] 
            
            if(vertex_name != 'A'):

                # 座標をメートルからミリメートルに変換
                original_coord_mm = (original_coord[0] * 1000, original_coord[1] * 1000)

                # ラベル名と変換前の座標を結合して表示
                label_text = f"{vertex_name} ({original_coord_mm[0]:.2f}, {original_coord_mm[1]:.2f})"
                label = font.render(label_text, True, (255, 255, 255))
                screen.blit(label, (coord[0] + 10, coord[1] - 10))

        # リンクを描画
        for link in links_coordinates:
            pygame.draw.line(screen, (255, 255, 255), link[0], link[1], 2)

        pygame.display.flip()  # 描画内容を画面に反映

    # Pygame 終了
    pygame.quit()
    sys.exit()
