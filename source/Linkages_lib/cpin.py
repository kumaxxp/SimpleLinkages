import cv2
import numpy as np

import math
from typing import Tuple

PIN_RADIUS = 40
PIN_COLOR = (100, 100, 100)
PIN_COLOR_ARC = (255, 100, 100)
PIN_WIDTH = 2

class CPin:
    def __call__(self):
        return 'CPin'

    def __init__(self, offset: float, degree: float):
        self.offset: float = offset
        self.degree: float = degree

        self.enable_rotation: bool = True
        self.is_fixed: bool = True
        self.is_drive: bool = True

        self.pt_parent:Tuple[float,float] = (0.0, 0.0)


    def set_parent_pos(self, pt_parent:Tuple[float,float]):
        self.pt_parent = pt_parent

    def set_degree(self, degree: float):
        self.degree = degree

    def calculate(self):
        pass

    def draw(self, img):
        pt_int =tuple(map(int,self.pt_parent)) 

        cv2.circle(img, 
            center = pt_int, 
            radius = PIN_RADIUS,
            color = PIN_COLOR,
            thickness =  PIN_WIDTH,
            lineType = cv2.LINE_AA,
            shift = 0)

        cv2.ellipse(img, 
            center = pt_int, 
            axes = (PIN_RADIUS,PIN_RADIUS), 
            angle = 0, 
            startAngle = 0,
            endAngle = int(self.degree),
            color = PIN_COLOR_ARC, 
            thickness =  -1, 
            lineType = cv2.LINE_AA)


if __name__ == '__main__':

    controlBox = np.zeros((300,512,3), np.uint8)
    cv2.namedWindow('panel')
    cv2.createTrackbar('deg', 'panel', 0, 360, lambda x: None)

    pin = CPin(0.0, 100.0)
    pin.set_parent_pos(200,200)

    img = np.zeros((600,1000,3), np.uint8)
    img[:,:,:] = 255
    while True:

        img = np.zeros((600,1000,3), np.uint8)
        img[:,:,:] = 255

        # 角度変更
        deg = cv2.getTrackbarPos('deg', 'panel') 

        pin.set_degree(deg)
        pin.draw(img)

        cv2.imshow('pin test', img)

        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()