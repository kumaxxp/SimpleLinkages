import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class GuiManagerWithPlot(GuiManager):
    def __init__(self, shared_data):
        super().__init__(shared_data)

        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.plot = self.figure.add_subplot(1, 1, 1)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        
        # ボタンの下にプロットを配置
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.plot_time_speed_graph()

    def plot_time_speed_graph(self):
        time_data = self.shared_data["time"]
        speed_data = self.shared_data["speed"]

        self.plot.clear()
        self.plot.plot(time_data, speed_data, label="Speed vs Time")
        self.plot.set_title("Time-Speed Graph")
        self.plot.set_xlabel("Time")
        self.plot.set_ylabel("Speed")
        self.plot.legend()

        self.canvas.draw()

    def _on_slider_change(self, value):
        super()._on_slider_change(value)
        self.plot_time_speed_graph()