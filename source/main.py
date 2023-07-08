from leg_simulation import Robot
from leg_simulation.shared_data import SharedData
from gui_frame import GraphGui, OpenGLManager, PygameManager, WifiManager

import time
import threading

# 残りの main.py コード
def main():
    # ロボットの初期化
    robot = Robot()
    shared_data = SharedData()
    initial_time = time.time()

    # 各マネージャーのインスタンスを作成
    graph_gui = GraphGui(shared_data)
    opengl_manager = OpenGLManager(initial_time, shared_data)
    pygame_manager = PygameManager(shared_data)
    wifi_manager = WifiManager(shared_data)

    # スレッドリスト
    threaded_managers = [opengl_manager, pygame_manager, wifi_manager]

    # スレッドリストに沿って、スレッドを初期化して実行
    threads = []
    for manager in threaded_managers:
        thread = threading.Thread(target=manager.run)
        threads.append(thread)
        thread.start()

    # Start the GUI manager in the main thread
    graph_gui.run()

    # Join threads after GUI manager finishes running
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()

