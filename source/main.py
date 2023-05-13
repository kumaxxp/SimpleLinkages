from leg_simulation import Robot
from gui_frame import GraphGui, OpenGLManager, PygameManager, SharedData, PlotManager

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
    plot_manager   = PlotManager(initial_time, shared_data)

    # 別スレッドで実行
    opengl_thread = threading.Thread(target=opengl_manager.run)
    pygame_thread = threading.Thread(target=pygame_manager.run)
    plot_thread   = threading.Thread(target=plot_manager.run)

    opengl_thread.start()
    pygame_thread.start()
    plot_thread.start()

    # Start the GUI manager in the main thread
    graph_gui.run()

    opengl_thread.join()
    pygame_thread.join()
    plot_thread.join()

if __name__ == "__main__":
    main()

