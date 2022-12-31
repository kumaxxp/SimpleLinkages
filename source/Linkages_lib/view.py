import cv2
import numpy as np

# 画像のサイズ（ピクセル）
width = 800
height = 600

# 画像を生成する
img = np.zeros((height, width, 3), np.uint8)

# 軸の色
axis_color = (255, 255, 255)

# 方眼のステップ（ピクセル）
grid_step = 50

# 縦軸を描画する
for x in range(0, width, grid_step):
    cv2.line(img, (x, 0), (x, height), axis_color, 1)

# 横軸を描画する
for y in range(0, height, grid_step):
    cv2.line(img, (0, y), (width, y), axis_color, 1)

# データを生成する
data = [(x, np.sin(x)) for x in np.linspace(0, 2*np.pi, 50)]

# データを描画する
for x, y in data:
    # データをスクリーン座標に変換する
    sx = int(x / (2*np.pi) * width)
    sy = int((y + 1) / 2 * height)
    
    # データを描画する
    cv2.circle(img, (sx, sy), 3, (0, 0, 255), -1)

# 画像を表示する
cv2.imshow("image", img)
cv2.waitKey(0)
