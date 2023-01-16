#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Linkages_lib.FourBarLinkage as FourBarLinkage
import os
import cv2

import math

import numpy as np
from matplotlib import pyplot as plt
from moviepy.editor import ImageSequenceClip

def link_machine():
    print("start four_bar_links")

    # リンクの長さ比
    # a : b : e = 100 : 160 : 100
    # f : g = 113.13 : 50
    four_bar = FourBarLinkage(a=100, b=160, e=100, angle_phi=60, angle_delta=0)
    four_bar.update_positions()

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
        four_bar.draw(image=img)

        cv2.imshow('link test', img)

        if cv2.waitKey(1) == ord('q'):
            break

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


if __name__ == '__main__':
    link_machine()
