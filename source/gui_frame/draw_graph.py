import tkinter as tk
from queue import Queue
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time

def update_data(q):
    current_time = 0.0
    while True:
        current_speed = current_time * 2  # Dummy data - replace with actual speed calculations
        q.put((current_time, current_speed))
        current_time += 1
        time.sleep(1)  # Sleep for 1 second before updating data

def update_graph(frame, lines, q, ax):
    while not q.empty():
        time_point, speed_point = q.get()
        time_data.append(time_point)
        speed_data.append(speed_point)
    lines.set_data(time_data, speed_data)
    ax.relim()
    ax.autoscale_view()

def run_simulation(root, time_data, speed_data):
    fig, ax = plt.subplots()
    lines, = ax.plot(time_data, speed_data, '-o')
    ax.set_xlabel('Time')
    ax.set_ylabel('Speed')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Create queue to store data and start updating data
    q = Queue()
    data_thread = threading.Thread(target=update_data, args=(q,))
    data_thread.start()

    # Update tkinter window
    def handle_idle_tasks():
        while True:
            root.update_idletasks()
            root.update()
            time.sleep(0.1)

    idle_tasks_thread = threading.Thread(target=handle_idle_tasks)
    idle_tasks_thread.start()

    ani = animation.FuncAnimation(fig, update_graph, fargs=(lines, q, ax), interval=100, blit=False)
