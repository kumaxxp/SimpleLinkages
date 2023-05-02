# gui_input.py
import tkinter as tk
import threading

slider_value = 0
value_lock = threading.Lock()

def slider_moved(value):
    global slider_value
    with value_lock:
        slider_value = int(value)

def run_tkinter_gui():
    window = tk.Tk()
    window.title("Tkinter Slider Example")
    
    # スライダの長さを 500 に設定
    slider = tk.Scale(window, from_=0, to=100, orient=tk.HORIZONTAL, command=slider_moved, length=300)
    slider.pack()

    window.mainloop()

def start_gui_thread():
    tkinter_thread = threading.Thread(target=run_tkinter_gui, daemon=True)
    tkinter_thread.start()

def get_slider_value():
    with value_lock:
        return slider_value