from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import pygame

from .config import speed

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

def draw_2d_objects(screen):
    pygame.draw.circle(screen, (255, 0, 0), (100, 100), 5)
    pygame.draw.line(screen, (0, 255, 0), (80, 80), (120, 120), 3)
