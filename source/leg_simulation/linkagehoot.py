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
        self.i = initial_parameters['i']
        self.j = initial_parameters['j']
        self.k = initial_parameters['k']
        self.fh= initial_parameters['fh']
        self.angle_E = 119.7
        self.angle_F = 42.0
        self.distance = -0.180

        # 初期値
        self.Positions = {
            "B":(0, 0),
            "E":(0, 0),
            "F":(0, 0),
            "G":(0, 0),
            "H":(0, 0),
            "I":(0, 0),
            "J":(0, 0),
            "K":(0, 0),
        }


    def compute_all_positions(self, B: tuple, C: tuple, theta_1: float, angle_AX: float):
        B_x, B_y = B
        C_x, C_y = C

        # 頂点Dの座標を計算
        E_x = C_x + self.e * np.cos(theta_1)
        E_y = C_y + self.e * np.sin(theta_1)

        # 頂点Fの座標を計算
        # 角度を足して新たな座標の角度を得る
        rad_EF = math.radians(self.angle_E) + theta_1
        rad_EF = theta_1 - math.radians(180 - self.angle_E)
        F_x = E_x + self.f * math.cos(rad_EF)
        F_y = E_y + self.f * math.sin(rad_EF)
        F = (F_x, F_y)

        #print(self.angle_E, math.degrees(theta_1), math.degrees(rad_EF))

        # 頂点Gの座標を計算する
        # 頂点Bから角度AXの延長上
        G_x = B_x + self.g * math.cos(angle_AX)
        G_y = B_y + self.g * math.sin(angle_AX)

        # 足底の点の角度を計算する
        base_points = self.calculate_base_points(F)

        # つま先の角度を計算する
        # 暫定的にdistanceを20mmに固定する
        toe_points = self.calculate_toe_points(F, self.distance)

        positions = {
            "B": (B_x, B_y),
            "E": (E_x, E_y),
            "F": (F_x, F_y),
            "G": (G_x, G_y)
        }

        self.Positions = { **positions, **base_points, **toe_points}

        # 結果をリターンする
        return self.Positions
    

    def calculate_base_points(self, F: tuple):
        """
        足底の座標を計算する。
        I,J,Kは地面と平行（水平）となる。
        """

        # Fから垂直に下ろした方向にKを置く
        F_x, F_y = F
        K_x = F_x
        K_y = F_y - self.k

        # Kの前後にI,Jを置く
        I_x = K_x + self.i
        J_x = K_x - self.j

        I_y = K_y
        J_y = K_y

        # Hの座標をFから割り出す
        rad_F = math.radians(self.angle_F)
        H_x = F_x + self.fh * math.cos(rad_F)
        H_y = F_y + self.fh * math.sin(rad_F)

        self.potisions_base = {
            "H": (H_x, H_y),
            "I": (I_x, I_y),
            "J": (J_x, J_y),
            "K": (K_x, K_y)
        }

        return self.potisions_base

    def calculate_toe_points(self, F: tuple, ground: float):
        """
        足底が浮いていて、つま先だけが地面に接している場合の座標を計算する
        groundがFから地面までの距離で、これはkよりも大きくなければならない
        """
        F_x, F_y = F

        if (F_y - self.k) < ground:
            # 点Kが設置しているなら、この処理は行わない
            positions_toe = {}

            return positions_toe
        
        else:
            # 点Kが設置していないなら、つま先を地面につける

            # Ifの座標を計算する
            It_y = ground
            distance = F_y - ground
            
            D = math.sqrt(self.k**2 + self.i**2)
            It_x = math.sqrt(D**2 - distance**2) + F_x
            It = (It_x, It_y)

            # Ktの座標を計算する。
            # F,Itから円を描いて交点をKtとします。
            # KtはF_Xよりもx座標が小さい方を採用。
            q1, q2 = self.circle_intersection(np.array([F_x, F_y]), self.k, np.array([It_x, It_y]), self.i)

            if (q1[0] <= F_x):
                Kt = q1
            else:
                Kt = q2

            Kt_x, Kt_y = Kt

            # Jtの座標を計算する
            vec_IK = (Kt_x - It_x, Kt_y - It_y)
            norm_IK = np.linalg.norm(vec_IK)
            unit_vec_IK = (vec_IK[0] / norm_IK, vec_IK[1] / norm_IK)
            Jt_x = Kt_x + unit_vec_IK[0] * self.j
            Jt_y = Kt_y + unit_vec_IK[1] * self.j

            # ベクトルIKの角度を計算
            angle_IK = np.arctan2(vec_IK[1], vec_IK[0])

            # Hの座標をFから割り出す
            rad_F = math.radians(self.angle_F - (180.0 - math.degrees(angle_IK)))
            #rad_F = math.radians(self.angle_F) - angle_IK

            print(self.angle_F, math.degrees(angle_IK))
            Ht_x = F_x + self.fh * math.cos(rad_F)
            Ht_y = F_y + self.fh * math.sin(rad_F)

            self.positions_toe = {
                "Ht": (Ht_x, Ht_y),
                "It": (It_x, It_y),
                "Jt": (Jt_x, Jt_y),
                "Kt": (Kt_x, Kt_y)
            }

            return self.positions_toe



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



