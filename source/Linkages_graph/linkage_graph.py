#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 複数の１次元配列を表示する3次元リアルタイムグラフ
# Library
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt # グラフ表示のため
from mpl_toolkits.mplot3d import Axes3D # ３Dグラフ作成のため
import mpl_toolkits.mplot3d.art3d as art3d
from matplotlib.patches import Arc
from matplotlib.patches import Circle

import Linkages_lib.FourBarLinkage as FourBarLinkage

class linkage_graph:
    def __init__(self):
        # params
        self.frame = 1500  # プロットするフレーム数
        self.sleepTime = 0.05  # １フレーム表示する時間[s]
        self.dataLength = 10  # １次元配列データの長さ
        self.dataAmount = 3 # １度にプロットする１次元配列データの個数
        self.zMax = 1 # z軸最大値
        self.zMin = -1 # z軸最小値
        self.xlabel = "x axis"
        self.ylabel = "y axis"
        self.zlabel = "z axis"
        self.colorsets = 'skyblue'
        self.xfigSize = 14 #　グラフを表示するウインドウのx方向の大きさ
        self.yfigSize = 10 #　グラフを表示するウインドウのy方向の大きさ
        self.Alpha = 1.0 # プロットした線の透明度

        # making stylish graph
        if self.colorsets == 'skyblue':
            color1 = '#FFFFFF'  # background
            color2 = '#C7D7FF'  # background2
            color3 = '#5BB1E3'  # accent color red: DE5E34 blue: 5BB1E3
            color4 = '#4C4C4C'  # axis

        plt.rcParams.update({
            'figure.figsize': [self.xfigSize, self.yfigSize],
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
        self.fig = plt.figure() # figureオブジェクトを作る
        self.ax = Axes3D(self.fig)

        # ３dグラフの背景を透明にする　最初の一回だけでOK
        self.ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

        # plot setting
        self.ax.set_zlim(self.zMin, self.zMax) # z軸固定
        self.ax.set_xlim(-1, 1) # x軸固定
        self.ax.set_ylim(-1, 1) # y軸固定
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)
        self.ax.set_zlabel(self.zlabel)

        plt.ion()
        self.ax.view_init(elev=8, azim=28)
        
    def draw_link(self, four_bar:FourBarLinkage, z:float = 0):
        
        aZ = [z,z]
        line_a= art3d.Line3D(aZ, [four_bar.A[0],four_bar.D[0]],[four_bar.A[1],four_bar.D[1]], color = 'r')
        self.ax.add_line(line_a)

        line_b= art3d.Line3D(aZ, [four_bar.A[0],four_bar.B[0]],[four_bar.A[1],four_bar.B[1]], color = 'c')
        self.ax.add_line(line_b)

        line_c= art3d.Line3D(aZ, [four_bar.C[0],four_bar.B[0]],[four_bar.C[1],four_bar.B[1]], color = 'c')
        self.ax.add_line(line_c)

        line_d= art3d.Line3D(aZ, [four_bar.C[0],four_bar.D[0]],[four_bar.C[1],four_bar.D[1]], color = 'b')
        self.ax.add_line(line_d)

        line_e= art3d.Line3D(aZ, [four_bar.B[0],four_bar.E[0]],[four_bar.B[1],four_bar.E[1]], color = 'c')
        self.ax.add_line(line_e)

        line_f= art3d.Line3D(aZ, [four_bar.D[0],four_bar.F[0]],[four_bar.D[1],four_bar.F[1]], color = 'g')
        self.ax.add_line(line_f)

        line_g= art3d.Line3D(aZ, [four_bar.G[0],four_bar.F[0]],[four_bar.G[1],four_bar.F[1]], color = 'r')
        self.ax.add_line(line_g)

        line_h= art3d.Line3D(aZ, [four_bar.G[0],four_bar.H[0]],[four_bar.G[1],four_bar.H[1]], color = 'c')
        self.ax.add_line(line_h)

        line_dd= art3d.Line3D(aZ, [four_bar.D[0],four_bar.H[0]],[four_bar.D[1],four_bar.H[1]], color = 'b')
        self.ax.add_line(line_dd)

        q = Arc((four_bar.D[0], four_bar.D[1]), width=0.005, height=0.005, angle=0, theta1=0, theta2=90, color="blue")
        self.ax.add_patch(q)
        art3d.pathpatch_2d_to_3d(q, z=z, zdir="x")

    def draw(self, four_bar_front:FourBarLinkage, four_bar_rear):

        # リンクの座標を描画する
        self.draw_link(four_bar_front, 0)
        self.draw_link(four_bar_rear, 0.02)

        plt.draw()
        self.ax.set_xlim(-0.1, 0.1)
        self.ax.set_ylim(-0.1, 0.1)
        self.ax.set_zlim(-0.1, 0.1)
        
        plt.pause(self.sleepTime)
        
        plt.cla()
