import cv2
import numpy as np

import math
from typing import Tuple

PIN_RADIUS = 20
PIN_COLOR = (100, 100, 100)
PIN_COLOR_ARC = (255, 100, 100)
PIN_WIDTH = 1

class CPin:
    """
    リンク上のピンを表すクラス。
    
    属性:
        offset (float): 親オブジェクトの原点からのピンのオフセット。
        degree (float): 親オブジェクトの原点を中心にしたピンの回転角度。
        enable_rotation (bool): ピンが回転できるかどうかを示すフラグ。
        is_fixed (bool): ピンが固定されているかどうかを示すフラグ。
        is_drive (bool): ピンがドライブピンかどうかを示すフラグ。
        parent_pos (Tuple[float, float]): 親オブジェクトの位置。
    
    """
    def __init__(self, offset: float, degree: float, enable_rotation: bool = True, is_fixed: bool = True, is_drive: bool = True):
        """
        コンストラクタ。

        Args:
            offset (float): 親オブジェクトの原点からのピンのオフセット
            degree (float): 親オブジェクトの原点を中心にしたピンの回転角度
            enable_rotation (bool, optional): 回転を有効にする場合は True。デフォルトは True。
            is_fixed (bool, optional): 固定されている場合は True。デフォルトは True。
            is_drive (bool, optional): 駆動されている場合は True。デフォルトは True。
        """
        self.offset = offset
        self.enable_rotation = enable_rotation
        self.is_fixed = is_fixed
        self.is_drive = is_drive
        self.degree = degree

        # 原点
        self.org_pos: Tuple[float, float] = (0, 0)
        # 親座標
        self.parent_pos: Tuple[float, float] = (0, 0)

    @property
    def degree(self) -> float:
        """ピンの角度。"""
        return self._degree

    @degree.setter
    def degree(self, degree: float):
        self._degree = degree

    @property
    def parent_pos(self) -> Tuple[float, float]:
        """親オブジェクトの位置。"""
        return self._parent_pos

    @parent_pos.setter
    def parent_pos(self, pos: Tuple[float, float]):
        self._parent_pos = pos

    def calculate_coordinates(self):
        """ピンの状態に基づいて値を計算する。"""
        # 原点は(self.offset, 0)
        self.org_pos: Tuple[float, float] = (self.offset, 0)

        # 原点を親座標でオフセットする
        self.org_pos = tuple(map(lambda x, y: x + y, self.org_pos, self.parent_pos))
        

    def draw(self, image: np.ndarray) -> None:
        """
        画像にピンを描画する。

        Args:
            image (np.ndarray): 描画対象の画像。
        """
        pos = tuple(map(int, self.org_pos))

        cv2.circle(image, center=pos, radius=PIN_RADIUS, color=PIN_COLOR, thickness=PIN_WIDTH,
            lineType=cv2.LINE_AA, shift=0)

        cv2.ellipse(image, center=pos, axes=(PIN_RADIUS, PIN_RADIUS), angle=0, startAngle=0,
            endAngle=int(self.degree), color=PIN_COLOR_ARC, thickness=-1, lineType=cv2.LINE_AA)



if __name__ == '__main__':

    controlBox = np.zeros((300,512,3), np.uint8)
    cv2.namedWindow('panel')
    cv2.createTrackbar('deg', 'panel', 0, 360, lambda x: None)

    pin = CPin(offset= 100, degree = 0.0)
    pin.parent_pos = (200,200)
    pin.calculate_coordinates()

    img = np.zeros((600,1000,3), np.uint8)
    img[:,:,:] = 255
    while True:

        img = np.zeros((600,1000,3), np.uint8)
        img[:,:,:] = 255

        # ピンの角度変更
        deg = cv2.getTrackbarPos('deg', 'panel') 
        pin.degree = deg

        # 描画
        pin.draw(image = img)

        cv2.imshow('pin test', img)

        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()