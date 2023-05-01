import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import threading

# 設定
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300

def draw_3d_objects():
    # 頂点
    glColor(1.0, 0.0, 0.0)
    glBegin(GL_POINTS)
    glVertex3f(0, 0, 0)
    glEnd()

    # リンク
    glColor(0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(0, 0, 0)
    glVertex3f(1, 1, 1)
    glEnd()

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

def main():
    # 初期化
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b"3D View")

    glEnable(GL_DEPTH_TEST)
    glClearColor(0.5, 0.5, 0.5, 1)

    # OpenGL ウィンドウで独自のループを実行
    def display_callback():
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # 3D オブジェクトの描画
        draw_3d_objects()

        glutSwapBuffers()
    
    glutDisplayFunc(display_callback)
    glutIdleFunc(glutPostRedisplay)

    # Pygame ウィンドウで独自のループを実行
    t = threading.Thread(target=draw_pygame_window)
    t.start()

    glutMainLoop()

if __name__ == "__main__":
    main()
