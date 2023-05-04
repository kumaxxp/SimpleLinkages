import sys
sys.path.append("../")

import time
from shared_data import SharedData
from GraphGui import GraphGui

class GraphGuiWithSpeedUpdate(GraphGui):
    def __init__(self, shared_data):
        self.current_speed = 100
        super().__init__(shared_data)

    def update_graph(self):
        # plot_time_speed_graph を呼び出してグラフを更新
        self.plot_time_speed_graph()

        # 次の更新の予約 (1000ms = 1s 後)
        self.root.after(1000, self.update_graph)

        # Add new speed data
        timestamp_ms = int(time.time() * 1000)
        self.shared_data.set_data("speed", timestamp_ms, self.current_speed)
        self.current_speed -= 10
        if self.current_speed < 0:
            self.current_speed = 100

        print('update_graph')

def main():
    shared_data = SharedData()

    graph_gui = GraphGuiWithSpeedUpdate(shared_data)
    graph_gui.run()

if __name__ == "__main__":
    main()
