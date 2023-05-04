import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class GraphGui:
    def __init__(self, shared_data):
        self.shared_data = shared_data
        self.root = tk.Tk()
        self.root.title("Time-Speed Graph")
        
        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.plot = self.figure.add_subplot(1, 1, 1)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # スライダーのコールバック関数を変更
        self.scale = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, command=self.plot_time_speed_graph)
        self.scale.pack(fill=tk.X, expand=True)

        self.plot_time_speed_graph()

        # 最初のグラフの更新を予約
        self.update_graph()

    def plot_time_speed_graph(self, *args):
        time_data = self.shared_data["time"]
        speed_data = self.shared_data["speed"]

        self.plot.clear()
        self.plot.plot(time_data, speed_data, label="Speed vs Time")
        self.plot.set_title("Time-Speed Graph")
        self.plot.set_xlabel("Time")
        self.plot.set_ylabel("Speed")
        self.plot.legend()

        self.canvas.draw()

    def update_graph(self):
        # plot_time_speed_graph を呼び出してグラフを更新
        self.plot_time_speed_graph()

        # 次の更新の予約 (1000ms = 1s 後)
        self.root.after(1000, self.update_graph)

        print('update_graph')

    def run(self):
        self.root.mainloop()