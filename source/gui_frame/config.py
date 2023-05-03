WINDOW_WIDTH = 800
WINDOW_HEIGHT = 1000
NEAR_CLIP_PLANE = 0.1
FAR_CLIP_PLANE = 100.0

import threading

speed = 1.0
speed_lock = threading.Lock()

def set_speed(new_speed):
    global speed
    with speed_lock:
        speed = new_speed
