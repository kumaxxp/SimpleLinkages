# 複数の１次元配列を表示する3次元リアルタイムグラフ
# Library   
import numpy as np # プロットするデータ配列を作成するため
import matplotlib.pyplot as plt # グラフ表示のため
from mpl_toolkits.mplot3d import Axes3D # ３Dグラフ作成のため
import mpl_toolkits.mplot3d.art3d as art3d

# params
frame = 1500  # プロットするフレーム数
sleepTime = 0.05  # １フレーム表示する時間[s]
dataLength = 10  # １次元配列データの長さ
dataAmount = 3 # １度にプロットする１次元配列データの個数
zMax = 10 # z軸最大値
zMin = 0 # z軸最小値
xlabel = "x axis"
ylabel = "y axis"
zlabel = "z axis"
colorsets = 'skyblue'
xfigSize = 14 #　グラフを表示するウインドウのx方向の大きさ
yfigSize = 10 #　グラフを表示するウインドウのy方向の大きさ
Alpha = 1.0 # プロットした線の透明度

# making stylish graph
if colorsets == 'skyblue':
    color1 = '#FFFFFF'  # background
    color2 = '#C7D7FF'  # background2
    color3 = '#5BB1E3'  # accent color red: DE5E34 blue: 5BB1E3
    color4 = '#4C4C4C'  # axis

plt.rcParams.update({
    'figure.figsize': [xfigSize, yfigSize],
    # 'axes.grid': False,
    'axes3d.grid': True,
    'grid.alpha': 0.2,
    'grid.linestyle': '-',
    'axes.grid.which': 'major',
    'axes.grid.axis': 'y',
    'grid.linewidth': 0.1,
    'font.size': 10,
    'grid.color': color4,
    'xtick.color': color4,  # x軸の色
    'ytick.color': color4,  # y軸の色
    'figure.facecolor': color1,  # 枠の外の背景色
    'figure.edgecolor': color1,
    'axes.edgecolor': color1,  # 枠色
    'axes.facecolor': 'none',  # 背景色　noneにするとfigure.facecolorと同じ色になった
    'axes.labelcolor': color4,  # 軸ラベル色
    'figure.dpi': 75.0,
    'figure.frameon': False,
})

# making 3d figure object
fig = plt.figure() # figureオブジェクトを作る
ax = Axes3D(fig)

ax.w_xaxis.set_pane_color((0., 0., 0., 0.))  # ３dグラフの背景を透明にする　最初の一回だけでOK
ax.w_yaxis.set_pane_color((0., 0., 0., 0.))  # ３dグラフの背景を透明にする
ax.w_zaxis.set_pane_color((0., 0., 0., 0.))  # ３dグラフの背景を透明にする

# plot setting
ax.set_zlim(zMin, zMax) # z軸固定
ax.set_xlabel(xlabel)
ax.set_ylabel(ylabel)
ax.set_zlabel(zlabel)

plt.ion()

x1 = 0
for i in range(frame):

    # ここで必要数分だけlineを引いて、add_lineしたらすべて表示できそう
    x1 = x1+ 0.1
    line= art3d.Line3D([x1,0.2],[0.3,0.4],[0,0], color = 'c')
    ax.add_line(line)

    plt.draw()
    plt.pause(sleepTime)
    plt.cla()   

    