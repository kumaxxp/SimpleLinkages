#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Linkages_lib.FourBarLinkage as FourBarLinkage
import os
import cv2

import math

import numpy as np
from matplotlib import pyplot as plt
from moviepy.editor import ImageSequenceClip
from mpl_toolkits.mplot3d import Axes3D

import glob

# 動作生成関数
def create_mp4(in_dir, out_filename, fps=24):
    path_list = sorted(glob.glob(os.path.join(*[in_dir, '*']))) # ファイルパスをソートしてリストする
    clip = ImageSequenceClip(path_list, fps=fps) # 画像を読み込んで動画を生成
    clip.write_videofile(out_filename, codec='libx264') # 動画をmp4形式で保存

# 2D表示用クラス
class OpenCV_2DView:
    def __init__(self, width:int = 800, height:int = 600, rec:bool = False):

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

    def draw(self, four_bar:FourBarLinkage):
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
        four_bar.draw(image = self.img)

        # Z軸平面 1 に描画する
        #four_bar.draw(image = self.img)

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


def link_machine():
    print("start four_bar_links")

    cv_2dview = OpenCV_2DView()

    # リンクの長さ比
    # a : b : e = 100 : 160 : 100
    # f : g = 113.13 : 50
    # Z平面の位置
    four_bar = FourBarLinkage(a=0.025313, b=0.04050137, e=0.025313, g=0.010, angle_phi=60, angle_delta=0)
    four_bar.update_positions()

    cv2.namedWindow('panel')
    cv2.createTrackbar('mode', 'panel', 0, 3, lambda x: None)
    cv2.createTrackbar('phi', 'panel', 90, 360, lambda x: None)
    cv2.createTrackbar('delta', 'panel', 210, 360, lambda x: None)
    cv2.createTrackbar('gamma', 'panel', 120, 360, lambda x: None)
    cv2.createTrackbar('Ex', 'panel', 200, 400, lambda x: None)
    cv2.createTrackbar('Ey', 'panel', 30, 100, lambda x: None)

    Ex = -200
    Ey = -200

    while True:

        # 角度変更
        x_offset = cv2.getTrackbarPos('Ex', 'panel')
        y_offset = cv2.getTrackbarPos('Ey', 'panel')
        x_in = Ex + x_offset
        y_in = Ey - y_offset

        # モードの切替
        mode = cv2.getTrackbarPos('mode', 'panel')
        if mode == 0:   # 自動で逆運動で楕円に動く
            four_bar.update_inverse_kinematics(x=four_bar.pos_ellipse[0] , y=four_bar.pos_ellipse[1] )
            four_bar.culc_ellipse()

        elif mode == 1: # 手動で逆運動で操作
            four_bar.update_inverse_kinematics(x=x_in, y=y_in)

        elif mode == 2: # 手動で角度Φ/角度δを操作
            phi = cv2.getTrackbarPos('phi', 'panel')
            delta = cv2.getTrackbarPos('delta', 'panel')
            four_bar.set_phi(phi)
            four_bar.set_delta(delta)

        elif mode == 3: # 手動で角度γ/角度δを操作（駆動軸で位置決定する）
            gamma = cv2.getTrackbarPos('gamma', 'panel')
            delta = cv2.getTrackbarPos('delta', 'panel')
            phi = gamma - (delta-180)
            four_bar.set_phi(phi)
            four_bar.set_delta(delta)

        four_bar.update_positions()
        cv_2dview.draw(four_bar)

        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    link_machine()
