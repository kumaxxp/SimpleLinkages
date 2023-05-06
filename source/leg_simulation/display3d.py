from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class Display3D:
    def __init__(self, screen):
        self.screen = screen
        self.init_3d_view()

    def init_3d_view(self):
        gluPerspective(45, (self.screen.get_width() / self.screen.get_height()), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -5.0)

        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glEnable(GL_DEPTH_TEST)

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

    def draw(self, transformed_coordinates, link_list):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glScalef(0.001, -0.001, 0.001)
        glRotatef(30.0, 1.0, 0.0, 0.0)
        glRotatef(10.0, 0.0, 1.0, 0.0)
        
        # 脚の座標取得
        positions = robot.leg.get_positions()
        
        links_coordinates = self.create_links(link_list, transformed_coordinates, 0.0)

        # 描画処理
        self.draw_axis()
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
        glColor3f(0.5, 0.5, 0.5)

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
