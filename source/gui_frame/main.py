import time
import threading

from gui_manager import GuiManager
from opengl_manager import OpenGLManager
from pygame_manager import PygameManager
from shared_data import SharedData

from config import speed

def main():
    shared_data = SharedData()
    initial_time = time.time()

    # 各マネージャーのインスタンスを作成
    gui_manager = GuiManager(shared_data)
    opengl_manager = OpenGLManager(initial_time, shared_data)
    pygame_manager = PygameManager(shared_data)

    # 別スレッドで実行
    opengl_thread = threading.Thread(target=opengl_manager.run)
    pygame_thread = threading.Thread(target=pygame_manager.run)

    opengl_thread.start()
    pygame_thread.start()

    # Start the GUI manager in the main thread
    gui_manager.run()

    opengl_thread.join()
    pygame_thread.join()    

if __name__ == "__main__":
    main()
