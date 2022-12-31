import cv2
import numpy as np

import math
from typing import Tuple
from typing import List

import math

from clink import CLink
from cpin import CPin

import math

LINK_COLOR = (100, 100, 100)
LINK_WIDTH = 2

# 四節リンクを表すクラス
class FourBarLinkage:
    def __init__(self, a, b, c, d, phi):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.phi = phi
        
        # 各点の座標を表す変数を定義する
        self.D = (0, 0)
        self.A = (a, 0)
        self.B = (0, 0)
        self.C = (d * math.cos(phi), d * math.sin(phi))
                
    def update_positions(self):
        self.C = (self.d * math.cos(self.phi), self.d * math.sin(self.phi))

        # 三角形ABCを作る
        AB = self.a - self.C[0]
        BC = self.c
        AC = self.d
        
        # 余弦定理で角Cを求める
        cos_C = (AB**2 + AC**2 - BC**2) / (2 * AB * AC)
        
        # コサイン値が-1から1の範囲内に収まっているかを確認する
        if cos_C < -1 or cos_C > 1:
            # 範囲外の場合は、-1から1の範囲内に修正する
            cos_C = max(-1, min(cos_C, 1))

        C = math.acos(cos_C)

        # 余弦定理で角Bを求める
        cos_B = (BC**2 + AC**2 - AB**2) / (2 * BC * AC)
        # コサイン値が-1から1の範囲内に収まっているかを確認する
        if cos_B < -1 or cos_B > 1:
            # 範囲外の場合は、-1から1の範囲内に修正する
            cos_B = max(-1, min(cos_B, 1))

        B = math.acos(cos_B)
        
        # 点Bを求める
        x = self.a - AC * math.cos(C)
        y = AC * math.sin(C)
        
        self.B = (x, y)
        
    def set_phi(self, phi):
        self.phi = phi
        
        self.update_positions()
        
    def _convert_coordinate(self, pos: tuple, offset_x: int = 0, offset_y: int = 600) -> tuple:
        pos_int_x = int(pos[0]) + offset_x
        pos_int_y = -int(pos[1]) + offset_y
        pos_int = (pos_int_x, pos_int_y)
        return pos_int
        

    def draw(self, image: np.ndarray) -> None:

        pos_A_int = self._convert_coordinate(self.A)
        pos_B_int = self._convert_coordinate(self.B)
        pos_C_int = self._convert_coordinate(self.C)
        pos_D_int = self._convert_coordinate(self.D)

        # linkを描画する
        cv2.line(image, pt1=pos_A_int, pt2=pos_B_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_B_int, pt2=pos_C_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_C_int, pt2=pos_D_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_D_int, pt2=pos_A_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)



if __name__ == '__main__':

    # ----------------------------
    # 四節リンクを生成し、各点の座標を表示する
    four_bar_linkage = FourBarLinkage(a=200, b=100, c=160, d=120, phi=math.radians(60))
    four_bar_linkage.update_positions()
    print(four_bar_linkage.D)  # (0, 0)
    print(four_bar_linkage.A)  # (10, 0)
    print(four_bar_linkage.B)  # (5.0, 5.0)
    print(four_bar_linkage.C)  # (7.0710678118654755, 4.0)

    # リンクの角度を設定し、各点の座標を表示する
    print(four_bar_linkage.D)  # (0, 0)
    print(four_bar_linkage.A)  # (10, 0)
    print(four_bar_linkage.B)  # (7.0710678118654755, 4.0)
    print(four_bar_linkage.C)  # (7.0710678118654755, 4.0)

    # ----------------------------

    # 画像のサイズ（ピクセル）
    width = 800
    height = 600

    # 画像を生成する
    img = np.zeros((height, width, 3), np.uint8)

    # 軸の色
    axis_color = (100, 100, 100)

    # 方眼のステップ（ピクセル）
    grid_step = 50


    cv2.namedWindow('panel')
    cv2.createTrackbar('deg', 'panel', 0, 360, lambda x: None)

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
        angle = cv2.getTrackbarPos('deg', 'panel') 

        radian = math.radians(angle)

        four_bar_linkage.set_phi(radian)
        four_bar_linkage.update_positions()
        four_bar_linkage.draw(image = img)

        cv2.imshow('link test', img)

        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()


