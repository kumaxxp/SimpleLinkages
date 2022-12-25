import cv2
import numpy as np

import math
from typing import Tuple
from typing import List

from cpin import CPin

LINK_COLOR = (100, 100, 100)
LINK_WIDTH = 2

class CLink:
    def __init__(self, length: float, pins:List[CPin]):
        self.length = length
        self.pins: List[CPin] = pins

        # 原点
        self.org_pos: Tuple[float, float] = (0, 0)
        # 反原点
        self.oop_pos: Tuple[float, float] = (0, 0)
        # 親座標
        self._parent_pos: Tuple[float, float] = (0, 0)

        # pinを配置
#        self.init_pin(offset = 0, degree = 30)
#        self.init_pin(offset = 300, degree = 90)

    def init_pin(self, offset: float, degree: float):
        pin = CPin(offset=offset, degree=degree)
        self.pins.append(pin)

    def calculate_coordinates(self):
        # 原点は(0, 0),反原点は(self.length, 0) となる
        self.org_pos: Tuple[float, float] = (0, 0)
        self.oop_pos: Tuple[float, float] = (self.length, 0)

        # 原点、反原点を親座標でオフセットする
        self.org_pos = tuple(map(lambda x, y: x + y, self.org_pos, self.parent_pos))
        self.oop_pos = tuple(map(lambda x, y: x + y, self.oop_pos, self.parent_pos))
        
        # 親座標中心で回転させたい。後日実装

        # ピンも座標計算
        for pin in self.pins:
            pin.calculate_coordinates()

    def draw(self, image: np.ndarray) -> None:
        org_pos_int = tuple(map(int, self.org_pos))
        oop_pos_int = tuple(map(int, self.oop_pos))

        # linkを描画する
        cv2.line(image, pt1=org_pos_int, pt2=oop_pos_int, color=LINK_COLOR,
                 thickness=LINK_WIDTH, lineType=cv2.LINE_AA, shift=0)

        # pinを描画する
        for pin in self.pins:
            pin.draw(image)

    @property
    def parent_pos(self) -> Tuple[float, float]:
        """親オブジェクトの位置。"""
        return self._parent_pos

    @parent_pos.setter
    def parent_pos(self, pos: Tuple[float, float]):
        self._parent_pos = pos
        # 各ピンにも親オブジェクトの位置を設定する。
        # リンクの角度に影響を受けるはずなので、後ほど修正する
        for pin in self.pins:
            pin.parent_pos = pos

# 初期化データ
data = [
    {
        "length": 500.0,
        "pins": [
            {
                "offset": 0,
                "degree": 45,
                "enable_rotation": True,
                "is_fixed": True,
                "is_drive": True
            },
            {
                "offset": 500,
                "degree": 30,
                "enable_rotation": True,
                "is_fixed": True,
                "is_drive": True
            }
        ]
    },
    {
        "length": 200.0,
        "pins": [
            {
                "offset": 0.0,
                "degree": 45,
                "enable_rotation": True,
                "is_fixed": True,
                "is_drive": True
            },
            {
                "offset": 200.0,
                "degree": 45,
                "enable_rotation": True,
                "is_fixed": True,
                "is_drive": True
            }
        ]
    }
]    


if __name__ == '__main__':

    controlBox = np.zeros((300,512,3), np.uint8)
    cv2.namedWindow('panel')
    cv2.createTrackbar('deg', 'panel', 0, 360, lambda x: None)

    img = np.zeros((600,1000,3), np.uint8)
    img[:,:,:] = 255

    links = [CLink(link_data["length"], [CPin(**pin_data) for pin_data in link_data["pins"]]) for link_data in data]

    pos:Tuple[float,float] = (100.0,400.0)
    for link in links:
        link.parent_pos = pos
        link.calculate_coordinates()

    pos2:Tuple[float,float] = (100.0,400.0)

    while True:

        img = np.zeros((600,1000,3), np.uint8)
        img[:,:,:] = 255

        # 角度変更
        deg = cv2.getTrackbarPos('deg', 'panel') 

        for link in links:
            link.draw(image = img)

        cv2.imshow('link test', img)

        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()