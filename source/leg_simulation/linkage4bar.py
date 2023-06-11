import math
import numpy as np

class Linkage4Bar:
    def __init__(self, initial_parameters, linkage5bar_instance):
        self.Positions = {}

        self.a = initial_parameters['a']
        self.b = initial_parameters['b']
        self.e = initial_parameters['e']

        self.linkage5bar = linkage5bar_instance

        # 初期値
        self.Positions = {
            "A": (0, 0),
            "B": (0, 0),
            "C": (0, 0),
            "D": (0, 0),
            "E": (0, 0)
        }


    def update_positions(self):
        A_x, A_y = self.linkage5bar.B1
        D_x, D_y = self.linkage5bar.B2

        B_x = A_x + self.a * math.cos(self.linkage5bar.theta_M1)
        B_y = A_y + self.a * math.sin(self.linkage5bar.theta_M1)

        C_x = D_x + self.a * math.cos(math.pi - self.linkage5bar.theta_M1)
        C_y = D_y + self.a * math.sin(math.pi - self.linkage5bar.theta_M1)

        return (A_x, A_y), (B_x, B_y), (C_x, C_y), (D_x, D_y)
    
    def compute_all_positions(self, M1, X, theta_1):
        A_x, A_y = M1
        X_x, X_y = X

        # 頂点Dの座標を計算
        D_x = A_x + self.a * np.cos(theta_1)
        D_y = A_y + self.a * np.sin(theta_1)

        # 頂点Bの座標を計算
        vec_AX = (X_x - A_x, X_y - A_y)
        norm_AX = np.linalg.norm(vec_AX)
        unit_vec_AX = (vec_AX[0] / norm_AX, vec_AX[1] / norm_AX)
        B_x = A_x + unit_vec_AX[0] * self.b
        B_y = A_y + unit_vec_AX[1] * self.b

        # 頂点Cの座標を計算
        C_x = B_x + self.a * np.cos(theta_1)
        C_y = B_y + self.a * np.sin(theta_1)

        # 頂点Eの座標を計算
        E_x = B_x + (self.a + self.e) * np.cos(theta_1)
        E_y = B_y + (self.a + self.e) * np.sin(theta_1)

        self.Positions = {
            "A": (A_x, A_y),
            "B": (B_x, B_y),
            "C": (C_x, C_y),
            "D": (D_x, D_y),
            "E": (E_x, E_y)
        }

        # 結果をリターンする
        return self.Positions

    def get_positions(self):
        return self.Positions

