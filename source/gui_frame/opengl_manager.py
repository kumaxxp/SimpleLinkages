from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from config import WINDOW_WIDTH, WINDOW_HEIGHT, NEAR_CLIP_PLANE, FAR_CLIP_PLANE
from draw_functions import draw_2d_objects, draw_3d_objects
from utils import update_object_position
from window_handlers import set_camera_position, keyboard_callback

class OpenGLManager:
    def __init__(self, initial_time, shared_data):
        self.shared_data = shared_data
        self.initial_time = initial_time

    def run(self):
        self.init_glut()

        # プロジェクション行列設定（透視投影）
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45.0, float(WINDOW_WIDTH) / WINDOW_HEIGHT, NEAR_CLIP_PLANE, FAR_CLIP_PLANE)
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
        glutSpecialFunc(keyboard_callback)

    def display_callback(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        speed = self.shared_data.get_value("speed")

        # If speed is None, set it to a default value (e.g., 0.0)
        if speed is None:
            speed = 0.0

        object_position = update_object_position(self.initial_time, speed=speed)
        print(speed)

        draw_3d_objects(object_position)

        # カメラの位置を更新する
        set_camera_position(object_position)

        glutSwapBuffers()
