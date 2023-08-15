#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import threading
from typing import List, Tuple

from .leg import Leg
from .shared_data import SharedData, ServoFb, ServoCmd  # Assuming the shared data class is accessible like this
from config import WINDOW_WIDTH, WINDOW_HEIGHT, SCALE_FACTOR

UPDATE_INTERVAL = 0.01  # Update interval in seconds

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
            'b':  0.04009,
            'l1': 0.025,
            'l2': 0.025,
            'm1': 0.050,
            'm2': 0.035
        }

        self.linkage4bar_params = {
            'a': 0.025,
            'b': 0.080,
            'e': 0.025
        }

        self.linkagehoot_params = {
            'e': 0.025,
            'f': 0.060467,
            'g': 0.040,
            'h-min': 0.066,
            'h-max': 0.086,
            'fh': 0.020902,
            'i' : 0.030,
            'j' : 0.030,
            'k' : 0.013
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
            ('M1', 'X'),
            ('B', 'E'),
            ('E', 'F'),
            ('B', 'G'),
            ('F', 'K'),
            ('J', 'K'),
            ('I', 'K'),
            ('G', 'H'),
            ('F', 'H')
        }

        # 各サーボの原点オフセットリスト
        self.origin_offset_list = [-240.0, -180.0, -360.0, -240.0, -180.0, -420.0, 60.0]        

        self.theta_angle_1 = -45
        self.theta_angle_2 = -115
        self.theta_1 = math.radians(self.theta_angle_1)
        self.theta_2 = math.radians(self.theta_angle_2)

        self.leg = Leg(self.linkage5bar_params, self.linkage4bar_params, self.linkagehoot_params)
        endeffector_position = self.leg.compute_endeffector_position(self.theta_1, self.theta_2)

         # Initialize SharedData
        self.shared_data : SharedData = SharedData()
        
        # Start checking and updating at regular intervals
        threading.Timer(UPDATE_INTERVAL, self.check_and_update).start()       
    
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

    def get_distance_B_M2(self):
        return self.leg.get_distance_B_M2()

    def check_and_update(self):
        # Check new angles from the shared data
        servo_fb : ServoFb = self.shared_data.servo_fb
        if servo_fb is not None:
            # servo_fb を論理角度に変換する
            angle_list = self.parse_servo_data(servo_fb)
            # If there are new angles, update them
            self.set_angles(angle_list[0], angle_list[1])
            self.update_position()

#        print("angle")
#        print(angle_list)
            
        # Schedule the next update
        threading.Timer(UPDATE_INTERVAL, self.check_and_update).start()

    @staticmethod
    def pulse_to_angle(pulse):
        """
        パルス数値を角度に変換する。
        
        引数：
        pulse (int): パルス数値
        
        戻り値:
        float: 角度(度)
        """
        angle = pulse * 0.24
        return angle

    def parse_servo_data(self, servo_data_struct):
        """
        サーボから受信した生データを解析し、パルス値を角度に変換する。
        
        引数：
        servo_data_struct (Struct): サーボからの生反応データ。
        
        戻り値：
        List[float]: 度数法に変換された角度のリスト。
        """
        angle_list = []

        for i, pulse in enumerate(servo_data_struct.a_angle):
            angle = self.pulse_to_angle(pulse)
            corrected_angle = angle + self.origin_offset_list[i]
            if corrected_angle < 0.0:
                corrected_angle = corrected_angle + 360.0
            angle_list.append(corrected_angle)

        return angle_list
    