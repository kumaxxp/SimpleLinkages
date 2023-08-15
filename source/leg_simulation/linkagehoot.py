import math
import numpy as np

# 4節リンクのA,B,C頂点を取り込んで、足先リンクの座標を計算する
# 足先リンクの頂点B,E,F,Gを計算する（Bは共有）。機構的に確定する。
# Fを中点とする線分I,Jは地面に平行に倣う性質を持つ。それにより⊿EFJの角度が確定し、頂点Hの位置が確定する
# HとGの距離が変化して、100mmよりも小さくなればその分エネルギーがたまっている。


class LinkageHoot:
    def __init__(self, initial_parameters, linkage4bar_instance):
        self.Positions = {}

        self.linkage4bar = linkage4bar_instance
        
        self.e = initial_parameters['e']
        self.f = initial_parameters['f']
        self.g = initial_parameters['g']
        self.angle_E = 119.7

        # 初期値
        self.Positions = {
            "B":(0, 0),
            "E":(0, 0),
            "F":(0, 0),
            "G":(0, 0),
            "H":(0, 0),
        }


    def compute_all_positions(self, B: tuple, C: tuple, theta_1: float, angle_AX: float):
        B_x, B_y = B
        C_x, C_y = C

        # 頂点Dの座標を計算
        E_x = C_x + self.e * np.cos(theta_1)
        E_y = C_y + self.e * np.sin(theta_1)

        # 頂点Fの座標を計算
        # 角度を足して新たな座標の角度を得る
#        angle_EF = theta_1 + self.angle_E
        print(angle_AX, theta_1)
        rad_EF = math.radians(self.angle_E) - angle_AX
        F_x = E_x + self.f * math.cos(rad_EF)
        F_y = E_y + self.f * math.sin(rad_EF)

        # 頂点Gの座標を計算する
        # 頂点Bから角度AXの延長上
        G_x = B_x + self.g * math.cos(angle_AX)
        G_y = B_y + self.g * math.sin(angle_AX)

        # この関数で、足底の点の角度を計算する


        self.Positions = {
            "B": (B_x, B_y),
            "E": (E_x, E_y),
            "F": (F_x, F_y),
            "G": (G_x, G_y)
        }

        # 結果をリターンする
        return self.Positions


    def calculate_point_with_angle_phi(self, start_point: tuple, ref_point: tuple,
                            angle: float, distance: float) -> tuple:
        """
        指定した始点から指定した角度と距離で新たな座標を計算する関数

        Parameters
        ----------
        start_point : tuple
            始点の座標（x, y）
        ref_point : tuple
            始点と一緒に直線を形成する参照点の座標（x, y）
        angle : float
            始点から参照点に対する新たな座標までの角度（単位はラジアン）
        distance : float
            始点からの新たな座標までの距離

        Returns
        -------
        new_coordinate : tuple
            計算された新たな座標（x, y）

        Notes
        -----
        角度はラジアンで指定します。
        """

        # 直線の角度を計算（atan2(y差/x差)を用いる）
        theta_line = math.atan2(start_point[1] - ref_point[1], start_point[0] - ref_point[0])

        # 角度を足して新たな座標の角度を得る
        theta_new = theta_line + angle

        # 始点からの距離と角度を用いて新たな座標を計算
        new_x = start_point[0] + distance * math.cos(theta_new)
        new_y = start_point[1] + distance * math.sin(theta_new)

        return (new_x, new_y)        

    def get_positions(self):
        return self.Positions



