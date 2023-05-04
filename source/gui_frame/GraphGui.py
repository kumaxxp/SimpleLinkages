import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import *
import matplotlib.dates as mdates

class GraphGui:
    def __init__(self, shared_data):
        self.shared_data = shared_data
        self.root = tk.Tk()
        self.root.title("Time-Speed Graph")

        self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=100)

        # Create a canvas with the figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # スライダーのコールバック関数を変更
        self.scale = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, command=self.plot_time_speed_graph)
        self.scale.pack(fill=tk.X, expand=True)

        self.plot_time_speed_graph()

        # 最初のグラフの更新を予約
        self.update_graph()

    def plot_time_speed_graph(self, *args):
        self.ax.clear()

        # Use the get_data method with a specific key
        data_points = self.shared_data.get_data('speed')

        # Separate timestamps and speeds
        times = [t for t, speed in data_points]
        speeds = [speed for t, speed in data_points]

        self.ax.plot(times, speeds)

        # Set x-axis limits to show only the last 10 seconds
        self.canvas.draw()

    def update_graph(self):
        # plot_time_speed_graph を呼び出してグラフを更新
        self.plot_time_speed_graph()

        # 次の更新の予約 (1000ms = 1s 後)
        self.root.after(1000, self.update_graph)

        print('update_graph')

    def run(self):
        self.root.mainloop()