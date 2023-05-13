import numpy as np
from scipy.spatial.transform import Rotation
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def rotation_matrix_from_vectors(vec1, vec2):
    # Normalize the input vectors
    vec1 = vec1 / np.linalg.norm(vec1)
    vec2 = vec2 / np.linalg.norm(vec2)

    # Calculate the rotation axis and angle
    axis = np.cross(vec1, vec2)
    axis_norm = np.linalg.norm(axis)
    angle = np.arccos(np.dot(vec1, vec2))

    K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    identity_matrix = np.identity(3)
    R = identity_matrix + np.sin(angle) * K + (1 - np.cos(angle)) * K @ K

    return R

class World:
    @staticmethod
    def collision_detection(position):
        if position[2] < 0:
            return True
        return False

class Robot:
    def __init__(self, position, leg1_params, leg2_params):
        self.position = np.array(position, dtype=float)
        self.rotation = Rotation.identity()  # 回転を初期化
        self.legs = [
            Leg(self, leg1_params["offsets"], leg1_params["initial_vertex1"], leg1_params["initial_vertex2"]),
            Leg(self, leg2_params["offsets"], leg2_params["initial_vertex1"], leg2_params["initial_vertex2"])
        ]
        # セットアップ時に足を適切な位置に移動します。
        initial_translation = np.array(position)  # 初期位置を指定
        self.update_legs(initial_translation)        

    def set_rotation(self, rotation_matrix_or_quaternion_or_euler_angles):
        # 回転行列、クォータニオン、またはオイラー角を受け取り、Rotationオブジェクトに変換
        self.rotation = Rotation.from_matrix(rotation_matrix_or_quaternion_or_euler_angles)

    def move(self, delta_position):
        new_position = self.position + delta_position
        if not World.collision_detection(new_position):
            self.position = new_position

            initial_translation = np.array(self.position)  # 初期位置を指定
            self.update_legs(initial_translation)        

    def update_legs(self):
        transform_matrix = np.eye(4)
        transform_matrix[:3, :3] = self.rotation.as_matrix()
        transform_matrix[:3, 3] = self.position
        for leg in self.legs:
            leg.update_position(transform_matrix)  # 変換行列をLegクラスに渡す

    def align_line_a_to_plane(self):
        # Get Leg1's vertex2 and Leg2's vertex2 global positions
        leg1_vertex2 = self.legs[0].vertex2
        leg2_vertex2 = self.legs[1].vertex2

        # Compute the current direction vector of line A
        current_direction = leg2_vertex2 - leg1_vertex2

        # Remove Z-component from the direction vector (projecting onto Z=0 plane)
        projected_direction = np.array([current_direction[0], current_direction[1], 0])

        # Set the target direction vector parallel to the X-axis
        target_direction = np.array([1, 0, 0])

        # Compute the rotation matrix
        R = rotation_matrix_from_vectors(projected_direction, target_direction)

        # Apply the rotation matrix to the robot
        self.set_rotation(R)

        # Apply the rotation to legs
        self.rotate_legs(R)

        # Move the robot so that leg2_vertex2 lies on Z=0 plane
        translation = np.array([0, 0, -leg2_vertex2[2]])
        self.move(translation)

    def rotate_legs(self, R):
        for leg in self.legs:
            leg.rotate(R)
            
    def update_legs(self, translation):
        translation = translation.astype(np.int64)
        for leg in self.legs:
            leg.vertex1 += translation
            leg.vertex2 += translation

    def visualize_robot_position(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Draw line A (green) and line B (yellow)
        lower_vertex = self.legs[np.argmin([leg.vertex2[2] for leg in self.legs])].vertex2
        higher_vertex = self.legs[1 - np.argmin([leg.vertex2[2] for leg in self.legs])].vertex2
        ax.plot(*zip(lower_vertex, higher_vertex), color="green")
        mid_point = (lower_vertex + higher_vertex) / 2
        ax.plot(*zip(mid_point, self.position), color="yellow")

        # Robot position (red dot)
        ax.scatter(*self.position, color="red")

        # Legs positions (blue dots and links)
        for leg in self.legs:
            leg.update_global_position()  # 必ず更新する
            ax.scatter(*leg.global_position, color="blue")
            ax.plot(*zip(leg.vertex1, leg.vertex2), color="black")

        # Draw floor (Z=0 plane)
        xs, ys = np.meshgrid(range(-10, 11), range(-10, 11))
        zs = xs * 0
        ax.plot_surface(xs, ys, zs, alpha=0.3)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.set_zlim(0, 10)
        
        plt.show()

class Leg:
    def __init__(self, robot, offsets, initial_vertex1, initial_vertex2):
        self.robot = robot
        self.local_position = np.array([offsets["x"], offsets["y"], offsets["z"]])
        self.global_position = np.zeros(3)
        self.initial_vertex1_offset = np.array(initial_vertex1)
        self.initial_vertex2_offset = np.array(initial_vertex2)
        self.vertex1 = np.array(initial_vertex1, dtype=np.float64)
        self.vertex2 = np.array(initial_vertex2, dtype=np.float64)

    def update_position(self, robot_transform_matrix):
        self.global_position = robot_transform_matrix[:3, :3].dot(self.local_position) + robot_transform_matrix[:3, 3]
        self.vertex1 = robot_transform_matrix[:3, :3].dot(self.initial_vertex1_offset - self.local_position) + self.global_position
        self.vertex2 = robot_transform_matrix[:3, :3].dot(self.initial_vertex2_offset - self.local_position) + self.global_position

    def rotate(self, R):
        self.vertex1 = np.dot(R, self.vertex1)
        self.vertex2 = np.dot(R, self.vertex2)

    def update_global_position(self):
        # global_position を適切に計算・更新
        self.global_position = self.vertex1 + self.vertex2

world = World()

leg1_params = {
    "offsets": {"x": 1, "y": 0, "z": 0},
    "initial_vertex1": [1, 0, 0],
    "initial_vertex2": [1, 0, -1]
}

leg2_params = {
    "offsets": {"x": -1, "y": 0, "z": 0},
    "initial_vertex1": [-1, 0, 0],
    "initial_vertex2": [-1, 0, -2]
}

robot = Robot([0, 0, 0], leg1_params, leg2_params)

# Move the robot
robot.move(np.array([1, 0, 0]))

# Align vertex2 of the legs to Z plane
robot.align_line_a_to_plane()

# Visualize the robot and legs positions
robot.visualize_robot_position()

# 移動例
robot.move(np.array([1, 0, 0]))
print(robot.position)
print(robot.legs[0].global_position)
print(robot.legs[1].global_position)