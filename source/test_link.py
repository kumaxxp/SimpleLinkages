import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

# 3Dグラフを作成
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 初期座標
x = [0]
y = [0]
z = [0]

# リンクを表示
link, = ax.plot(x, y, z)

def update(num):
    # リンクの座標を更新
    x.append(num/10)
    y.append(num/2)
    z.append(num/3)
    link.set_data(x, y)
    link.set_3d_properties(z)

ani = animation.FuncAnimation(fig, update, frames=range(10), repeat=True)
plt.show()
