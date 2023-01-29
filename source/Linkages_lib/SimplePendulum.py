from numpy import sin, cos
from scipy.integrate import solve_ivp
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np

import scipy.constants as const

print(const.g)

g = 10                                 # 重力加速度 [m/s^2]
l = 1                                 # 振り子の長さ [m]

def models(t, state):# 運動方程式
    dy = np.zeros_like(state)
    dy[0] = state[1]
    dy[1] = -(const.g/l)*sin(state[0])
    return dy

t_span = [0,20]                         # 観測時間 [s]
dt = 0.05                               # 間隔 [s]
t = np.arange(t_span[0], t_span[1], dt)
phi_0 = 180.0                              # 初期角度 [deg]
omega_0 = 0.0                                # 初期角速度 [deg/s]

state = np.radians([phi_0, omega_0])           # 初期状態

results = solve_ivp(models, t_span, state, t_eval=t)
phi = results.y[0,:]

plt.plot(phi)

x = l * sin(phi)       
y = -l * cos(phi)      

fig, ax = plt.subplots()

line, = ax.plot([], [], 'o-', linewidth=2) # このlineに次々と座標を代入して描画

def animation(i):
    thisx = [0, x[i]]
    thisy = [0, y[i]]

    line.set_data(thisx, thisy)
    return line,

ani = FuncAnimation(fig, animation, frames=np.arange(0, len(t)), interval=25, blit=True)

ax.set_xlim(-l,l)
ax.set_ylim(-l,l)
ax.set_aspect('equal')
ax.grid()
plt.show()

ani.save('pendulum.gif', writer='pillow', fps=15)