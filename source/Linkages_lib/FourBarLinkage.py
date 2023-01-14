import cv2
import os
import shutil

from moviepy.editor import ImageSequenceClip

from PIL import Image
import glob
import numpy as np

import math
from typing import Tuple
from typing import List

import math

LINK_COLOR = (100, 100, 100)
LINK_COLOR_R = (0, 0, 255)
LINK_WIDTH = 2
LINK_COLOR_B = (255, 0, 0)
LINK_COLOR_G = (0, 255, 0)

PIN_RADIUS = 30
PIN_RADIUS_PHI = 20
PIN_COLOR = (100, 100, 100)
PIN_COLOR_ARC = (255, 100, 100)
PIN_COLOR_PHI1 = (100, 255, 100)
PIN_COLOR_PHI2 = (100, 100, 255)
PIN_TEXT = (0, 0, 0)
PIN_WIDTH = 1

CENTER_RADIUS = 50
CENTER_COLOR = (100, 100, 100)
CENTER_COLOR_ARC = (240, 220, 220)

RECT_LEN = 40
RECT_COLOR = (50, 50, 50)

# 四節リンクを表すクラス
class FourBarLinkage:
    def __init__(self, a, b, e, angle_phi, angle_delta):
        self.a = a
        self.b = b
        self.c = a
        self.d = b
        self.e = e

        self.f = math.sqrt(2* ((RECT_LEN * 2) ** 2))

        self.t = 0
        self.pos_ellipse = (100, 100)

        self.angle_phi = angle_phi
        self.angle_delta = angle_delta
        self.angle_gamma = self.angle_phi + self.angle_delta

        self.phi = math.radians(angle_phi)
        self.delta = math.radians(angle_delta)
        self.gamma = math.radians(self.angle_gamma)
        self.phi_delta = math.radians(angle_phi + angle_delta)

        # 各点の座標を表す変数を定義する
        self.D = (0, 0)
        self.A = (a * math.cos(self.delta), a * math.sin(self.delta))
        self.B = (a * math.cos(self.delta) + b * math.cos(self.phi_delta), 
                a * math.sin(self.delta) + b * math.sin(self.phi_delta))
        self.C = (b * math.cos(self.phi) * math.cos(self.delta) - b * math.sin(self.phi) * math.sin(self.delta),
                b * math.cos(self.phi) * math.sin(self.delta) + b * math.sin(self.phi) * math.cos(self.delta))

        self.E = (a * math.cos(self.delta) + (b + e) * math.cos(self.phi_delta),
                a * math.sin(self.delta) + (b + e) * math.sin(self.phi_delta))


        #self.F = (self.D[0] + self.f * math.cos(self.delta), self.D[1] + self.f * math.sin(self.delta))
        self.F = (self.D[0] + RECT_LEN*2, self.D[1] + RECT_LEN*2)
        self.G = (self.F[0] + self.b * math.cos(self.gamma), self.F[1] + self.b * math.sin(self.gamma))

        # 各点の角度を表す変数を定義する
        self.angle_A = 180 - angle_phi
        self.angle_B = angle_phi
        self.angle_C = 180 - angle_phi
        self.angle_phi  = angle_phi

        self.angle_phi1 = 0
        self.angle_phi2 = 0

        self.L = math.sqrt((self.E[0] - self.E[0])**2 + (self.E[1] - self.E[1])**2)

        self.update_positions()


    def update_positions(self):

        # 各点の座標を計算する
        self.phi_delta = math.radians(self.angle_phi + self.angle_delta)
        self.angle_gamma = self.angle_phi + self.angle_delta
        self.gamma = math.radians(self.angle_gamma)

        # 各点の座標を表す変数を定義する
        self.D = (0, 0)
        self.A = (self.a * math.cos(self.delta), self.a * math.sin(self.delta))
        self.B = (self.a * math.cos(self.delta) + self.b * math.cos(self.phi_delta), 
                self.a * math.sin(self.delta) + self.b * math.sin(self.phi_delta))
        self.C = (self.b * math.cos(self.phi) * math.cos(self.delta) - self.b * math.sin(self.phi) * math.sin(self.delta),
                self.b * math.cos(self.phi) * math.sin(self.delta) + self.b * math.sin(self.phi) * math.cos(self.delta))

        self.E = (self.a * math.cos(self.delta) + (self.b + self.e) * math.cos(self.phi_delta),
                self.a * math.sin(self.delta) + (self.b + self.e) * math.sin(self.phi_delta))

        self.L = math.sqrt((self.E[0] - self.E[0])**2 + (self.E[1] - self.E[1])**2)

        in_delta = math.radians(self.angle_delta - 180)

