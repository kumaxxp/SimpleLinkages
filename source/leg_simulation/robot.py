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

    def draw_2d(self, screen, font):
        positions = self.leg.get_positions()

        transformed_coordinates = {key: self.convert_coordinates(coord, self.screen_width, self.screen_height) for key, coord in positions.items()}

        links_coordinates = self.create_links_2D(self.link_list, transformed_coordinates)

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

        pygame.display.flip()

    def init_3d_view(self):
        # gluPerspective(45, (self.screen_width / self.screen_height), 0.1, 50.0)
        gluPerspective(0, (self.screen_width / self.screen_height), 0.1, 50.0)
        glTranslatef(0.0, 0.0, 0.0)     # 平行移動

        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)


    def draw_3d_objects(self, object_position):
        # 頂点
        # オブジェクトの色を固定値に設定
        glColor3f(1.0, 0.0, 0.0)

        glPushMatrix()
        glTranslatef(*object_position)

        # glutSolidCube を使用してオブジェクトを描画
        glutSolidCube(1.0)

        glPopMatrix()
        glBegin(GL_POINTS)

        # object_position を使用して頂点を描画
        glVertex3f(*object_position)
        glEnd()

        # リンク
        glColor(0.0, 1.0, 0.0)
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(1, 1, 1)
        glEnd()

    # legを表示する
    def display_gl(self, surface):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glScalef(0.001, -0.001, 0.001)  # オブジェクトのスケール(Y軸を上下反転)
        glRotatef(30.0, 1.0, 0.0, 0.0)  # X軸を中心に30度傾ける
        glRotatef(10.0, 0.0, 1.0, 0.0)  # Y軸を中心に10度傾ける

        # 脚の座標取得
        positions = self.leg.get_positions()

        transformed_coordinates = {key: self.convert_coordinates(coord, 0, 0) for key, coord in positions.items()}

        links_coordinates = self.create_links(self.link_list, transformed_coordinates, 0.0)

        # 描画処理
        self.draw_axis()
        self.draw_links(links_coordinates)

        pygame.display.flip()
        pygame.time.wait(10)

    def draw_axis(self):
        glColor3f(0.0, 1.0, 0.0)
        #glColor3f(0.5, 0.5, 0.5)

        glBegin(GL_LINES)
        glVertex3f(-self.screen_width // 2, 0, 0)
        glVertex3f(self.screen_width // 2, 0, 0)
        glEnd()

        glBegin(GL_LINES)
        glVertex3f(0, -self.screen_height // 2, 0)
        glVertex3f(0, self.screen_height // 2, 0)
        glEnd()

        glBegin(GL_LINES)
        glVertex3f(0, 0, -self.screen_height // 2)
        glVertex3f(0, 0, self.screen_height // 2)
        glEnd()

    def draw_links(self, links_coordinates):
        glColor3f(0.5, 0.5, 0.5)

        glBegin(GL_LINES)
        for link in links_coordinates:
            glVertex3fv(link[0])
            glVertex3fv(link[1])
        glEnd()

    # 座標からリンクのリストを作成する。三次元に拡張する
    def create_links(self, links, coordinates, t):
        link_coordinates = []
        for vertex1, vertex2 in links:
            if vertex1 in coordinates and vertex2 in coordinates:
                coord1 = coordinates[vertex1][0], coordinates[vertex1][1], t
                coord2 = coordinates[vertex2][0], coordinates[vertex2][1], t
                link_coordinates.append((coord1, coord2))
        return link_coordinates

    def set_camera_position(self, object_position, distance=10):
        # カメラの位置を計算
        camera_position = (object_position[0], object_position[1], object_position[2] - distance)

        # カメラの注視点をオブジェクトの位置に設定
        target_position = object_position

        # カメラの向きを上方向に設定（デフォルト）
        up_direction = (0, 1, 0)

        # gluLookAtを使ってカメラの位置と注視点を設定
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(*camera_position, *target_position, *up_direction)


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

