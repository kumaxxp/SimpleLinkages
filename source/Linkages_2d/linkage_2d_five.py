#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Linkages_lib.FiveBarLinkage as FiveBarLinkage
import Linkages_lib.FourBarSubLinkage as FourBarSubLinkage
import os
import cv2

import math

import numpy as np
from moviepy.editor import ImageSequenceClip

import glob

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

# 動作生成関数
def create_mp4(in_dir, out_filename, fps=24):
    path_list = sorted(glob.glob(os.path.join(*[in_dir, '*']))) # ファイルパスをソートしてリストする
    clip = ImageSequenceClip(path_list, fps=fps) # 画像を読み込んで動画を生成
    clip.write_videofile(out_filename, codec='libx264') # 動画をmp4形式で保存

# 2D表示用クラス
class linkage_2d_five:
    def __init__(self, width:int = 1000, height:int = 600, rec:bool = False):

        # dirフォルダが無い時に新規作成
        dir = './image/'
        if os.path.exists(dir):
            pass
        else:
            os.mkdir(dir)

        self.width = width
        self.height = height
        self.rec_cnt : int = 0
        self.bRec : bool = rec

        # 画像を生成する
        self.img = np.zeros((height, width, 3), np.uint8)

        # 軸の色
        self.axis_color = (100, 100, 100)

        # 方眼のステップ（ピクセル）
        self.grid_step = 50

    def draw(self, five_bar_front:FiveBarLinkage, four_bar:FourBarSubLinkage ):
        self.img = np.zeros((self.height, self.width, 3), np.uint8)
        self.img[:,:,:] = 255

        # ---------------------------------------------------------
        # 縦軸を描画する
        for x in range(0, self.width, self.grid_step):
            cv2.line(self.img, (x, 0), (x, self.height), self.axis_color, 1)

        # 横軸を描画する
        for y in range(0, self.height, self.grid_step):
            cv2.line(self.img, (0, y), (self.width, y), self.axis_color, 1)    
        # ---------------------------------------------------------

        # Z軸平面 0 に描画する
        self.draw_link(image = self.img, five_bar = five_bar_front, four_bar=four_bar)

        cv2.imshow('link test', self.img)

    def rec(self):
        # 画像を保存
        if self.bRec == True:
            if self.img.size != 0:
                path = os.path.join(*[dir, str("{:05}".format(self.rec_cnt)) + '.png'])
                scale = 0.5
                img_tmp = self.img.copy()
                re_width  :int = int(img_tmp.shape[1]*scale)
                re_height :int = int(img_tmp.shape[0]*scale)
                img2 = cv2.resize(img_tmp, (re_width, re_height))

                cv2.imwrite(path, img2)

        self.rec_cnt += 1

    def save_movie(self):
        # 動画を作成する
        if self.bRec == True:
            self.create_mp4(dir, 'output.mp4', 24)
            self.shutil.rmtree(dir)

    def _convert_coordinate(self, pos: tuple, offset_x: int = 350, offset_y: int = 50) -> tuple:
        pos_int_x = int(pos[0]*1000*4) + offset_x
        pos_int_y = -int(pos[1]*1000*4) + offset_y
        pos_int = (pos_int_x, pos_int_y)
        return pos_int

    def _convert_coordinate_right(self, pos: tuple, offset_x: int = 800, offset_y: int = 200) -> tuple:
        pos_int_x = int(pos[0]*1000*4) + offset_x
        pos_int_y = -int(pos[1]*1000*4) + offset_y
        pos_int = (pos_int_x, pos_int_y)
        return pos_int

    def _convert_angle(self, angle_st: float, angle_ed: float) -> tuple:
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

    def draw_link(self, image: np.ndarray, five_bar:FiveBarLinkage, four_bar:FourBarSubLinkage) -> None:

        # cv2の座標系に位置を変換する
        # Y座標系を±反転し、画面の中央に原点をシフトする
        pos_B1_int = self._convert_coordinate(five_bar.B1)
        pos_B2_int = self._convert_coordinate(five_bar.B2)
        pos_M1_int = self._convert_coordinate(five_bar.M1)
        pos_M2_int = self._convert_coordinate(five_bar.M2)
        pos_X_int = self._convert_coordinate(five_bar.X)

        pos_A_int = self._convert_coordinate(four_bar.A)
        pos_B_int = self._convert_coordinate(four_bar.B)
        pos_C_int = self._convert_coordinate(four_bar.C)
        pos_D_int = self._convert_coordinate(four_bar.D)
        pos_E_int = self._convert_coordinate(four_bar.E)

        pos_M1i_int = self._convert_coordinate(four_bar.M1)
        pos_Xi_int = self._convert_coordinate(five_bar.Xi)

        pos_Ei_int = self._convert_coordinate(four_bar.Ei)
        pos_Fi_int = self._convert_coordinate(four_bar.Fi)

        # cv2の座標系に回転角を変換する
        # 角度は±反転し、反時計回りで塗りつぶせるように、
        # 開始角度を大きな数値になるように調整する

        # linkを描画する
        cv2.line(image, pt1=pos_B1_int, pt2=pos_B2_int, color=LINK_COLOR_G, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_B1_int, pt2=pos_M1_int, color=LINK_COLOR_R, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_B2_int, pt2=pos_M2_int, color=LINK_COLOR_R, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_M1_int, pt2=pos_X_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_M2_int, pt2=pos_X_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)

        cv2.line(image, pt1=pos_A_int, pt2=pos_B_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_B_int, pt2=pos_C_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_C_int, pt2=pos_D_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_D_int, pt2=pos_A_int, color=LINK_COLOR_R, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_E_int, pt2=pos_B_int, color=LINK_COLOR_B, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)

        cv2.line(image, pt1=pos_B1_int, pt2=pos_M1i_int, color=LINK_COLOR_G, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_M1i_int, pt2=pos_Xi_int, color=LINK_COLOR_G, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)

        cv2.line(image, pt1=pos_B1_int, pt2=pos_Fi_int, color=LINK_COLOR_R, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_Fi_int, pt2=pos_Ei_int, color=LINK_COLOR_R, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)

        # テキスト
        cv2.putText(img = image, text = 'B1', org = pos_B1_int, fontFace=cv2.FONT_HERSHEY_PLAIN, 
            fontScale=1.0, color=PIN_TEXT, thickness=1, lineType=cv2.LINE_AA)
        cv2.putText(img = image, text = 'B2', org = pos_B2_int, fontFace=cv2.FONT_HERSHEY_PLAIN, 
            fontScale=1.0, color=PIN_TEXT, thickness=1, lineType=cv2.LINE_AA)
        cv2.putText(img = image, text = 'M1', org = pos_M1_int, fontFace=cv2.FONT_HERSHEY_PLAIN, 
            fontScale=1.0, color=PIN_TEXT, thickness=1, lineType=cv2.LINE_AA)
        cv2.putText(img = image, text = 'M2', org = pos_M2_int, fontFace=cv2.FONT_HERSHEY_PLAIN, 
            fontScale=1.0, color=PIN_TEXT, thickness=1, lineType=cv2.LINE_AA)
        cv2.putText(img = image, text = 'X', org = pos_X_int, fontFace=cv2.FONT_HERSHEY_PLAIN, 
            fontScale=1.0, color=PIN_TEXT, thickness=1, lineType=cv2.LINE_AA)
        
        pos = (pos_A_int[0]+30, pos_A_int[1])
        cv2.putText(img = image, text = 'A', org = pos, fontFace=cv2.FONT_HERSHEY_PLAIN, 
            fontScale=1.0, color=PIN_TEXT, thickness=1, lineType=cv2.LINE_AA)
        cv2.putText(img = image, text = 'B', org = pos_B_int, fontFace=cv2.FONT_HERSHEY_PLAIN, 
            fontScale=1.0, color=PIN_TEXT, thickness=1, lineType=cv2.LINE_AA)
        cv2.putText(img = image, text = 'C', org = pos_C_int, fontFace=cv2.FONT_HERSHEY_PLAIN, 
            fontScale=1.0, color=PIN_TEXT, thickness=1, lineType=cv2.LINE_AA)
        cv2.putText(img = image, text = 'D', org = pos_D_int, fontFace=cv2.FONT_HERSHEY_PLAIN, 
            fontScale=1.0, color=PIN_TEXT, thickness=1, lineType=cv2.LINE_AA)
        cv2.putText(img = image, text = 'E', org = pos_E_int, fontFace=cv2.FONT_HERSHEY_PLAIN, 
            fontScale=1.0, color=PIN_TEXT, thickness=1, lineType=cv2.LINE_AA)

        cv2.circle(image, center=pos_B1_int, radius=PIN_RADIUS, color=PIN_COLOR, thickness=1, lineType=cv2.LINE_AA, shift=0)
        cv2.circle(image, center=pos_B2_int, radius=PIN_RADIUS, color=PIN_COLOR, thickness=1, lineType=cv2.LINE_AA, shift=0)
        cv2.circle(image, center=pos_M1_int, radius=PIN_RADIUS, color=PIN_COLOR, thickness=PIN_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.circle(image, center=pos_M2_int, radius=PIN_RADIUS, color=PIN_COLOR, thickness=PIN_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.circle(image, center=pos_X_int, radius=PIN_RADIUS, color=PIN_COLOR, thickness=PIN_WIDTH, lineType=cv2.LINE_AA, shift=0)

        cv2.circle(image, center=pos_A_int, radius=PIN_RADIUS, color=PIN_COLOR, thickness=PIN_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.circle(image, center=pos_B_int, radius=PIN_RADIUS, color=PIN_COLOR, thickness=PIN_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.circle(image, center=pos_C_int, radius=PIN_RADIUS, color=PIN_COLOR, thickness=PIN_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.circle(image, center=pos_D_int, radius=PIN_RADIUS, color=PIN_COLOR, thickness=PIN_WIDTH, lineType=cv2.LINE_AA, shift=0)

        # 足先点Eの座標
        pos = (pos_E_int[0]+30, pos_E_int[1])
        cv2.putText(image, text = str(four_bar.E), org = pos, fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.0, color=PIN_TEXT, thickness=1, lineType=cv2.LINE_AA)

        pos = (pos_X_int[0]+30, pos_X_int[1])
        cv2.putText(image, text = str(four_bar.X), org = pos, fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.0, color=PIN_TEXT, thickness=1, lineType=cv2.LINE_AA)

        # B1,B2の角度Θ1/Θ2
        pos = (pos_B1_int[0]+30, pos_B1_int[1])
        cv2.putText(image, text = str(five_bar.theta1), org = pos, fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.0, color=PIN_TEXT, thickness=1, lineType=cv2.LINE_AA)

        pos = (pos_B2_int[0]+30, pos_B2_int[1])
        cv2.putText(image, text = str(five_bar.theta2), org = pos, fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.0, color=PIN_TEXT, thickness=1, lineType=cv2.LINE_AA)

        pos = (pos_M1i_int[0]+30, pos_M1i_int[1])
        cv2.putText(image, text = str(four_bar.M1), org = pos, fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.0, color=PIN_TEXT, thickness=1, lineType=cv2.LINE_AA)

        pos = (pos_Xi_int[0]+30, pos_Xi_int[1])
        cv2.putText(image, text = str(five_bar.Xi), org = pos, fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.0, color=PIN_TEXT, thickness=1, lineType=cv2.LINE_AA)

        pos = (pos_B1_int[0], pos_B1_int[1]+50)
        txt = str(four_bar.theta1) + str(four_bar.phi)
        cv2.putText(image, text = txt, org = pos, fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.0, color=PIN_TEXT, thickness=1, lineType=cv2.LINE_AA)
