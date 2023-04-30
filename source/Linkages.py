#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import numpy as np


class Linkage5Bar:
    def __init__(self, initial_parameters):
        self.B1 = np.array([initial_parameters['b'] / 2, 0])
        self.B2 = np.array([-initial_parameters['b'] / 2, 0])

        self.b = initial_parameters['b']
        self.l1 = initial_parameters['l1']
        self.l2 = initial_parameters['l2']
        self.m1 = initial_parameters['m1']
        self.m2 = initial_parameters['m2']

        self.theta_M1 = None
        self.theta_M2 = None

    @staticmethod
    def circle_intersection(c1, r1, c2, r2):
        d = np.linalg.norm(c1 - c2)
        if d > r1 + r2:
            return None

        delta = (d**2 - r2**2 + r1**2) / (2 * d)

        h = np.sqrt(r1**2 - delta**2)

        e = (c2 - c1) / d

        p = c1 + delta * e
        q1, q2 = p + h * np.array([-e[1], e[0]]), p - h * np.array([-e[1], e[0]])

        return q1, q2

    def compute_vertex_X(self, theta_1, theta_2):
        x_M1, x_M2 = self.forward_kinematics(theta_1, theta_2)

        circle_intersects = self.circle_intersection(x_M1, self.m1, x_M2, self.m2)
        if circle_intersects is None:
            return None
        else:
            x1, x2 = circle_intersects
            # y座標が小さい頂点を選択します
            x_result = x1 if x1[1] < x2[1] else x2
            return x_result

    def forward_kinematics(self, theta_1, theta_2):
        x_M1 = np.array([self.l1 * np.cos(theta_1), self.l1 * np.sin(theta_1)])
        x_M2 = np.array([self.b + self.l2 * np.cos(theta_2), self.l2 * np.sin(theta_2)])
        return x_M1, x_M2        

    def inverse_kinematics(self, target_position):
        x, y = target_position
        q = ((x ** 2 + y ** 2) - (self.m1 ** 2 + self.m2 ** 2)) / (2 * self.m1 * self.m2)
        if -1 <= q <= 1:
            self.theta_M2 = math.acos(q)
        else:
            raise ValueError("Target position is not reachable")

        beta = math.atan2(y, x)
        gamma = math.asin((self.m2 * math.sin(self.theta_M2)) / math.sqrt(x ** 2 + y ** 2))
        self.theta_M1 = beta - gamma


class Linkage4Bar:
    def __init__(self, initial_parameters, linkage5bar_instance):
        self.a = initial_parameters['a']
        self.b = initial_parameters['b']

        self.linkage5bar = linkage5bar_instance

    def update_positions(self):
        A_x, A_y = self.linkage5bar.B1
        D_x, D_y = self.linkage5bar.B2

        B_x = A_x + self.a * math.cos(self.linkage5bar.theta_M1)
        B_y = A_y + self.a * math.sin(self.linkage5bar.theta_M1)

        C_x = D_x + self.a * math.cos(math.pi - self.linkage5bar.theta_M1)
        C_y = D_y + self.a * math.sin(math.pi - self.linkage5bar.theta_M1)

        return (A_x, A_y), (B_x, B_y), (C_x, C_y), (D_x, D_y)
    

class Leg:
    def __init__(self, linkage5bar_params, linkage4bar_params):
        self.linkage5bar = Linkage5Bar(linkage5bar_params)
        self.linkage4bar = Linkage4Bar(linkage4bar_params)

    def compute_endeffector_position(self, theta_1, theta_2):
        X = self.linkage5bar.compute_vertex_X(theta_1, theta_2)
        if X is None:
            return None

        A = X
        endeffector_position = self.linkage4bar.compute_E_position(A)
        return endeffector_position

    def forward_kinematics(self, B1_angle: float, B2_angle: float) -> dict:
        # set the new angles in the linkage5bar object
        self.linkage5bar.thetaB1_deg = B1_angle
        self.linkage5bar.thetaB2_deg = B2_angle
        
        # calculate positions and angles of linkage4bar object
        positions_4bar = self.linkage4bar.get_positions()
        angles_4bar = self.linkage4bar.get_angles_degrees()
        
        # calculate new positions of linkage5bar
        self.linkage5bar.set_new_X(positions_4bar["E"])
        positions_5bar = self.linkage5bar.get_positions()
        
        # combine the results
        result_positions = {**positions_4bar, **positions_5bar}
        
        return result_positions
    

    def inverse_kinematics(self, target_position: tuple) -> dict:
        pass  # To be implemented


# Please create a "linkage4bar.py" file and define the Linkage4Bar class.
# Similarly, create a "linkage5bar.py" file and define the Linkage5Bar class.

if __name__ == "__main__":

    linkage5bar_params = {
        'b': 10,
        'l1': 5,
        'l2': 5,
        'm1': 5,
        'm2': 5
    }

    linkage4bar_params = {
        'L3': 5,
        'L4': 5
    }

    leg = Leg(linkage5bar_params, linkage4bar_params)
    theta_1 = math.radians(45)
    theta_2 = math.radians(30)

    endeffector_position = leg.compute_endeffector_position(theta_1, theta_2)
    print("エンドエフェクタの位置:", endeffector_position)

    