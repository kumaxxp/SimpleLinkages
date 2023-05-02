import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import threading
import time

global speed
speed = 1.0

def keyboard_callback(key, x, y):
    global speed

    # 上矢印キーで速度を増加
    if key == GLUT_KEY_UP:
        speed += 0.1

    # 下矢印キーで速度を減少
    elif key == GLUT_KEY_DOWN:
        speed -= 0.1

    # リミット速度
    speed = max(0.0, speed)

    print("Speed:", speed)


# 設定
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300
NEAR_CLIP_PLANE = 0.1
FAR_CLIP_PLANE = 100.0

def get_color_by_speed(speed):
    # 最小速度と最大速度を定義
    min_speed, max_speed = 0.0, 3.0

    # オブジェクトの色相を計算（速度が低いほど青、高いほど赤になるように設定）
    t = (speed - min_speed) / (max_speed - min_speed)
    r = t
    g = 0
    b = 1 - t

    # クリッピング
    r = min(max(r, 0), 1)
    g = min(max(g, 0), 1)
    b = min(max(b, 0), 1)

    return r, g, b

def draw_3d_objects(object_position):
    # 頂点
    # 変更1: オブジェクトの色を速度に基づいて変更
    r, g, b = get_color_by_speed(speed)
    glColor3f(r, g, b)

    glPushMatrix()
    glTranslatef(*object_position)

    # 変更2: glutSolidCubeからglutSolidSphereに変更
    glutSolidSphere(1.0, 20, 20)

    glPopMatrix()    
    glBegin(GL_POINTS)

    # 変更2: object_position を使用して頂点を描画
    glVertex3f(*object_position)
    glEnd()

    # リンク
    glColor(0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(0, 0, 0)
    glVertex3f(1, 1, 1)
    glEnd()

# 変更3: 時間経過に応じてオブジェクトの位置を更新する関数
def update_object_position(initial_time, speed):
    elapsed_time = time.time() - initial_time
    x = speed * elapsed_time % 5.0
    return x, 0.0, 0.0
    
# Pygameを利用した2D頂点/リンク描画関数
def draw_2d_objects(screen):
    pygame.draw.circle(screen, (255, 0, 0), (100, 100), 5)
    pygame.draw.line(screen, (0, 255, 0), (80, 80), (120, 120), 3)

def draw_pygame_window():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("2D View")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False

        screen.fill((0, 0, 0))

        # 2D オブジェクトの描画
        draw_2d_objects(screen)

        pygame.display.flip()

    pygame.quit()

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

def main():
    # 初期化
    global initial_time
    initial_time = time.time()

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
