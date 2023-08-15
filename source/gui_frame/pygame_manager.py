import pygame
import numpy as np
import math
from pygame.locals import *

from config import WINDOW_WIDTH, WINDOW_HEIGHT, SCALE_FACTOR
from leg_simulation import Robot
from leg_simulation.shared_data import SharedData, ServoFb, ServoCmd
#from ..leg_simulation.shared_data import SharedData, ServoCmd, ServoFb, ServoCmdStruct, ServoFbStruct

class PygameManager:
    def __init__(self, shared_data: SharedData) -> None:
        self.shared_data = shared_data
        self.time_data = [0, 1, 2, 3, 4, 5]
        self.speed_data = [0, 2, 4, 6, 8, 10]
        self.line_color = (255, 255, 255)
        self.origin = (50, 450)
        self.axis_scale = (100, 50)

        self.screen_height = WINDOW_HEIGHT
        self.screen_width = WINDOW_WIDTH
        self.scale_factor = SCALE_FACTOR

        self.robot = Robot()  # robot インスタンスを初期化
        self.link_list = self.robot.get_link_list()

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("2D View")

        running = True
        clock = pygame.time.Clock()  # フレームレート制御のためのClockオブジェクトを作成します
        
        while running:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    running = False

            screen.fill((0, 0, 0))
            font = pygame.font.Font(None, 24)

            # 2D オブジェクトの描画
            self.draw_2d(screen, font)

            pygame.display.update()
            #pygame.display.flip()

            clock.tick(30)
            pygame.time.delay(50)

            servo_fb : ServoFbStruct = self.shared_data.servo_fb

            #print(servo_fb.a_angle ) # 受信した角度データを表示
            #print(servo_fb.a_vol)   # 受信した電圧データを表示

        pygame.quit()

    def draw_2d(self, screen, font):
        positions = self.robot.get_positions()

        offset = (0, -400)

        transformed_coordinates = {key: self.convert_coordinates(coord, self.screen_width, self.screen_height, offset) for key, coord in positions.items()}

        links_coordinates = self.create_links_2D(self.link_list, transformed_coordinates)

        # ここから、pygameを使った2D表示を行います
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

        distance_GH = math.sqrt((positions['G'][0]-positions['H'][0])**2 + (positions['G'][1]-positions['H'][1])**2)

        # リミットなどの情報
        distance = distance_GH
        if distance != None:
            label_text = f"{'Distance G-H'}({distance:.4f}"
            label = font.render(label_text, True, (255, 255, 255))
            screen.blit(label, (0 + 10, 0 + 10))


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

    def convert_coordinates(self, coord, screen_width, screen_height, offset=(0, 0)):
        """
        与えられたデカルト座標を画面上で表示するためのピクセル座標に変換します。
        
        パラメータ:
            coord: xとy座標を含むタプル
            screen_width: 画面の幅(ピクセル単位)
            screen_height: 画面の高さ(ピクセル単位)
            offset: 座標に適用されるxとyオフセットのタプル（オプション）。デフォルトは (0,0)
            
        戻り値:
            変換されたx, y座標のタプル
        """

        x, y = coord
        
        # x を変換し、y を反転（スクリーン座標は左上が原点）
        # スケールファクターでスケーリングして、画面サイズの半分とオフセットを加算します。
        # ピクセル値は整数である必要があります。
        x_transformed = int((x * self.scale_factor) + screen_width // 2 + offset[0])
        y_transformed = int((-y * self.scale_factor) + screen_height // 2 + offset[1])
        return x_transformed, y_transformed
