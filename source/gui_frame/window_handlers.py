import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from config import WINDOW_WIDTH, WINDOW_HEIGHT, speed
from draw_functions import draw_2d_objects
import gui_input

def keyboard_callback(key, x, y):
    global speed

    slider_value = gui_input.get_slider_value()
    print(slider_value)  # 現在のスライダ値をコンソールに表示
    
    # 上矢印キーで速度を増加
    if key == GLUT_KEY_UP:
        speed += 0.1

    # 下矢印キーで速度を減少
    elif key == GLUT_KEY_DOWN:
        speed -= 0.1

    # リミット速度
    speed = max(0.0, speed)

    print("Speed:", speed)

def set_camera_position(object_position, distance=10):
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

def draw_graph(screen, data, color, origin, axis_scale):
    for i in range(len(data) - 1):
        start_pos = (origin[0] + i * axis_scale[0], origin[1] - data[i] * axis_scale[1])
        end_pos = (origin[0] + (i + 1) * axis_scale[0], origin[1] - data[i + 1] * axis_scale[1])
        pygame.draw.line(screen, color, start_pos, end_pos, 3)

def draw_pygame_window():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("2D View")

    # Define data and settings for the graph
    time_data = [0, 1, 2, 3, 4, 5]
    speed_data = [0, 2, 4, 6, 8, 10]
    line_color = (255, 255, 255)
    origin = (50, 450)
    axis_scale = (100, 50)    

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False

        screen.fill((0, 0, 0))

        # 2D オブジェクトの描画
        draw_2d_objects(screen)

        # グラフ表示
        draw_graph(screen, speed_data, line_color, origin, axis_scale)        

        pygame.display.flip()

    pygame.quit()