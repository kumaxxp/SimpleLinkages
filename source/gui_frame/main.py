import time
import threading
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from config import WINDOW_WIDTH, WINDOW_HEIGHT, NEAR_CLIP_PLANE, FAR_CLIP_PLANE, speed
from draw_functions import draw_2d_objects, draw_3d_objects
from utils import update_object_position
from window_handlers import set_camera_position, keyboard_callback, draw_pygame_window

from window_handlers import speed

import gui_input

import tkinter as tk
from draw_graph import run_simulation

def main():
    # 初期化
    global initial_time
    initial_time = time.time()

    gui_input.start_gui_thread()

    # 3D表示
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b"3D View")

    glEnable(GL_DEPTH_TEST)
    glClearColor(0.5, 0.5, 0.5, 1)

    # プロジェクション行列設定（透視投影）
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45.0, float(WINDOW_WIDTH) / WINDOW_HEIGHT, NEAR_CLIP_PLANE, FAR_CLIP_PLANE)
    glMatrixMode(GL_MODELVIEW)

    # OpenGL ウィンドウで独自のループを実行
    def display_callback():
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        object_position = update_object_position(initial_time, speed=speed)
        draw_3d_objects(object_position)

        # カメラの位置を更新する
        set_camera_position(object_position)

        glutSwapBuffers()

    glutDisplayFunc(display_callback)
    glutIdleFunc(glutPostRedisplay)
    glutSpecialFunc(keyboard_callback)
    
    # Pygame ウィンドウで独自のループを実行
    t = threading.Thread(target=draw_pygame_window)
    t.start()

    glutMainLoop()

if __name__ == "__main__":
    main()
