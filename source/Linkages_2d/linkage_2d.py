#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Linkages_lib.FourBarLinkage as FourBarLinkage
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
class linkage_2d:
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

    def draw(self, four_bar_front:FourBarLinkage, four_bar_rear:FourBarLinkage ):
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
        self.draw_link(image = self.img, four_bar = four_bar_front)

        # Z軸平面 1 に描画する
        if four_bar_rear != None:
            self.draw_link(image = self.img, four_bar = four_bar_rear)

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

    def _convert_coordinate(self, pos: tuple, offset_x: int = 350, offset_y: int = 200) -> tuple:
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

    def draw_link(self, image: np.ndarray, four_bar:FourBarLinkage) -> None:

        # cv2の座標系に位置を変換する
        # Y座標系を±反転し、画面の中央に原点をシフトする
        pos_A_int = self._convert_coordinate(four_bar.A)
        pos_B_int = self._convert_coordinate(four_bar.B)
        pos_C_int = self._convert_coordinate(four_bar.C)
        pos_D_int = self._convert_coordinate(four_bar.D)
        pos_E_int = self._convert_coordinate(four_bar.E)
        pos_F_int = self._convert_coordinate(four_bar.F)
        pos_G_int = self._convert_coordinate(four_bar.G)
        pos_H_int = self._convert_coordinate(four_bar.H)
        pos_I_int = self._convert_coordinate(four_bar.I)
        pos_J_int = self._convert_coordinate(four_bar.J)
        pos_K_int = self._convert_coordinate(four_bar.K)

        # cv2の座標系に回転角を変換する
        # 角度は±反転し、反時計回りで塗りつぶせるように、
        # 開始角度を大きな数値になるように調整する
        angle_delta_st, angle_delta_ed = self._convert_angle(0, four_bar.angle_delta)
        angle_gamma_st, angle_gamma_ed = self._convert_angle(0, four_bar.angle_gamma)

        angle_A_st, angle_A_ed = self._convert_angle(four_bar.angle_A_st, four_bar.angle_A_ed)
        angle_B_st, angle_B_ed = self._convert_angle(four_bar.angle_B_st, four_bar.angle_B_ed)
        angle_C_st, angle_C_ed = self._convert_angle(four_bar.angle_C_st, four_bar.angle_C_ed)
        angle_D_st, angle_D_ed = self._convert_angle(four_bar.angle_D_st, four_bar.angle_D_ed)

        # 中心座標
        cv2.circle(image, center=pos_D_int, radius=CENTER_RADIUS, color=CENTER_COLOR, thickness=1, lineType=cv2.LINE_AA, shift=0)
        cv2.ellipse(image, center=pos_D_int, axes=(CENTER_RADIUS, CENTER_RADIUS),
            angle=0, startAngle=angle_delta_st, endAngle=angle_delta_ed, color=CENTER_COLOR_ARC, thickness=-1, lineType=cv2.LINE_AA)
        cv2.ellipse(image, center=pos_F_int, axes=(CENTER_RADIUS, CENTER_RADIUS),
            angle=0, startAngle=angle_gamma_st, endAngle=angle_gamma_ed, color=CENTER_COLOR_ARC, thickness=-1, lineType=cv2.LINE_AA)

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
        #cv2.line(image, pt1=pos_J_int, pt2=pos_C_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_J_int, pt2=pos_E_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_J_int, pt2=pos_K_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)

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
        cv2.circle(image, center=pos_J_int, radius=G_RADIUS, color=G_COLOR, thickness=PIN_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.circle(image, center=pos_K_int, radius=G_RADIUS, color=G_COLOR, thickness=PIN_WIDTH, lineType=cv2.LINE_AA, shift=0)
        
        # 対角線
        #cv2.line(image, pt1=pos_D_int, pt2=pos_B_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)

        # 重心からエンドエフェクトまで
        cv2.line(image, pt1=pos_I_int, pt2=pos_J_int, color=G_COLOR, thickness=1, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_I_int, pt2=pos_K_int, color=G_COLOR, thickness=1, lineType=cv2.LINE_AA, shift=0)
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
        cv2.putText(img = image, text = 'I', org = pos_I_int, fontFace=cv2.FONT_HERSHEY_PLAIN, 
            fontScale=1.0, color=PIN_TEXT, thickness=1, lineType=cv2.LINE_AA)
        cv2.putText(img = image, text = 'J', org = pos_J_int, fontFace=cv2.FONT_HERSHEY_PLAIN, 
            fontScale=1.0, color=PIN_TEXT, thickness=1, lineType=cv2.LINE_AA)
        cv2.putText(img = image, text = 'K', org = pos_K_int, fontFace=cv2.FONT_HERSHEY_PLAIN, 
            fontScale=1.0, color=PIN_TEXT, thickness=1, lineType=cv2.LINE_AA)

        pos_int = (int(pos_A_int[0]), int(pos_A_int[1]) + 20)
        cv2.putText(img = image, text = str(four_bar.angle_A), org = pos_int, fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.0, color=PIN_TEXT, thickness=1, lineType=cv2.LINE_AA)
        pos_int = (int(pos_B_int[0]), int(pos_B_int[1]) + 20)
        cv2.putText(img = image, text = str(four_bar.angle_B), org = pos_int, fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.0, color=PIN_TEXT, thickness=1, lineType=cv2.LINE_AA)

        # 座標表示
        pos_int = (int(pos_E_int[0]), int(pos_E_int[1]) + 20)
        cv2.putText(img = image, text = str(four_bar.E), 
            org = pos_int, fontFace=cv2.FONT_HERSHEY_PLAIN, 
            fontScale=1.0, color=PIN_TEXT, thickness=1, lineType=cv2.LINE_AA)

        pos_int = (int(pos_D_int[0]), int(pos_D_int[1]) + 20)
        cv2.putText(img = image, text = str(four_bar.D), 
            org = pos_int, fontFace=cv2.FONT_HERSHEY_PLAIN, 
            fontScale=1.0, color=PIN_TEXT, thickness=1, lineType=cv2.LINE_AA)

        pos_ellipse_int = self._convert_coordinate(four_bar.pos_ellipse)
        cv2.circle(image, center=pos_ellipse_int, radius=PIN_RADIUS, color=PIN_COLOR, thickness=1, lineType=cv2.LINE_AA, shift=0)

        # 鉛直方向の角度を表示
        pos_int = (int(pos_E_int[0]), int(pos_E_int[1]) + 40)
        cv2.putText(img = image, text = str(four_bar.angle_alpha), 
            org = pos_int, fontFace=cv2.FONT_HERSHEY_PLAIN, 
            fontScale=1.0, color=PIN_TEXT, thickness=1, lineType=cv2.LINE_AA)


        # 脚の角度を鉛直方向に固定した場合の画像
        # 画面の少し右方向に並べて表示する
        pos_rA_int = self._convert_coordinate_right(four_bar.rA)
        pos_rB_int = self._convert_coordinate_right(four_bar.rB)
        pos_rC_int = self._convert_coordinate_right(four_bar.rC)
        pos_rD_int = self._convert_coordinate_right(four_bar.rD)
        pos_rE_int = self._convert_coordinate_right(four_bar.rE)

        pos_rF_int = self._convert_coordinate_right(four_bar.rF)
        pos_rG_int = self._convert_coordinate_right(four_bar.rG)
        pos_rH_int = self._convert_coordinate_right(four_bar.rH)
        pos_rI_int = self._convert_coordinate_right(four_bar.rI)
        pos_rJ_int = self._convert_coordinate_right(four_bar.rJ)
        pos_rK_int = self._convert_coordinate_right(four_bar.rK)

        pos_int = (pos_rI_int[0], pos_rI_int[1]+100)

        cv2.line(image, pt1=pos_rA_int, pt2=pos_rB_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_rB_int, pt2=pos_rC_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_rC_int, pt2=pos_rD_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_rD_int, pt2=pos_rA_int, color=LINK_COLOR_R, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_rB_int, pt2=pos_rE_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_rF_int, pt2=pos_rG_int, color=LINK_COLOR_R, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_rD_int, pt2=pos_rH_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_rG_int, pt2=pos_rH_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_rD_int, pt2=pos_rF_int, color=LINK_COLOR_G, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_rI_int, pt2=pos_rJ_int, color=G_COLOR, thickness=1, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_rI_int, pt2=pos_rK_int, color=G_COLOR, thickness=1, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_rI_int, pt2=pos_rE_int, color=G_COLOR, thickness=1, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_rJ_int, pt2=pos_rE_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_rJ_int, pt2=pos_rC_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_rJ_int, pt2=pos_rK_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)

        cv2.line(image, pt1=pos_rI_int, pt2=pos_int, color=LINK_COLOR_B , thickness=3, lineType=cv2.LINE_AA, shift=0)

        cv2.circle(image, center=pos_rD_int, radius=PIN_RADIUS, color=PIN_COLOR, thickness=PIN_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.circle(image, center=pos_rI_int, radius=G_RADIUS, color=G_COLOR, thickness=PIN_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.circle(image, center=pos_rJ_int, radius=G_RADIUS, color=PIN_COLOR, thickness=PIN_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.circle(image, center=pos_rK_int, radius=G_RADIUS, color=PIN_COLOR, thickness=PIN_WIDTH, lineType=cv2.LINE_AA, shift=0)
