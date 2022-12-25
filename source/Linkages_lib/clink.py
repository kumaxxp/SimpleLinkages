import cv2
import numpy as np

import math
from typing import Tuple
from operator import add

from cpin import CPin

LINK_COLOR = (100, 100, 100)
LINK_WIDTH = 2

class CLink:
    def __init__(self, length: float):
        self.length = length
        self.pins: list[CPin] = []

        
        # 原点
        self.pt_org:tuple(float,float) = (0,0)
        # 反原点
        self.pt_oop:tuple(float,float) = (100,100)
        # 親座標
        self.pt_parent:tuple(float,float) = (0,0)


        # この部分の初期化はjsonファイルを読み込んで設定したいところ
        pin = CPin(offset=500.0, degree=90.0)

        self.pins.append(pin) 

    def calculate_coordinates():
        # 座標計算。親座標にしたがって動く
        pass

    def draw(self, img):

        pt_org_int =tuple(map(int,self.pt_org)) 
        pt_oop_int =tuple(map(int,self.pt_oop)) 
        pt_parent_int =tuple(map(int,self.pt_parent)) 

        pt_org_int = tuple(map(lambda x, y: x + y, pt_org_int, pt_parent_int))
        pt_oop_int = tuple(map(lambda x, y: x + y, pt_oop_int, pt_parent_int))

        cv2.line(img,
            pt1 = pt_org_int,
            pt2 = pt_oop_int,
            color = LINK_COLOR,
            thickness =  LINK_WIDTH,
            lineType = cv2.LINE_AA,
            shift = 0)

        if self.pins:
            self.pins[0].draw(img)


    def set_parent_pos(self, pt_parent:Tuple[float,float]):
        self.pt_parent = pt_parent
        self.pins[0].set_parent_pos(pt_parent)



if __name__ == '__main__':

    controlBox = np.zeros((300,512,3), np.uint8)
    cv2.namedWindow('panel')
    cv2.createTrackbar('deg', 'panel', 0, 360, lambda x: None)

    pt:Tuple[float,float] = (200.0,200.0)
    Link = CLink(length = 100)
    Link.set_parent_pos(pt_parent=pt)

    img = np.zeros((600,1000,3), np.uint8)
    img[:,:,:] = 255
    while True:

        img = np.zeros((600,1000,3), np.uint8)
        img[:,:,:] = 255

        # 角度変更
        deg = cv2.getTrackbarPos('deg', 'panel') 

        Link.draw(img)

        cv2.imshow('link test', img)

        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()