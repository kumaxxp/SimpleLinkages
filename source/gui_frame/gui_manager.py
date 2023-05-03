import tkinter as tk
from draw_graph import run_simulation

class GuiManager():
    def __init__(self):
        super().__init__()
        self.title("GUI Manager")

        # ここにGUIのコンポーネントとイベントハンドラを追加
        self.start_button = tk.Button(self, text="Start Simulation", command=self.start_simulation)
        self.start_button.pack()

    def run(self):
        run_simulation()
        self.mainloop()
