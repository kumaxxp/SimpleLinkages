import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import *
import matplotlib.dates as mdates

from leg_simulation import Robot
from leg_simulation.shared_data import SharedData, ServoCmd, ArduinoCommand

from typing import List

COUNT = 5

THETA1_MIN = -90
THETA1_MAX = 0

THETA2_MIN = -180
THETA2_MAX = -90

class GraphGui:
    def __init__(self, shared_data:SharedData):
        self.shared_data = shared_data
        self.root = tk.Tk()
        self.root.title("Time-Speed Graph")

        self.robot = Robot()  # robot インスタンスを初期化

        self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=100)

        # Create a canvas with the figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Angle theta1 slider settings
        self.theta1_slider = tk.Scale(self.root, from_=THETA1_MIN, to=THETA1_MAX, orient=tk.HORIZONTAL,
                                 command=self.update_angles, label="Theta1")
        self.theta1_slider.set(-45)  # Set the default value for Theta1
        self.theta1_slider.pack(fill=tk.X, expand=True)

        # Angle theta2 slider settings
        self.theta2_slider = tk.Scale(self.root, from_=THETA2_MIN, to=THETA2_MAX, orient=tk.HORIZONTAL,
                                 command=self.update_angles, label="Theta2")
        self.theta2_slider.set(-115)  # Set the default value for Theta2
        self.theta2_slider.pack(fill=tk.X, expand=True)

        
        self.is_auto = tk.BooleanVar()  # 追加: 手動/自動 フラグ
        self.is_auto.set(False)  # 追加: 真 (True) で自動モード
        self.manual_auto_button = tk.Checkbutton(self.root, text="Auto", variable=self.is_auto,
                                                 command=self.switch_manual_auto)
        self.manual_auto_button.pack()


        # Speed slider settings
        self.speed_slider = tk.Scale(self.root, from_=0, to=10, orient=tk.HORIZONTAL,
                                 command=self.update_speed, label="Speed")
        self.speed_slider.set(5)  # Set the default value for Speed
        self.speed_slider.pack(fill=tk.X, expand=True)

        self.plot_time_speed_graph()

        # 最初のグラフの更新を予約
        self.update_graph()

    def update_angles(self, *args):
        a_angle : List[float] = [0.0] * 7

        if self.is_auto.get():  # 追加: 自動モードの場合に更新
            theta1 = self.theta1_slider.get()
            theta2 = self.theta2_slider.get()

            servo_cmd = ServoCmd()
            if self.is_auto.get() == True & servo_cmd.command != ArduinoCommand.AUTOMATIC:
                servo_cmd.command = ArduinoCommand.AUTOMATIC
            elif self.is_auto.get() == False & servo_cmd.command != ArduinoCommand.MANUAL:
                servo_cmd.command = ArduinoCommand.MANUAL

            # GUIからの入力を送信する
            a_angle[0] = theta1
            a_angle[1] = theta2

            a_angle_puls = self.robot.convert_angle_list_to_pulse(a_angle)
            self.shared_data.servo_cmd = a_angle_puls

            print(self.shared_data.servo_cmd)

            # Update the robot's angles and recalculate its position
            self.robot.set_angles(theta1, theta2)
            self.robot.update_position()

    def update_speed(self, value):
        speed = float(value)
        timestamp = datetime.now()

        # Save the new speed value to shared_data
        self.shared_data.set_data('speed', timestamp, speed)

    def plot_time_speed_graph(self, *args):
        self.ax.clear()

        # Use the get_data method with a specific key
        data_points = self.shared_data.get_data('speed')

        # Separate timestamps and speeds
        times = [t for t, speed in data_points]
        speeds = [speed for t, speed in data_points]

        self.ax.plot(times, speeds)

        # Set x-axis limits to show only the last 10 seconds
        self.ax.set_xlim([datetime.now() - timedelta(seconds=10), datetime.now()])
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

        self.canvas.draw()

    def update_graph(self):
        # plot_time_speed_graph を呼び出してグラフを更新
        self.plot_time_speed_graph()

        # 次の更新の予約 (1000ms = 1s 後)
        self.root.after(10, self.update_graph)

    def switch_manual_auto(self):  # 追加: ボタンクリック時の処理
        if self.is_auto.get():
            self.manual_auto_button.config(text="Auto")
            # ここに自動処理を記述します
        else:
            self.manual_auto_button.config(text="Manual")


    def run(self):
        self.root.mainloop()
