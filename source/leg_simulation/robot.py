#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import threading
from typing import List, Tuple

from .leg import Leg
from config import WINDOW_WIDTH, WINDOW_HEIGHT, SCALE_FACTOR

class Robot:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.lock = threading.Lock()        

        self.screen_height = WINDOW_HEIGHT
        self.screen_width = WINDOW_WIDTH
        self.scale_factor = SCALE_FACTOR

        self.linkage5bar_params = {
            'b': 0.020,
            'l1': 0.015,
            'l2': 0.025,
            'm1': 0.040,
            'm2': 0.025
        }

        self.linkage4bar_params = {
            'a': 0.020,
            'b': 0.050,
            'e': 0.040
        }

        self.link_list = {
            ('A', 'B'),
            ('B', 'C'),
            ('C', 'D'),
            ('D', 'A'),
            ('C', 'E'),
            ('B1', 'B2'),
            ('B1', 'M1'),
            ('B2', 'M2'),
            ('M2', 'X'),
            ('M1', 'X')
        }

        self.theta_angle_1 = -45
        self.theta_angle_2 = -115
        self.theta_1 = math.radians(self.theta_angle_1)
        self.theta_2 = math.radians(self.theta_angle_2)

        self.leg = Leg(self.linkage5bar_params, self.linkage4bar_params)
        endeffector_position = self.leg.compute_endeffector_position(self.theta_1, self.theta_2)
    
    def get_positions(self) -> List[Tuple[float, float]]:
        with self.lock:
            positions = self.leg.get_positions()
        return positions
    
    def get_link_list(self) -> List:
        return self.link_list
    
    def set_angles(self, theta_angle_1, theta_angle_2):
        with self.lock:
            self.theta_angle_1 = theta_angle_1
            self.theta_angle_2 = theta_angle_2
            self.theta_1 = math.radians(self.theta_angle_1)
            self.theta_2 = math.radians(self.theta_angle_2)

    def update_position(self):
        endeffector_position = self.leg.compute_endeffector_position(self.theta_1, self.theta_2)

    def get_distance_B2_X(self):
        return self.leg.get_distance_B2_X()

