import pygame

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import numpy as np

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

        # 線の太さの範囲を取得
        range_buffer = (GLfloat * 2)()
        glGetFloatv(GL_ALIASED_LINE_WIDTH_RANGE, range_buffer)

        min_line_width = range_buffer[0]
        max_line_width = range_buffer[1]

        print(f"Line width range: {min_line_width} to {max_line_width}")


    def display_callback(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    #    glScalef(0.001, -0.001, 0.001)
        glScalef(-0.010, -0.010, 0.010)
        glRotatef(20.0, 1.0, 0.0, 0.0)
        glRotatef(20.0, 0.0, 1.0, 0.0)

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
#        self.draw_links(links_coordinates)
        self.draw_links_cylinder(links_coordinates, 10.0)


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

    def draw_links_wire(self, links_coordinates):
    #    glColor3f(0.5, 0.5, 0.5)
        glColor3f(1.0, 1.0, 1.0)

        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [1.0, 1.0, 1.0, 1.0])

        # 線の太さを設定
        glLineWidth(4.0)

        glBegin(GL_LINES)
        for link in links_coordinates:
            glVertex3fv(link[0])
            glVertex3fv(link[1])
        glEnd()

    def draw_links(self, links_coordinates):
        glColor3f(1.0, 1.0, 1.0)

        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [1.0, 1.0, 1.0, 1.0])

        for link in links_coordinates:
            self.draw_cylinder(link[0], link[1], 0.05)  # 0.05は太さを表しています

    def draw_cylinder(self, start, end, radius, height):
        start = np.array(start)
        end = np.array(end)
        direction = end - start

        up = np.array([0, 0, 1])
        z_axis = direction / np.linalg.norm(direction)
        x_axis = np.cross(up, z_axis)
        y_axis = np.cross(z_axis, x_axis)

        rotation_matrix = np.eye(4)
        rotation_matrix[:3, 0] = x_axis
        rotation_matrix[:3, 1] = y_axis
        rotation_matrix[:3, 2] = z_axis
        rotation_matrix[3, 3] = 1
        glPushMatrix()

        glTranslatef(start[0], start[1], start[2])
        glMultMatrixf(rotation_matrix.T.flatten())
    #    glColor3f(0.5, 0.1, 0.1)

        glDisable(GL_TEXTURE_2D)

        quadric = gluNewQuadric()
        gluQuadricNormals(quadric, GLU_SMOOTH)
        gluQuadricTexture(quadric, GL_TRUE)
        gluCylinder(quadric, radius, radius, height, 32, 32)

        glEnable(GL_TEXTURE_2D)
        
        glPopMatrix()

    def enable_lighting(self):
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        glLightfv(GL_LIGHT0, GL_POSITION, [0.0, -100.0, -100.0, 0.0])

        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.01, 0.01, 0.01, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.06, 0.06, 0.06, 1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [0.03, 0.03, 0.03, 1.0])

        # 反射パラメーターを設定
        glMaterialf(GL_FRONT, GL_SHININESS, 50)

        # 反射光の設定
        glMaterialfv(GL_FRONT, GL_SPECULAR, GLfloat_3(0.1, 0.1, 0.1))

    def draw_links_cylinder(self, links_coordinates, radius=0.1):
        self.enable_lighting()

#        glColor3f(1.0, 1.0, 1.0)
#        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [0.06, 0.06, 0.06, 1.0])
#        glMaterialfv(GL_FRONT, GL_SPECULAR, [0.1, 0.1, 0.1, 1.0])
#        glMaterialf(GL_FRONT, GL_SHININESS, 50.0)

        for link in links_coordinates:
            start = link[0]
            end = link[1]
            height = np.linalg.norm(np.array(end) - np.array(start))
            self.draw_cylinder(start, end, radius, height)

        # Disable lighting after drawing
        glDisable(GL_LIGHTING)

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
    
    def get_orientation_quaternion(self, direction):
        up = np.array([0, 1, 0])
        axis = np.cross(up, direction)
        axis_norm = np.linalg.norm(axis)

        if axis_norm < 0.0001:
            return np.array([1, 0, 0, 0])

        axis_normalized = axis / axis_norm

        angle_over_two = np.arccos(np.dot(up, direction)) / 2
        sin_angle_over_two = np.sin(angle_over_two)

        return np.array([
            np.cos(angle_over_two),
            axis_normalized[0] * sin_angle_over_two,
            axis_normalized[1] * sin_angle_over_two,
            axis_normalized[2] * sin_angle_over_two
        ])

    def quaternion_to_axis_angle(self, quat):
        if abs(1.0 - quat[0]) < 0.0001:
            return 0, 0, 1, 0

        angle = 2 * np.arccos(quat[0])
        temp = np.sqrt(1 - (quat[0] ** 2))

        x = quat[1] / temp
        y = quat[2] / temp
        z = quat[3] / temp
        
        return np.degrees(angle), x, y, z

