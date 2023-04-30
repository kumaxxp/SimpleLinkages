import sys
import pygame
import math
import threading

from leg import Leg
from utils import convert_coordinates, create_links

import tkinter as tk

# 画面サイズ
screen_width, screen_height = 1000, 800

def slider_change(value):
    global theta_1, theta_2
    theta_1 = math.radians(float(scale_theta_1.get()))
    theta_2 = math.radians(float(scale_theta_2.get()))
    endeffector_position = leg.compute_endeffector_position(theta_1, theta_2)
    print("エンドエフェクタの位置:", endeffector_position)


def run_gui():
    global scale_theta_1, scale_theta_2
    gui = tk.Tk()
    gui.title("Theta Sliders")
    
    scale_theta_1 = tk.Scale(gui, from_=-180, to=180, orient=tk.HORIZONTAL, command=slider_change)
    scale_theta_1.set(-45)
    scale_theta_1.pack()
    
    scale_theta_2 = tk.Scale(gui, from_=-180, to=180, orient=tk.HORIZONTAL, command=slider_change)
    scale_theta_2.set(-115)
    scale_theta_2.pack()

    gui.mainloop()

if __name__ == "__main__":

    # Start the GUI in a separate thread
    gui_thread = threading.Thread(target=run_gui)
    gui_thread.daemon = True  # Set daemon so the main program closes when the pygame window is closed
    gui_thread.start()

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

    # 描画ループ
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break


        # -----脚の座標取得-----
        # 脚の頂点位置を取得
        positions = leg.get_positions()
        # 脚の頂点のリストを表示用に座標変換
        transformed_coordinates = {key: convert_coordinates(coord, screen_width, screen_height) for key, coord in positions.items()}
        # 座標からリンクのリストを生成
        links_coordinates = create_links(link_list, transformed_coordinates)

        # -----描画処理------
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

            # Y 軸
            pygame.draw.line(screen, (128, 128, 128), (origin[0] - marker_length, origin[1] - coord_val), (origin[0] + marker_length, origin[1] - coord_val))

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
