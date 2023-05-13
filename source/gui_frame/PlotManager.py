import threading
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from config import SCALE_FACTOR
from leg_simulation import Robot

class PlotManager(threading.Thread):
    def __init__(self, initial_time, shared_data):
        # スーパークラスのイニシャライザを呼び出します。
        super().__init__()
        self.shared_data = shared_data
        self.initial_time = initial_time
        self.robot = Robot()  # robot インスタンスを初期化
        self.scale_factor = float(SCALE_FACTOR)
        
    def run(self):
        self.init_plot()

    def init_plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")

        # 軸のラベル設定
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

        while True:
            # プロットデータ取得
            positions = self.robot.get_positions()
            link_list = self.robot.get_link_list()

            transformed_coordinates = {key: coord for key, coord in positions.items()}
            links_coordinates = self.create_links(link_list, transformed_coordinates)

            # 描画処理
            self.draw_links(ax, links_coordinates)

            print("test")

            # グラフ表示更新
            plt.pause(0.01)
            ax.clear()

    def create_links(self, links, coordinates):
        link_coordinates = []
        for vertex1, vertex2 in links:
            if vertex1 in coordinates and vertex2 in coordinates:
                coord1 = coordinates[vertex1]
                coord2 = coordinates[vertex2]
                link_coordinates.append((coord1, coord2))
        return link_coordinates

    def draw_links(self, ax, links_coordinates):
        for link in links_coordinates:
            coords = np.array([link[0], link[1]])
            ax.plot(coords[:, 0], coords[:, 1], coords[:, 2], c="b")
            ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2], c="r", marker="o")