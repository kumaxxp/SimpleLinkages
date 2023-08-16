import numpy as np
import math

class Linkage5Bar:
    def __init__(self, initial_parameters):
        self.Positions = {}

        self.B1 = np.array([initial_parameters['b'] / 2, 0])
        self.B2 = np.array([-initial_parameters['b'] / 2, 0])

        self.b = initial_parameters['b']
        self.l1 = initial_parameters['l1']
        self.l2 = initial_parameters['l2']
        self.m1 = initial_parameters['m1']
        self.m2 = initial_parameters['m2']

        self.theta_M1 = None
        self.theta_M2 = None

        self.distance_B_M2 = 0.0

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
        
    def compute_all_positions(self, theta_1, theta_2):
        # Calculate vertex A (M1)
        M1_x = self.B1[0] + self.l1 * np.cos(theta_1)
        M1_y = self.B1[1] + self.l1 * np.sin(theta_1)

        # Calculate vertex B (M2)
        M2_x = self.B2[0] + self.l2 * np.cos(theta_2)
        M2_y = self.B2[1] + self.l2 * np.sin(theta_2)

        # Call circle_intersection to find the possible X points
        M1 = np.array([M1_x, M1_y])
        M2 = np.array([M2_x, M2_y])
        intersection_points = self.circle_intersection(M1, self.m1, M2, self.m2)

        if intersection_points is None:
            # m1,m2からのx交点が計算できなかった
            return None

        X1, X2 = intersection_points

        # Choose the intersection point with smaller Y coordinate as the final X point
        if X1[1] < X2[1]:
            X_x, X_y = X1
        else:
            X_x, X_y = X2

        # Compute the distance between point B2 and X
        self.distance_B2_X = np.sqrt((self.B2[0] - X_x)**2 + (self.B2[1] - X_y)**2)

        if self.distance_B2_X >= self.b:
            # Save all positions and angles in the Positions member variable
            self.Positions = {
                'B1': (self.B1[0], self.B1[1]),
                'B2': (self.B2[0], self.B2[1]),
                'M1': (M1_x, M1_y),
                'M2': (M2_x, M2_y),
                'X': (X_x, X_y),
            }
            blimit = False
        else:
            blimit = True

        # B2-Xの距離がリミットの30.0mm 以下の場合は座標を更新して、blimitはFalse
        # B2-Xの距離がリミットの30.0mm より大きい場合は座標を更新せず、blimitはTrue
        return self.Positions, blimit
    
    def get_positions(self):
        return self.Positions

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

    def get_distance_B2_X(self):
        return self.distance_B2_X

