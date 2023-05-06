import pygame

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import threading

from config import WINDOW_WIDTH, WINDOW_HEIGHT, SCALE_FACTOR, NEAR_CLIP_PLANE, FAR_CLIP_PLANE
from leg_simulation import Robot

class OpenGLManager(threading.Thread):
    def __init__(self, initial_time, shared_data):
        self.shared_data = shared_data
        self.initial_time = initial_time
        self.robot = Robot()  # robot インスタンスを初期化

        self.screen_height = float(WINDOW_HEIGHT)
        self.screen_width = float(WINDOW_WIDTH)
        self.scale_factor = float(SCALE_FACTOR)

    def run(self):
        self.init_glut()

        # プロジェクション行列設定（透視投影）
        glMatrixMode(GL_PROJECTION)
    #    gluPerspective(45.0, float(WINDOW_WIDTH) / WINDOW_HEIGHT, NEAR_CLIP_PLANE, FAR_CLIP_PLANE)
        gluPerspective(45, (self.screen_width / self.screen_height), NEAR_CLIP_PLANE, FAR_CLIP_PLANE)
        glTranslatef(0.0, 0.0, 0.0)     # 平行移動
        glMatrixMode(GL_MODELVIEW)

        glutMainLoop()

    def init_glut(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        glutCreateWindow(b"3D View")

        glEnable(GL_DEPTH_TEST)
        glClearColor(0.5, 0.5, 0.5, 1)

        # OpenGL のコールバック関数の設定
        glutDisplayFunc(self.display_callback)
        glutIdleFunc(glutPostRedisplay)
        #glutSpecialFunc(keyboard_callback)

    def display_callback(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    #    glScalef(0.001, -0.001, 0.001)
        glScalef(-0.010, -0.010, 0.010)
        glRotatef(0.0, 1.0, 0.0, 0.0)
        glRotatef(0.0, 0.0, 1.0, 0.0)

        self.draw_axis()
#        self.draw_3d_objects((1,1,1))
        self.draw((1,1,1))

        # カメラの位置を更新する
        self.set_camera_position((0,0,0))

        glutSwapBuffers()

    def draw_3d_objects(self, object_position):
        # 表示テスト用の実装
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

    def draw(self, transformed_coordinates):
#        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#        glLoadIdentity()

#        glScalef(0.001, -0.001, 0.001)
#        glRotatef(30.0, 1.0, 0.0, 0.0)
#        glRotatef(10.0, 0.0, 1.0, 0.0)

        # 脚の座標取得
        positions = self.robot.get_positions()
        link_list = self.robot.get_link_list()
        
        transformed_coordinates = {key: self.convert_coordinates(coord, 0, 0) for key, coord in positions.items()}
        links_coordinates = self.create_links(link_list, transformed_coordinates, 0.0)

        # 描画処理
#        self.draw_axis()
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
    #    glColor3f(0.5, 0.5, 0.5)
        glColor3f(1.0, 1.0, 1.0)

        glBegin(GL_LINES)
        for link in links_coordinates:
            glVertex3fv(link[0])
            glVertex3fv(link[1])
        glEnd()

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

    # 座標からリンクのリストを作成する。三次元に拡張する
    def create_links(self, links, coordinates, t):
        link_coordinates = []
        for vertex1, vertex2 in links:
            if vertex1 in coordinates and vertex2 in coordinates:
                coord1 = coordinates[vertex1][0], coordinates[vertex1][1], t
                coord2 = coordinates[vertex2][0], coordinates[vertex2][1], t
                link_coordinates.append((coord1, coord2))
        return link_coordinates

    def convert_coordinates(self, coord, screen_width, screen_height):
        x, y = coord
        x_transformed = int((x * self.scale_factor) + screen_width // 2)
        y_transformed = int((-y * self.scale_factor) + screen_height // 2)
        return x_transformed, y_transformed
    
