import time
import threading

from gui_manager import GuiManager
from opengl_manager import OpenGLManager
from pygame_manager import PygameManager

from config import speed

def main():

    # インスタンス化
    gui_mgr = GuiManager()
    pygame_mgr = PygameManager()

    initial_time = time.time()

    # Start the GUI manager
    gui_thread = threading.Thread(target=gui_mgr.start_gui)
    gui_thread.start()
    
    # Start the Pygame manager
    pygame_thread = threading.Thread(target=pygame_mgr.draw_pygame_window)
    pygame_thread.start()

    # Initialize and start the OpenGL manager
    opengl_mgr = OpenGLManager(
        initial_time=initial_time,
        speed=speed
    )
    opengl_mgr.run()

if __name__ == "__main__":
    main()
