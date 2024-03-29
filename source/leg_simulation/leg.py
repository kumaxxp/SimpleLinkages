from .linkage5bar import Linkage5Bar
from .linkage4bar import Linkage4Bar

class Leg:
    def __init__(self, linkage5bar_params, linkage4bar_params):
        self.linkage5bar = Linkage5Bar(linkage5bar_params)
        self.linkage4bar = Linkage4Bar(linkage4bar_params, self.linkage5bar)

    def compute_endeffector_position(self, theta_1, theta_2):

        positions_5bar, blimit = self.linkage5bar.compute_all_positions(theta_1, theta_2)
        if blimit == False:
            X = positions_5bar["X"]
            M1 = positions_5bar["M1"]

            positions_4bar = self.linkage4bar.compute_all_positions(M1, X, theta_1)
            endeffector_position = positions_4bar['E']
        else:
            positions_4bar = self.linkage4bar.get_positions()
            endeffector_position = positions_4bar['E']

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
        return { **self.linkage5bar.get_positions() , **self.linkage4bar.get_positions()}

    def inverse_kinematics(self, target_position: tuple) -> dict:
        pass  # To be implemented

    def get_distance_B2_X(self):
        return self.linkage5bar.get_distance_B2_X()

