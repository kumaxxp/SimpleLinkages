import random
import sys
import time

sys.path.append("../")
from GraphGui import GraphGui

def generate_initial_data():
    shared_data = {"time": [], "speed": []}
    for i in range(10):
        shared_data["time"].append(i)
        shared_data["speed"].append(random.randint(0, 100))
    return shared_data

def update_data(shared_data):
    current_time = len(shared_data['time'])
    shared_data['time'].append(current_time)
    shared_data['speed'].append(random.randint(0, 100))

def main():
    # サンプルデータ生成
    shared_data = generate_initial_data()

    # GraphGui のインスタンス生成
    graph_gui = GraphGui(shared_data)

    print("Running GraphGui, close the window to stop.")

    # グラフィックウィンドウの実行
    graph_gui.run()

    # スライダコントロールのデータを取得して shared_data を更新
    while graph_gui.is_running():
        time.sleep(1)  # 1秒待つ
        update_data(shared_data)
        graph_gui.update_plot(shared_data)

    print("GraphGui closed.")

if __name__ == "__main__":
    main()
