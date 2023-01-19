#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import os
import shutil

from moviepy.editor import ImageSequenceClip

from PIL import Image
import glob
import numpy as np
from matplotlib import pyplot as plt

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

G_RADIUS = 15
G_COLOR = (0, 0, 200)

RECT_COLOR = (50, 50, 50)

#モータの短辺の長さ(m)
RECT_LEN:float = 0.020
MOTOR_DEF:float = 0.01986
MOTOR_GUIDE:float = 0.004

# 四節リンクを表すクラス
class FourBarLinkage:
    def __init__(self, a, b, e, g, angle_phi, angle_delta):
        self.a : float = a
        self.b : float = b
        self.c : float = a
        self.d : float = b
        self.e : float = e

        self.f : float = math.sqrt((MOTOR_DEF ** 2) + (MOTOR_DEF + MOTOR_GUIDE)**2)    # 113.13
        self.g : float = g

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
        self.F = (self.D[0] + MOTOR_DEF, self.D[1] + MOTOR_DEF + MOTOR_GUIDE)
        self.G = (self.F[0] + self.g * math.cos(self.gamma), self.F[1] + self.g * math.sin(self.gamma))
        self.H = (self.D[0] + self.g * math.cos(self.gamma), self.D[1] + self.g * math.sin(self.gamma))

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
        self.angle_gamma = self.angle_phi + self.angle_delta - 180
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

        self.G = (self.F[0] + self.g * math.cos(self.gamma), self.F[1] + self.g * math.sin(self.gamma))
        self.H = (self.D[0] + self.g * math.cos(self.gamma), self.D[1] + self.g * math.sin(self.gamma))

        self.I = ((self.F[0] - self.D[0]) /2 ,(self.F[1] - self.D[1]) /2) 

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
        pos_int_x = int(pos[0]*1000*4) + offset_x
        pos_int_y = -int(pos[1]*1000*4) + offset_y
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
        pos_H_int = self._convert_coordinate(self.H)
        pos_I_int = self._convert_coordinate(self.I)

        # cv2の座標系に回転角を変換する
        # 角度は±反転し、反時計回りで塗りつぶせるように、
        # 開始角度を大きな数値になるように調整する
        angle_delta_st, angle_delta_ed = self._convert_angle(0, self.angle_delta)
        angle_gamma_st, angle_gamma_ed = self._convert_angle(0, self.angle_gamma)

        angle_A_st, angle_A_ed = self._convert_angle(self.angle_A_st, self.angle_A_ed)
        angle_B_st, angle_B_ed = self._convert_angle(self.angle_B_st, self.angle_B_ed)
        angle_C_st, angle_C_ed = self._convert_angle(self.angle_C_st, self.angle_C_ed)
        angle_D_st, angle_D_ed = self._convert_angle(self.angle_D_st, self.angle_D_ed)

        # 中心座標
        cv2.circle(image, center=pos_D_int, radius=CENTER_RADIUS, color=CENTER_COLOR, thickness=1, lineType=cv2.LINE_AA, shift=0)
        cv2.ellipse(image, center=pos_D_int, axes=(CENTER_RADIUS, CENTER_RADIUS),
            angle=0, startAngle=angle_delta_st, endAngle=angle_delta_ed, color=CENTER_COLOR_ARC, thickness=-1, lineType=cv2.LINE_AA)
        cv2.ellipse(image, center=pos_F_int, axes=(CENTER_RADIUS, CENTER_RADIUS),
            angle=0, startAngle=angle_gamma_st, endAngle=angle_gamma_ed, color=CENTER_COLOR_ARC, thickness=-1, lineType=cv2.LINE_AA)

        # モーターを互い違いに2配置するイメージ
    #    pos1 = (pos_D_int[0] - RECT_LEN, pos_D_int[1] -RECT_LEN)
    #    pos2 = (pos_D_int[0] + RECT_LEN*3, pos_D_int[1] +RECT_LEN)
    #    cv2.rectangle(image, pt1=pos1, pt2=pos2, color=RECT_COLOR, thickness=1, lineType=cv2.LINE_4, shift=0)

    #    pos1 = (pos_D_int[0] - RECT_LEN, pos_D_int[1] -RECT_LEN*3)
    #    pos2 = (pos_D_int[0] + RECT_LEN*3, pos_D_int[1] -RECT_LEN)
    #    cv2.rectangle(image, pt1=pos1, pt2=pos2, color=RECT_COLOR, thickness=1, lineType=cv2.LINE_4, shift=0)

    #    pos_motor = (pos_D_int[0] + RECT_LEN*2, pos_D_int[1] - RECT_LEN*2)
    #    cv2.circle(image, center=pos_motor, radius=PIN_RADIUS, color=CENTER_COLOR, thickness=1, lineType=cv2.LINE_AA, shift=0)

        # linkを描画する
        cv2.line(image, pt1=pos_A_int, pt2=pos_B_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_B_int, pt2=pos_C_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_C_int, pt2=pos_D_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_D_int, pt2=pos_A_int, color=LINK_COLOR_R, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_B_int, pt2=pos_E_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_F_int, pt2=pos_G_int, color=LINK_COLOR_R, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_D_int, pt2=pos_H_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_G_int, pt2=pos_H_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_D_int, pt2=pos_F_int, color=LINK_COLOR_G, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)

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
        cv2.circle(image, center=pos_I_int, radius=G_RADIUS, color=G_COLOR, thickness=PIN_WIDTH, lineType=cv2.LINE_AA, shift=0)

        # 対角線
        cv2.line(image, pt1=pos_D_int, pt2=pos_B_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)

        # 重心からエンドエフェクトまで
        cv2.line(image, pt1=pos_I_int, pt2=pos_E_int, color=G_COLOR, thickness=1, lineType=cv2.LINE_AA, shift=0)

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
        cv2.putText(img = image, text = 'F', org = pos_F_int, fontFace=cv2.FONT_HERSHEY_PLAIN, 
            fontScale=1.0, color=PIN_TEXT, thickness=1, lineType=cv2.LINE_AA)
        cv2.putText(img = image, text = 'G', org = pos_G_int, fontFace=cv2.FONT_HERSHEY_PLAIN, 
            fontScale=1.0, color=PIN_TEXT, thickness=1, lineType=cv2.LINE_AA)
        cv2.putText(img = image, text = 'H', org = pos_H_int, fontFace=cv2.FONT_HERSHEY_PLAIN, 
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

        
        pos_ellipse_int = self._convert_coordinate(self.pos_ellipse)
        cv2.circle(image, center=pos_ellipse_int, radius=PIN_RADIUS, color=PIN_COLOR, thickness=1, lineType=cv2.LINE_AA, shift=0)

    def culc_ellipse(self):
        self.pos_ellipse = self.ellipse_xy(self.t)
        self.t += 1

    def ellipse_xy(self, t:float) -> Tuple[float, float]:
        a = 0.04
        b = 0.01
        
        r = -math.pi * (1/1000)*t *1.5
        x = a * math.cos(r)
        y = b * math.sin(r) - 0.070

        return x,y

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

    cv2.namedWindow('panel')
    cv2.createTrackbar('mode', 'panel', 0, 3, lambda x: None)
    cv2.createTrackbar('phi', 'panel', 90, 360, lambda x: None)
    cv2.createTrackbar('delta', 'panel', 210, 360, lambda x: None)
    cv2.createTrackbar('gamma', 'panel', 120, 360, lambda x: None)
    cv2.createTrackbar('Ex', 'panel', 200, 400, lambda x: None)
    cv2.createTrackbar('Ey', 'panel', 30, 100, lambda x: None)

    Ex = -200
    Ey = -200

    i : int = 0

    # グラフの準備 ----------------
    plt.ion()

    figure, (ax1,ax2,ax3) = plt.subplots(nrows = 3, figsize=(8,6))
    line1, = ax1.plot((-100,0), (-360,360), label="$\gamma$")
    line2, = ax2.plot((-100,0), (-360,360), label="$\phi$")
    line3, = ax3.plot((-100,0), (-360,360), label="$\delta$")

    line1_1, = ax1.plot((-100,0), (-360,360), label="$vel- \gamma$")

    plt.xlabel("X",fontsize=18)
    plt.ylabel("angle",fontsize=18) 

    hans, labs = ax1.get_legend_handles_labels()
    ax1.legend(handles=hans, labels=labs)

    hans, labs = ax2.get_legend_handles_labels()
    ax2.legend(handles=hans, labels=labs)
    
    hans, labs = ax3.get_legend_handles_labels()
    ax3.legend(handles=hans, labels=labs)

    ar_data_y1 = np.zeros(100)
    ar_data_y2 = np.zeros(100)
    ar_data_y3 = np.zeros(100)

    ar_data_y1_1 = np.zeros(100)
    ar_data_x = np.array(range(-100,0))

    # -----------------------------

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

        # モードの切替
        mode = cv2.getTrackbarPos('mode', 'panel')
        if mode == 0:   # 自動で逆運動で楕円に動く
            four_bar_linkage.update_inverse_kinematics(x=four_bar_linkage.pos_ellipse[0] , y=four_bar_linkage.pos_ellipse[1] )
            four_bar_linkage.culc_ellipse()

        elif mode == 1: # 手動で逆運動で操作
            four_bar_linkage.update_inverse_kinematics(x=x_in, y=y_in)

        elif mode == 2: # 手動で角度Φ/角度δを操作
            phi = cv2.getTrackbarPos('phi', 'panel')
            delta = cv2.getTrackbarPos('delta', 'panel')
            four_bar_linkage.set_phi(phi)
            four_bar_linkage.set_delta(delta)

        elif mode == 3: # 手動で角度γ/角度δを操作（駆動軸で位置決定する）
            gamma = cv2.getTrackbarPos('gamma', 'panel')
            delta = cv2.getTrackbarPos('delta', 'panel')
            phi = gamma - (delta-180)
            four_bar_linkage.set_phi(phi)
            four_bar_linkage.set_delta(delta)

        four_bar_linkage.update_positions()
        four_bar_linkage.draw(image=img)

        cv2.imshow('link test', img)

        if cv2.waitKey(1) == ord('q'):
            break

        # データをグラフ表示 ---------------------------------------
        ar_data_y1 = np.roll(ar_data_y1, -1)
        ar_data_y1[-1] = four_bar_linkage.angle_gamma

        ar_data_y2 = np.roll(ar_data_y2, -1)
        ar_data_y2[-1] = four_bar_linkage.angle_phi

        ar_data_y3 = np.roll(ar_data_y3, -1)
        ar_data_y3[-1] = four_bar_linkage.angle_delta

        # 角速度
        vel_1 = ar_data_y1[-2] - ar_data_y1[-1]
        ar_data_y1_1 = np.roll(ar_data_y1_1, -1)
        ar_data_y1_1[-1] = vel_1*100

        line1.set_xdata(ar_data_x)
        line1.set_ydata(ar_data_y1)
        line1_1.set_xdata(ar_data_x)
        line1_1.set_ydata(ar_data_y1_1)

        line2.set_xdata(ar_data_x)
        line2.set_ydata(ar_data_y2)

        line3.set_xdata(ar_data_x)
        line3.set_ydata(ar_data_y3)

    #    figure.canvas.draw()
    #    figure.canvas.flush_events()

        # ---------------------------------------------------------

        # 画像保存パスを準備
        # 画像を保存
        if bRec == True:
            if img.size != 0:
                path = os.path.join(*[dir, str("{:05}".format(i)) + '.png'])
                scale = 0.5
                img_tmp = img.copy()
                re_width  :int = int(img_tmp.shape[1]*scale)
                re_height :int = int(img_tmp.shape[0]*scale)
                img2 = cv2.resize(img_tmp, (re_width, re_height))

                cv2.imwrite(path, img2)

        i += 1

    # 動画を作成する
    if bRec == True:
        create_mp4(dir, 'output.mp4', 24)
        shutil.rmtree(dir)

    cv2.destroyAllWindows()