#        self.F = (self.D[0] + self.f * math.cos(in_delta), self.D[1] + self.f * math.sin(in_delta))
        self.G = (self.F[0] + self.b * math.cos(self.gamma), self.F[1] + self.b * math.sin(self.gamma))

        # 各点の角度を表す変数を定義する
        self.angle_A = 180 - self.angle_phi
        self.angle_B = self.angle_phi
        self.angle_C = 180 - self.angle_phi
        self.angle_phi  = self.angle_phi

        # 各点の図上の角度を表す変数を定義する
        self.angle_D_st = 0 + self.angle_delta
        self.angle_D_ed = self.angle_D_st + self.angle_phi

        self.angle_A_st = self.angle_phi + self.angle_delta
        self.angle_A_ed = self.angle_A_st + self.angle_A

        self.angle_B_st = self.angle_A_ed
        self.angle_B_ed = self.angle_B_st + self.angle_B

        self.angle_C_st = self.angle_B_ed
        self.angle_C_ed = self.angle_C_st + self.angle_C

    def update_inverse_kinematics(self, x: float, y: float):
        data:float
        a_cos:float
        a_tan:float

        # δを計算
        data = (x ** 2 + y ** 2 + self.a ** 2 - (self.b + self.e) ** 2) / (2 * self.a * math.sqrt(x**2 + y**2))
        if data > 1 or data < -1:
            return

        a_cos = math.acos(data)
        a_tan = math.atan2(y,x)

        # マイナス側を採用
        delta_p =  a_cos + a_tan
        delta_m = -a_cos + a_tan

        self.set_delta(math.degrees(delta_m))

        # Φを計算
        a_tan_phi:float
        a_tan_phi = math.atan2((y - self.a * math.sin(self.delta)) , (x - self.a * math.cos(self.delta)))
        angle_phi = math.degrees(a_tan_phi) - self.angle_delta

        self.set_phi(angle_phi)


    def set_phi(self, angle):
        # Φの角度は頂点Dの角度として保存する
        self.angle_phi = angle
        self.phi = math.radians(angle)

        self.update_positions()

    def set_delta(self, angle):
        # Δの角度は全体の角度として保存する
        self.angle_delta = angle
        self.delta = math.radians(angle)

        self.update_positions()

    def _convert_coordinate(self, pos: tuple, offset_x: int = 400, offset_y: int = 200) -> tuple:
        pos_int_x = int(pos[0]) + offset_x
        pos_int_y = -int(pos[1]) + offset_y
        pos_int = (pos_int_x, pos_int_y)
        return pos_int

    def _convert_angle(self, angle_st: float, angle_ed: float) -> Tuple:
        angle_st_tm : int
        angle_ed_tm : int
        angle_st_tm = -int(angle_st) 
        angle_ed_tm = -int(angle_ed) 

        if angle_st_tm < angle_ed_tm:
            if angle_st_tm < 0:
                angle_st_tm += 360
            else:
                angle_ed_tm -= 360

        return angle_st_tm, angle_ed_tm

    def draw(self, image: np.ndarray) -> None:

        # cv2の座標系に位置を変換する
        # Y座標系を±反転し、画面の中央に原点をシフトする
        pos_A_int = self._convert_coordinate(self.A)
        pos_B_int = self._convert_coordinate(self.B)
        pos_C_int = self._convert_coordinate(self.C)
        pos_D_int = self._convert_coordinate(self.D)
        pos_E_int = self._convert_coordinate(self.E)
        pos_F_int = self._convert_coordinate(self.F)
        pos_G_int = self._convert_coordinate(self.G)

        # cv2の座標系に回転角を変換する
        # 角度は±反転し、反時計回りで塗りつぶせるように、
        # 開始角度を大きな数値になるように調整する
        angle_delta_st, angle_delta_ed = self._convert_angle(0, self.angle_delta)

        angle_A_st, angle_A_ed = self._convert_angle(self.angle_A_st, self.angle_A_ed)
        angle_B_st, angle_B_ed = self._convert_angle(self.angle_B_st, self.angle_B_ed)
        angle_C_st, angle_C_ed = self._convert_angle(self.angle_C_st, self.angle_C_ed)
        angle_D_st, angle_D_ed = self._convert_angle(self.angle_D_st, self.angle_D_ed)

        # 中心座標
        cv2.circle(image, center=pos_D_int, radius=CENTER_RADIUS, color=CENTER_COLOR, thickness=1, lineType=cv2.LINE_AA, shift=0)
        cv2.ellipse(image, center=pos_D_int, axes=(CENTER_RADIUS, CENTER_RADIUS),
            angle=0, startAngle=angle_delta_st, endAngle=angle_delta_ed, color=CENTER_COLOR_ARC, thickness=-1, lineType=cv2.LINE_AA)

        # モーターを互い違いに2配置するイメージ
        pos1 = (pos_D_int[0] - RECT_LEN, pos_D_int[1] -RECT_LEN)
        pos2 = (pos_D_int[0] + RECT_LEN*3, pos_D_int[1] +RECT_LEN)
        cv2.rectangle(image, pt1=pos1, pt2=pos2, color=RECT_COLOR, thickness=1, lineType=cv2.LINE_4, shift=0)

        pos1 = (pos_D_int[0] - RECT_LEN, pos_D_int[1] -RECT_LEN*3)
        pos2 = (pos_D_int[0] + RECT_LEN*3, pos_D_int[1] -RECT_LEN)
        cv2.rectangle(image, pt1=pos1, pt2=pos2, color=RECT_COLOR, thickness=1, lineType=cv2.LINE_4, shift=0)

        pos_motor = (pos_D_int[0] + RECT_LEN*2, pos_D_int[1] - RECT_LEN*2)
        cv2.circle(image, center=pos_motor, radius=PIN_RADIUS, color=CENTER_COLOR, thickness=1, lineType=cv2.LINE_AA, shift=0)

        # linkを描画する
        cv2.line(image, pt1=pos_A_int, pt2=pos_B_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_B_int, pt2=pos_C_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_C_int, pt2=pos_D_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_D_int, pt2=pos_A_int, color=LINK_COLOR_R, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_B_int, pt2=pos_E_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_C_int, pt2=pos_G_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_F_int, pt2=pos_G_int, color=LINK_COLOR_R, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)

        # 頂点Dを描画する。Φ/Φ1/Φ2を表示
        cv2.circle(image, center=pos_A_int, radius=PIN_RADIUS, color=PIN_COLOR, thickness=PIN_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.ellipse(image, center=pos_A_int, axes=(PIN_RADIUS, PIN_RADIUS),
            angle=0, startAngle=angle_A_st, endAngle=angle_A_ed, color=PIN_COLOR_ARC, thickness=-1, lineType=cv2.LINE_AA)

        cv2.circle(image, center=pos_B_int, radius=PIN_RADIUS, color=PIN_COLOR, thickness=PIN_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.ellipse(image, center=pos_B_int, axes=(PIN_RADIUS, PIN_RADIUS),
            angle=0, startAngle=angle_B_st, endAngle=angle_B_ed, color=PIN_COLOR_ARC, thickness=-1, lineType=cv2.LINE_AA)

        cv2.circle(image, center=pos_C_int, radius=PIN_RADIUS, color=PIN_COLOR, thickness=PIN_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.ellipse(image, center=pos_C_int, axes=(PIN_RADIUS, PIN_RADIUS),
            angle=0, startAngle=angle_C_st, endAngle=angle_C_ed, color=PIN_COLOR_ARC, thickness=-1, lineType=cv2.LINE_AA)

        cv2.circle(image, center=pos_D_int, radius=PIN_RADIUS, color=PIN_COLOR, thickness=PIN_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.ellipse(image, center=pos_D_int, axes=(PIN_RADIUS, PIN_RADIUS),
            angle=0, startAngle=angle_D_st, endAngle=angle_D_ed, color=PIN_COLOR_ARC, thickness=-1, lineType=cv2.LINE_AA)

        cv2.circle(image, center=pos_E_int, radius=PIN_RADIUS, color=PIN_COLOR, thickness=PIN_WIDTH, lineType=cv2.LINE_AA, shift=0)

        cv2.circle(image, center=pos_F_int, radius=PIN_RADIUS, color=PIN_COLOR, thickness=PIN_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.circle(image, center=pos_G_int, radius=PIN_RADIUS, color=PIN_COLOR, thickness=PIN_WIDTH, lineType=cv2.LINE_AA, shift=0)

#        cv2.circle(image, center=pos_F_int, radius=PIN_RADIUS, color=PIN_COLOR, thickness=PIN_WIDTH, lineType=cv2.LINE_AA, shift=0)
#        cv2.ellipse(image, center=pos_F_int, axes=(PIN_RADIUS, PIN_RADIUS),
#            angle=0, startAngle=angle_F_st, endAngle=angle_F_ed, color=PIN_COLOR_ARC, thickness=-1, lineType=cv2.LINE_AA)

#        cv2.circle(image, center=pos_G_int, radius=PIN_RADIUS, color=PIN_COLOR, thickness=PIN_WIDTH, lineType=cv2.LINE_AA, shift=0)
#        cv2.ellipse(image, center=pos_G_int, axes=(PIN_RADIUS, PIN_RADIUS),
#            angle=0, startAngle=angle_G_st, endAngle=angle_G_ed, color=PIN_COLOR_ARC, thickness=-1, lineType=cv2.LINE_AA)

        # 対角線
        cv2.line(image, pt1=pos_D_int, pt2=pos_B_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)

        # テキスト
        cv2.putText(img = image, text = 'A', org = pos_A_int, fontFace=cv2.FONT_HERSHEY_PLAIN, 
            fontScale=1.0, color=PIN_TEXT, thickness=1, lineType=cv2.LINE_AA)
        cv2.putText(img = image, text = 'B', org = pos_B_int, fontFace=cv2.FONT_HERSHEY_PLAIN, 
            fontScale=1.0, color=PIN_TEXT, thickness=1, lineType=cv2.LINE_AA)
        cv2.putText(img = image, text = 'C', org = pos_C_int, fontFace=cv2.FONT_HERSHEY_PLAIN, 
            fontScale=1.0, color=PIN_TEXT, thickness=1, lineType=cv2.LINE_AA)
        cv2.putText(img = image, text = 'D', org = pos_D_int, fontFace=cv2.FONT_HERSHEY_PLAIN, 
            fontScale=1.0, color=PIN_TEXT, thickness=1, lineType=cv2.LINE_AA)
        cv2.putText(img = image, text = 'E', org = pos_E_int, fontFace=cv2.FONT_HERSHEY_PLAIN, 
            fontScale=1.0, color=PIN_TEXT, thickness=1, lineType=cv2.LINE_AA)

        pos_int = (int(pos_A_int[0]), int(pos_A_int[1]) + 20)
        cv2.putText(img = image, text = str(self.angle_A), org = pos_int, fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.0, color=PIN_TEXT, thickness=1, lineType=cv2.LINE_AA)
        pos_int = (int(pos_B_int[0]), int(pos_B_int[1]) + 20)
        cv2.putText(img = image, text = str(self.angle_B), org = pos_int, fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.0, color=PIN_TEXT, thickness=1, lineType=cv2.LINE_AA)


        # 座標表示
        pos_int = (int(pos_E_int[0]), int(pos_E_int[1]) + 20)
        cv2.putText(img = image, text = str(self.E), 
            org = pos_int, fontFace=cv2.FONT_HERSHEY_PLAIN, 
            fontScale=1.0, color=PIN_TEXT, thickness=1, lineType=cv2.LINE_AA)

        pos_int = (int(pos_D_int[0]), int(pos_D_int[1]) + 20)
        cv2.putText(img = image, text = str(self.D), 
            org = pos_int, fontFace=cv2.FONT_HERSHEY_PLAIN, 
            fontScale=1.0, color=PIN_TEXT, thickness=1, lineType=cv2.LINE_AA)

        # ガイド用の楕円を描く
        pos_Guide = (pos_D_int[0], pos_D_int[1] + 250)
        cv2.ellipse(image, center=pos_Guide, axes=(100, 20),
            angle=0, startAngle=0, endAngle=360, color=PIN_COLOR, thickness=1, lineType=cv2.LINE_AA)

        
        self.pos_ellipse = self.ellipse_xy(self.t)
        pos_ellipse_int = self._convert_coordinate(self.pos_ellipse)
        self.t += 1

        cv2.circle(image, center=pos_ellipse_int, radius=PIN_RADIUS, color=PIN_COLOR, thickness=1, lineType=cv2.LINE_AA, shift=0)


    # ポイントの座標を変換する
    def _transform_pin(self, pos: Tuple[float, float], angle: float, H: np.ndarray) -> \
        Tuple[Tuple[float, float], float]:

        # 元の座標を表す行列を作成
        point = np.array([[pos[0]], [pos[1]], [1]])
        
        # 元の座標を変換行列 H の座標系に変換
        transformed_point = H @ point
        
        # 変換後の座標を取得
        x_t = transformed_point[0, 0]
        y_t = transformed_point[1, 0]

        radian = math.radians(angle)
        
        # 元の回転角度を表す行列を作成
        rotation = np.array([[np.cos(radian), -np.sin(radian), 0],
                            [np.sin(radian), np.cos(radian), 0],
                            [0, 0, 1]])
        
        # 元の回転角度を変換行列 H の座標系に変換
        transformed_rotation = H @ rotation @ np.linalg.inv(H)
        
        # 変換後の回転角度を取得
        theta = np.arctan2(transformed_rotation[1, 0], transformed_rotation[0, 0])

        pos: tuple = (x_t, y_t)
        theta_degree = math.degrees(theta)

        return pos, theta_degree

    # ポイントの座標を変換する
    def _transform_point(self, pos: Tuple[float, float], H: np.ndarray) -> Tuple[float, float]:

        # 元の座標を表す行列を作成
        point = np.array([[pos[0]], [pos[1]], [1]])
        
        # 元の座標を変換行列 H の座標系に変換
        transformed_point = H @ point
        
        # 変換後の座標を取得
        x_t = transformed_point[0, 0]
        y_t = transformed_point[1, 0]
                
        # 変換後の回転角度を取得
        pos: Tuple = (x_t, y_t)

        return pos

    # ポイントの座標を変換する
    def _transform_angle(self, angle: float, H: np.ndarray) -> float:

        radian = math.radians(angle)

        # 元の回転角度を表す行列を作成
        rotation = np.array([[np.cos(radian), -np.sin(radian), 0],
                            [np.sin(radian), np.cos(radian), 0],
                            [0, 0, 1]])
        
        # 元の回転角度を変換行列 H の座標系に変換
        transformed_rotation = H @ rotation @ np.linalg.inv(H)
        
        # 変換後の回転角度を取得
        theta = np.arctan2(transformed_rotation[1, 0], transformed_rotation[0, 0])
        theta_degree = math.degrees(theta)

        return theta_degree

    def ellipse_xy(self, t:float) -> Tuple[float, float]:
        a = 100
        b = 20
        
        r = -math.pi * (1/1000)*t *1.5
        x = a * math.cos(r)
        y = b * math.sin(r) - 300

        return x,y



class Transform2D:
    def __init__(self, x=0, y=0, delta_angle=0):
        self.x = x
        self.y = y
        self.delta_angle = delta_angle
        self.delta = math.radians(delta_angle)

    def set_data(self, x=0, y=0, delta_angle=0):
        self.x = x
        self.y = y
        self.delta_angle = delta_angle
        self.delta = math.radians(delta_angle)
    
    def matrix(self):
        return np.array([[np.cos(self.delta), -np.sin(self.delta), self.x],
                         [np.sin(self.delta), np.cos(self.delta), self.y],
                         [0, 0, 1]])


def create_mp4(in_dir, out_filename, fps=24):
    path_list = sorted(glob.glob(os.path.join(*[in_dir, '*']))) # ファイルパスをソートしてリストする
    clip = ImageSequenceClip(path_list, fps=fps) # 画像を読み込んで動画を生成
    clip.write_videofile(out_filename, codec='libx264') # 動画をmp4形式で保存


if __name__ == '__main__':

    # ----------------------------
    # 四節リンクを生成し、各点の座標を表示する
#    four_bar_linkage = FourBarLinkage(a=300, b=80, c=300, d=80, e=150, angle_phi=60)
    four_bar_linkage = FourBarLinkage(a=100, b=160, e=100, angle_phi=60, angle_delta=0)
    four_bar_linkage.update_positions()
    # ----------------------------

    # 画像のサイズ（ピクセル）
    width = 800
    height = 600

    # dirフォルダが無い時に新規作成
    dir = './image/'
    if os.path.exists(dir):
        pass
    else:
        os.mkdir(dir)


    # 画像を生成する
    img = np.zeros((height, width, 3), np.uint8)

    # 軸の色
    axis_color = (100, 100, 100)

    # 方眼のステップ（ピクセル）
    grid_step = 50

    # 親座標の角度と平行移動
    angle_delta = -30
    four_bar_linkage.set_delta(angle_delta)

    cv2.namedWindow('panel')
    cv2.createTrackbar('deg', 'panel', 90, 360, lambda x: None)
    cv2.createTrackbar('delta', 'panel', 210, 360, lambda x: None)
    cv2.createTrackbar('Ex', 'panel', 200, 400, lambda x: None)
    cv2.createTrackbar('Ey', 'panel', 30, 100, lambda x: None)

    Ex = -200
    Ey = -200
    angle = 0
    angle_delta = 0

    i : int = 0

    bRec : bool = False

    while True:

        img = np.zeros((height, width, 3), np.uint8)
        img[:,:,:] = 255

        # ---------------------------------------------------------
        # 縦軸を描画する
        for x in range(0, width, grid_step):
            cv2.line(img, (x, 0), (x, height), axis_color, 1)

        # 横軸を描画する
        for y in range(0, height, grid_step):
            cv2.line(img, (0, y), (width, y), axis_color, 1)    
        # ---------------------------------------------------------


        # 角度変更
        x_offset = cv2.getTrackbarPos('Ex', 'panel')
        y_offset = cv2.getTrackbarPos('Ey', 'panel')
        x_in = Ex + x_offset
        y_in = Ey - y_offset

        # ポイントEの座標からΦとδを割り出してリンクの座標を計算する
    #    four_bar_linkage.update_inverse_kinematics(x=x_in, y=y_in)
        four_bar_linkage.update_inverse_kinematics(x=four_bar_linkage.pos_ellipse[0] , y=four_bar_linkage.pos_ellipse[1] )

        four_bar_linkage.update_positions()
        four_bar_linkage.draw(image=img)

        cv2.imshow('link test', img)

        if cv2.waitKey(1) == ord('q'):
            break

        # 画像保存パスを準備
        # 画像を保存
        if bRec == True:
            path = os.path.join(*[dir, str("{:05}".format(i)) + '.jpg'])
            cv2.imwrite(path, img)

        i += 1


    # 動画を作成する
    if bRec == True:
        create_mp4(dir, 'output.mp4', 24)
        shutil.rmtree(dir)

    cv2.destroyAllWindows()


