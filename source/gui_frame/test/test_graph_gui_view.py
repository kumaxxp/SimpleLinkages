import sys
sys.path.append("../")
import time
import threading

from shared_data import SharedData
from GraphGui import GraphGui


class DataUpdater:
    def __init__(self, shared_data):
        self.shared_data = shared_data
        self.data_update_thread = threading.Thread(target=self.update_data)
        self.data_update_thread.start()

    def update_data(self):
        current_speed = 100
        while True:
            timestamp_ms = int(time.time() * 1000)
            self.shared_data.set_data("speed", timestamp_ms, current_speed)
            current_speed -= 10
            if current_speed < 0:
                current_speed = 100

            time.sleep(1) # Wait for 1 second before the next update


def main():
    shared_data = SharedData()

    data_updater = DataUpdater(shared_data)
    graph_gui = GraphGui(shared_data)
    graph_gui.run()

if __name__ == "__main__":
    main()
