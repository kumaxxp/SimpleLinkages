import math
import numpy as np

# 4節リンクのA,B,C頂点を取り込んで、足先リンクの座標を計算する
# 足先リンクの頂点B,E,F,Gを計算する（Bは共有）。機構的に確定する。
# Fを中点とする線分I,Jは地面に平行に倣う性質を持つ。それにより⊿EFJの角度が確定し、頂点Hの位置が確定する
# HとGの距離が変化して、100mmよりも小さくなればその分エネルギーがたまっている。


class LinkageHoot:
    def __init__(self, initial_parameters, linkage4bar_instance):
        pass


