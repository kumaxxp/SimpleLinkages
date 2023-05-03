import tkinter as tk
from manager_interface import ManagerInterface

class GuiManager(tk.Tk):
    def __init__(self, shared_data):
        super().__init__()
        self.title("GUI Manager")
        self.shared_data = shared_data

        # Create slider control
        self.scale = tk.Scale(self, from_=0, to=10, resolution=0.01, length=300, orient=tk.HORIZONTAL, command=self._on_slider_change)
        self.scale.set(0) # Initialize with the speed value from config.py
        self.scale.pack()

    def _on_slider_change(self, value):
        self.shared_data.set_value("speed", float(value))

    def run(self):
        root = tk.Tk()
        slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=self._on_slider_change)
        slider.pack()

        root.mainloop()