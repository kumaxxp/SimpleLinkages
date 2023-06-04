import threading
import numpy as np

import matplotlib
matplotlib.use('TkAgg')
import pygame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import tkinter as tk

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from config import SCALE_FACTOR, WINDOW_WIDTH, WINDOW_HEIGHT
from leg_simulation import Robot


class PlotManager(threading.Thread):
    def __init__(self, initial_time, shared_data):
        super().__init__()
        self.shared_data = shared_data
        self.initial_time = initial_time
        self.robot = Robot()
        self.scale_factor = float(SCALE_FACTOR)

    def run(self):
        self.init_plot()

    def init_plot(self):
        root = tk.Tk()
        fig = plt.figure(figsize=(WINDOW_WIDTH / 80, WINDOW_HEIGHT / 80), dpi=80)
        ax = fig.add_subplot(111, projection="3d")

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pygame Window")

        def update_plot():
            positions = self.robot.get_positions()
            link_list = self.robot.get_link_list()

            transformed_coordinates = {key: self.convert_coordinates(coord, WINDOW_WIDTH, WINDOW_HEIGHT) for key, coord in positions.items()}
            links_coordinates = self.create_links(link_list, transformed_coordinates, 0.0)

            ax.clear()
            self.draw_links(ax, links_coordinates)

            canvas.draw()

            root.after(10, update_plot)

        update_plot()
        root.mainloop()

    def create_links(self, links, coordinates, t):
        link_coordinates = []
        for vertex1, vertex2 in links:
            if vertex1 in coordinates and vertex2 in coordinates:
                coord1 = coordinates[vertex1][0], coordinates[vertex1][1], t
                coord2 = coordinates[vertex2][0], coordinates[vertex2][1], t
                link_coordinates.append((coord1, coord2))
        return link_coordinates

    def convert_coordinates(self, coord, screen_width, screen_height):
        x, y = coord
        x_transformed = int((x * self.scale_factor) + screen_width // 2)
        y_transformed = int((-y * self.scale_factor) + screen_height // 2)
        return x_transformed, y_transformed

    def draw_links(self, ax, links_coordinates):
        for link in links_coordinates:
            coords = np.array([link[0], link[1]])
            ax.plot(coords[:, 0], coords[:, 1], coords[:, 2], c="b")
            ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2], c="r", marker="o")


if __name__ == "__main__":
    plot_manager = PlotManager(0, None)
    plot_manager.run()
