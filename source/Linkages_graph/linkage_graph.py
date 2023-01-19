#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 複数の１次元配列を表示する3次元リアルタイムグラフ
# Library
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt # グラフ表示のため
from mpl_toolkits.mplot3d import Axes3D # ３Dグラフ作成のため
import mpl_toolkits.mplot3d.art3d as art3d

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

        self.ax.w_xaxis.set_pane_color((0., 0., 0., 0.))  # ３dグラフの背景を透明にする　最初の一回だけでOK
        self.ax.w_yaxis.set_pane_color((0., 0., 0., 0.))  # ３dグラフの背景を透明にする
        self.ax.w_zaxis.set_pane_color((0., 0., 0., 0.))  # ３dグラフの背景を透明にする

        # plot setting
        self.ax.set_zlim(self.zMin, self.zMax) # z軸固定
        self.ax.set_xlim(-1, 1) # x軸固定
        self.ax.set_ylim(-1, 1) # y軸固定
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)
        self.ax.set_zlabel(self.zlabel)

        plt.ion()

    def draw(self, four_bar:FourBarLinkage):

        # ここで必要数分だけlineを引いて、add_lineしたらすべて表示できそう
        
        line_a= art3d.Line3D([four_bar.A[0],four_bar.D[0]],[four_bar.A[1],four_bar.D[1]],[0,0], color = 'c')
        self.ax.add_line(line_a)

        line_b= art3d.Line3D([four_bar.A[0],four_bar.B[0]],[four_bar.A[1],four_bar.B[1]],[0,0], color = 'c')
        self.ax.add_line(line_b)

        line_c= art3d.Line3D([four_bar.C[0],four_bar.B[0]],[four_bar.C[1],four_bar.B[1]],[0,0], color = 'c')
        self.ax.add_line(line_c)

        line_d= art3d.Line3D([four_bar.C[0],four_bar.D[0]],[four_bar.C[1],four_bar.D[1]],[0,0], color = 'c')
        self.ax.add_line(line_d)


        line_e= art3d.Line3D([four_bar.B[0],four_bar.E[0]],[four_bar.B[1],four_bar.E[1]],[0,0], color = 'c')
        self.ax.add_line(line_e)

        print(four_bar.A,four_bar.C)

        plt.draw()
        plt.pause(self.sleepTime)
        plt.cla()


