#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import numpy as np

import pygame
import sys

class Linkage5Bar:
    def __init__(self, initial_parameters):
        self.Positions = {}

        self.B1 = np.array([initial_parameters['b'] / 2, 0])
        self.B2 = np.array([-initial_parameters['b'] / 2, 0])

        self.b = initial_parameters['b']
        self.l1 = initial_parameters['l1']
        self.l2 = initial_parameters['l2']
        self.m1 = initial_parameters['m1']
        self.m2 = initial_parameters['m2']

        self.theta_M1 = None
        self.theta_M2 = None

    @staticmethod
    def circle_intersection(c1, r1, c2, r2):
        d = np.linalg.norm(c1 - c2)
        if d > r1 + r2:
            return None

        delta = (d**2 - r2**2 + r1**2) / (2 * d)

        h = np.sqrt(r1**2 - delta**2)

        e = (c2 - c1) / d

        p = c1 + delta * e
        q1, q2 = p + h * np.array([-e[1], e[0]]), p - h * np.array([-e[1], e[0]])

        return q1, q2

    def compute_vertex_X(self, theta_1, theta_2):
        x_M1, x_M2 = self.forward_kinematics(theta_1, theta_2)

        circle_intersects = self.circle_intersection(x_M1, self.m1, x_M2, self.m2)
        if circle_intersects is None:
            return None
        else:
            x1, x2 = circle_intersects
            # y座標が小さい頂点を選択します
            x_result = x1 if x1[1] < x2[1] else x2
            return x_result
        
    def compute_all_positions(self, theta_1, theta_2):
        # Calculate vertex A (M1)
        M1_x = self.B1[0] + self.l1 * np.cos(theta_1)
        M1_y = self.B1[1] + self.l1 * np.sin(theta_1)

        # Calculate vertex B (M2)
        M2_x = self.B2[0] + self.l2 * np.cos(theta_2)
        M2_y = self.B2[1] + self.l2 * np.sin(theta_2)

        # Call circle_intersection to find the possible X points
        M1 = np.array([M1_x, M1_y])
        M2 = np.array([M2_x, M2_y])
        intersection_points = self.circle_intersection(M1, self.m1, M2, self.m2)

        if intersection_points is None:
            return None

        X1, X2 = intersection_points

        print(X1)
        print(X2)

        # Choose the intersection point with smaller Y coordinate as the final X point
        if X1[1] < X2[1]:
            X_x, X_y = X1
        else:
            X_x, X_y = X2

        print(X_x,X_y)

        # Save all positions and angles in the Positions member variable
        self.Positions = {
            'B1': (self.B1[0], self.B1[1]),
            'B2': (self.B2[0], self.B2[1]),
            'M1': (M1_x, M1_y),
            'M2': (M2_x, M2_y),
            'X': (X_x, X_y),
        }

        return self.Positions
    
    def get_positions(self):
        return self.Positions

    def forward_kinematics(self, theta_1, theta_2):
        x_M1 = np.array([self.l1 * np.cos(theta_1), self.l1 * np.sin(theta_1)])
        x_M2 = np.array([self.b + self.l2 * np.cos(theta_2), self.l2 * np.sin(theta_2)])
        return x_M1, x_M2        

    def inverse_kinematics(self, target_position):
        x, y = target_position
        q = ((x ** 2 + y ** 2) - (self.m1 ** 2 + self.m2 ** 2)) / (2 * self.m1 * self.m2)
        if -1 <= q <= 1:
            self.theta_M2 = math.acos(q)
        else:
            raise ValueError("Target position is not reachable")

        beta = math.atan2(y, x)
        gamma = math.asin((self.m2 * math.sin(self.theta_M2)) / math.sqrt(x ** 2 + y ** 2))
        self.theta_M1 = beta - gamma


class Linkage4Bar:
    def __init__(self, initial_parameters, linkage5bar_instance):
        self.Positions = {}

        self.a = initial_parameters['a']
        self.b = initial_parameters['b']
        self.e = initial_parameters['e']

        self.linkage5bar = linkage5bar_instance

    def update_positions(self):
        A_x, A_y = self.linkage5bar.B1
        D_x, D_y = self.linkage5bar.B2

        B_x = A_x + self.a * math.cos(self.linkage5bar.theta_M1)
        B_y = A_y + self.a * math.sin(self.linkage5bar.theta_M1)

        C_x = D_x + self.a * math.cos(math.pi - self.linkage5bar.theta_M1)
        C_y = D_y + self.a * math.sin(math.pi - self.linkage5bar.theta_M1)

        return (A_x, A_y), (B_x, B_y), (C_x, C_y), (D_x, D_y)
    
    def compute_all_positions(self, M1, X, theta_1):
        A_x, A_y = M1
        X_x, X_y = X

        # 頂点Dの座標を計算
        D_x = A_x + self.a * np.cos(theta_1)
        D_y = A_y + self.a * np.sin(theta_1)

        # 頂点Bの座標を計算
        vec_AX = (X_x - A_x, X_y - A_y)
        norm_AX = np.linalg.norm(vec_AX)
        unit_vec_AX = (vec_AX[0] / norm_AX, vec_AX[1] / norm_AX)
        B_x = A_x + unit_vec_AX[0] * self.b
        B_y = A_y + unit_vec_AX[1] * self.b

        # 頂点Cの座標を計算
        C_x = B_x + self.a * np.cos(theta_1)
        C_y = B_y + self.a * np.sin(theta_1)

        # 頂点Eの座標を計算
        E_x = B_x + (self.a + self.e) * np.cos(theta_1)
        E_y = B_y + (self.a + self.e) * np.sin(theta_1)

        self.Positions = {
            "A": (A_x, A_y),
            "B": (B_x, B_y),
            "C": (C_x, C_y),
            "D": (D_x, D_y),
            "E": (E_x, E_y)
        }

        # 結果をリターンする
        return self.Positions

    def get_positions(self):
        return self.Positions


class Leg:
    def __init__(self, linkage5bar_params, linkage4bar_params):
        self.linkage5bar = Linkage5Bar(linkage5bar_params)
        self.linkage4bar = Linkage4Bar(linkage4bar_params, self.linkage5bar)

    def compute_endeffector_position(self, theta_1, theta_2):

        positions_5bar = self.linkage5bar.compute_all_positions(theta_1, theta_2)
        X = positions_5bar["X"]
        M1 = positions_5bar["M1"]

        positions_4bar = self.linkage4bar.compute_all_positions(M1, X, theta_1)
        endeffector_position = positions_4bar['E']

        return endeffector_position

    def forward_kinematics(self, B1_angle: float, B2_angle: float) -> dict:
        # set the new angles in the linkage5bar object
        self.linkage5bar.thetaB1_deg = B1_angle
        self.linkage5bar.thetaB2_deg = B2_angle
        
        # calculate positions and angles of linkage4bar object
        positions_4bar = self.linkage4bar.get_positions()
        angles_4bar = self.linkage4bar.get_angles_degrees()
        
        # calculate new positions of linkage5bar
        self.linkage5bar.set_new_X(positions_4bar["E"])
        positions_5bar = self.linkage5bar.get_positions()
        
        # combine the results
        result_positions = {**positions_4bar, **positions_5bar}
        
        return result_positions
    
    def get_positions(self):
        return { **self.linkage5bar.get_positions() , **self.linkage4bar.get_positions()}

    def inverse_kinematics(self, target_position: tuple) -> dict:
        pass  # To be implemented


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
