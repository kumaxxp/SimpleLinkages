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
LINK_COLOR_G = (0, 0, 255)
LINK_WIDTH = 2

PIN_RADIUS = 30
PIN_RADIUS_PHI = 20
PIN_COLOR = (100, 100, 100)
PIN_COLOR_ARC = (255, 100, 100)
PIN_COLOR_PHI1 = (100, 255, 100)
PIN_COLOR_PHI2 = (100, 100, 255)
PIN_TEXT = (0, 0, 0)
PIN_WIDTH = 1

# 四節リンクを表すクラス
class FourBarLinkage:
    def __init__(self, a, b, c, d, angle_phi):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = b
        self.phi = math.radians(angle_phi)
        
        # 各点の座標を表す変数を定義する
        self.D = (0, 0)
        self.A = (a, 0)
        self.B = (0, 0)
        self.C = (d * math.cos(angle_phi), d * math.sin(angle_phi))

        # 各点の角度を表す変数を定義する
#        self.angle_D = angle_phi
#        self.angle_A = 0
#        self.angle_B = 0
#        self.angle_C = 0
        self.phi = math.radians(angle_phi)

#        self.angle_phi1 = 0
        self.angle_phi2 = 0
        self.angle_phi  = angle_phi

        self.update_positions()


    def update_positions(self):
        # 点Cを求める
        self.C = (self.d * math.cos(self.phi), self.d * math.sin(self.phi))
        h = math.sqrt((self.C[0] - self.a)**2 + self.C[1]**2)

        # 余弦定理で角Bを求める
        cos_B = (self.b**2 + self.c**2 - h**2) / (2 * self.b * self.c)
        # コサイン値が-1から1の範囲内に収まっているかを確認する
        if cos_B < -1 or cos_B > 1:
            # 範囲外の場合は、-1から1の範囲内に修正する
            cos_B = max(-1, min(cos_B, 1))

        B = math.acos(cos_B)
        self.angle_B = math.degrees(B)

        cos_DCA = (self.d**2 + h**2 - self.a**2) / (2 * self.d * h)
        # コサイン値が-1から1の範囲内に収まっているかを確認する
        if cos_DCA < -1 or cos_DCA > 1:
            # 範囲外の場合は、-1から1の範囲内に修正する
            cos_DCA = max(-1, min(cos_DCA, 1))

        DCA = math.acos(cos_DCA)
        angle_DCA = math.degrees(DCA)

        cos_ACB = (self.c**2 + h**2 - self.b**2) / (2 * self.c * h)
        # コサイン値が-1から1の範囲内に収まっているかを確認する
        if cos_ACB < -1 or cos_ACB > 1:
            # 範囲外の場合は、-1から1の範囲内に修正する
            cos_ACB = max(-1, min(cos_ACB, 1))

        ACB = math.acos(cos_ACB)
        angle_ACB = math.degrees(ACB)

        self.angle_C = angle_DCA + angle_ACB

        self.angle_A = 360 - self.angle_C - self.angle_B - self.angle_phi
        
        # 点Bを求める
        theta = math.radians(180.0-self.angle_A)
        x = self.a + self.b * math.cos(theta)
        y = self.b * math.sin(theta)
        
        self.B = (x, y)

        # Θ1の角度を求める
        self.angle_phi1 = math.degrees(math.atan2(self.B[1], self.B[0]))
        self.angle_phi2 = self.angle_phi - self.angle_phi1

        # -------------------------------------
        # 頂点Eを計算する
        Ex = self.A[0] - math.cos(theta) * self.e
        Ey = -math.sin(theta) * self.e

        self.E = (Ex,Ey) 


        a_chk = math.sqrt((self.A[0] - self.D[0])**2 + (self.A[1] - self.D[1])**2)
        b_chk = math.sqrt((self.B[0] - self.A[0])**2 + (self.B[1] - self.A[1])**2)
        c_chk = math.sqrt((self.C[0] - self.B[0])**2 + (self.C[1] - self.B[1])**2)
        d_chk = math.sqrt((self.D[0] - self.C[0])**2 + (self.D[1] - self.C[1])**2)
    #    print(a_chk, b_chk, c_chk, d_chk)
        print(self.C[0], self.C[1])

    def set_phi(self, angle):
        # Φの角度は頂点Dの角度として保存する
        self.angle_phi = angle
        self.phi = math.radians(angle)

        self.update_positions()
        
    def _convert_coordinate(self, pos: tuple, offset_x: int = 200, offset_y: int = 400) -> tuple:
        pos_int_x = int(pos[0]) + offset_x
        pos_int_y = -int(pos[1]) + offset_y
        pos_int = (pos_int_x, pos_int_y)
        return pos_int

    def draw(self, image: np.ndarray) -> None:

        pos_A_int = self._convert_coordinate(self.A)
        pos_B_int = self._convert_coordinate(self.B)
        pos_C_int = self._convert_coordinate(self.C)
        pos_D_int = self._convert_coordinate(self.D)
        pos_E_int = self._convert_coordinate(self.E)

        # linkを描画する
        cv2.line(image, pt1=pos_A_int, pt2=pos_B_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_B_int, pt2=pos_C_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_C_int, pt2=pos_D_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_D_int, pt2=pos_A_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.line(image, pt1=pos_A_int, pt2=pos_E_int, color=LINK_COLOR, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)

        # 頂点Dを描画する。Φ/Φ1/Φ2を表示

        cv2.circle(image, center=pos_A_int, radius=PIN_RADIUS, color=PIN_COLOR, thickness=PIN_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.ellipse(image, center=pos_A_int, axes=(PIN_RADIUS, PIN_RADIUS),
            angle=0, startAngle=-180, endAngle=int(self.angle_A)-180, color=PIN_COLOR_ARC, thickness=-1, lineType=cv2.LINE_AA)

        cv2.circle(image, center=pos_B_int, radius=PIN_RADIUS, color=PIN_COLOR, thickness=PIN_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.ellipse(image, center=pos_B_int, axes=(PIN_RADIUS, PIN_RADIUS),
            angle=0, startAngle=int(self.angle_A), endAngle=int(self.angle_B+self.angle_A), color=PIN_COLOR_ARC, thickness=-1, lineType=cv2.LINE_AA)

        cv2.circle(image, center=pos_C_int, radius=PIN_RADIUS, color=PIN_COLOR, thickness=PIN_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.ellipse(image, center=pos_C_int, axes=(PIN_RADIUS, PIN_RADIUS),
            angle=0, startAngle=180-int(self.angle_phi), endAngle=self.angle_phi+self.angle_C-180, color=PIN_COLOR_ARC, thickness=-1, lineType=cv2.LINE_AA)

        cv2.circle(image, center=pos_D_int, radius=PIN_RADIUS, color=PIN_COLOR, thickness=PIN_WIDTH, lineType=cv2.LINE_AA, shift=0)
        cv2.ellipse(image, center=pos_D_int, axes=(PIN_RADIUS, PIN_RADIUS),
            angle=0, startAngle=0, endAngle=-int(self.angle_phi), color=PIN_COLOR_ARC, thickness=-1, lineType=cv2.LINE_AA)
        cv2.ellipse(image, center=pos_D_int, axes=(PIN_RADIUS_PHI, PIN_RADIUS_PHI),
            angle=0, startAngle=-int(self.angle_phi1), endAngle=-int(self.angle_phi2)-int(self.angle_phi1), color=PIN_COLOR_PHI2, thickness=-1, lineType=cv2.LINE_AA)
        cv2.ellipse(image, center=pos_D_int, axes=(PIN_RADIUS_PHI, PIN_RADIUS_PHI),
            angle=0, startAngle=0, endAngle=-int(self.angle_phi1), color=PIN_COLOR_PHI1, thickness=-1, lineType=cv2.LINE_AA)

        cv2.circle(image, center=pos_E_int, radius=PIN_RADIUS, color=PIN_COLOR, thickness=PIN_WIDTH, lineType=cv2.LINE_AA, shift=0)

        # 対角線
        cv2.line(image, pt1=pos_D_int, pt2=pos_B_int, color=LINK_COLOR_G, thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)

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

#        cv2.ellipse(image, center=pos_B_int, axes=(PIN_RADIUS, PIN_RADIUS),
#            angle=0, startAngle=int(self.angle_A), endAngle=-int(-180-self.angle_B+self.angle_A), color=PIN_COLOR_PHI2, thickness=-1, lineType=cv2.LINE_AA)

#        cv2.circle(image, center=pos_C_int, radius=PIN_RADIUS, color=PIN_COLOR, thickness=PIN_WIDTH, lineType=cv2.LINE_AA, shift=0)
#        cv2.ellipse(image, center=pos_C_int, axes=(PIN_RADIUS, PIN_RADIUS),
#            angle=0, startAngle=int(self.angle_phi), endAngle=int(self.angle_B+self.angle_phi), color=PIN_COLOR_ARC, thickness=-1, lineType=cv2.LINE_AA)


if __name__ == '__main__':

    # ----------------------------
    # 四節リンクを生成し、各点の座標を表示する
    four_bar_linkage = FourBarLinkage(a=100, b=150, c=100, d=150, angle_phi=60)
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
    cv2.createTrackbar('deg', 'panel', 90, 360, lambda x: None)

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

        four_bar_linkage.set_phi(angle)
        four_bar_linkage.update_positions()
        four_bar_linkage.draw(image = img)

        cv2.imshow('link test', img)

        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()


