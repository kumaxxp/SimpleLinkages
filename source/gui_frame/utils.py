import time

def get_color_by_speed(speed):
    # 最小速度と最大速度を定義
    min_speed, max_speed = 0.0, 3.0

    # オブジェクトの色相を計算（速度が低いほど青、高いほど赤になるように設定）
    t = (speed - min_speed) / (max_speed - min_speed)
    r = t
    g = 0
    b = 1 - t

    # クリッピング
    r = min(max(r, 0), 1)
    g = min(max(g, 0), 1)
    b = min(max(b, 0), 1)

    return r, g, b
    
def update_object_position(initial_time, speed):
    elapsed_time = time.time() - initial_time
    x = speed * elapsed_time % 5.0
    return x, 0.0, 0.0
