from .linkage5bar import Linkage5Bar
from .linkage4bar import Linkage4Bar
from .linkagehoot import LinkageHoot
import numpy as np

class Leg:
    def __init__(self, linkage5bar_params, linkage4bar_params, linkagehoot_params):
        self.linkage5bar = Linkage5Bar(linkage5bar_params)
        self.linkage4bar = Linkage4Bar(linkage4bar_params, self.linkage5bar)
        self.linkagehoot = LinkageHoot(linkagehoot_params, self.linkage4bar)
        self.distance_B_M2 = 0.0

    def compute_endeffector_position(self, theta_1, theta_2, ground):

        result = self.linkage5bar.compute_all_positions(theta_1, theta_2)
        if result is None:
            print("5節リンク計算エラー X交点計算不可")
        else:
            positions_5bar, blimit = result

        if blimit == False:
            X = positions_5bar["X"]
            M1 = positions_5bar["M1"]

            positions_4bar = self.linkage4bar.compute_all_positions(M1, X, theta_1)
            angles_4bar = self.linkage4bar.get_angles()
            #endeffector_position = positions_4bar['E']

            B = positions_4bar["B"]
            C = positions_4bar["C"]
            angle_AX = angles_4bar["angle_AX"]

            positions_hoot = self.linkagehoot.compute_all_positions(B, C, theta_1, angle_AX, ground)
            endeffector_position = positions_hoot["E"]

        else:
            positions_4bar = self.linkage4bar.get_positions()
            endeffector_position = positions_4bar['E']

        # 調査のためにBとM2の距離を計算
        self.distance_B_M2 = np.sqrt((positions_4bar["B"][0] - positions_5bar["M2"][0])**2 + (positions_4bar["B"][1] - positions_5bar["M2"][1])**2)

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
    
    def get_positions(self):
        return { **self.linkage5bar.get_positions() , **self.linkage4bar.get_positions() , **self.linkagehoot.get_positions()}

    def inverse_kinematics(self, target_position: tuple) -> dict:
        pass  # To be implemented

    def get_distance_B2_X(self):
        return self.linkage5bar.get_distance_B2_X()

    def get_distance_B_M2(self):
        return self.distance_B_M2

