#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Linkages_lib.FourBarLinkage as FourBarLinkage
import Linkages_graph.linkage_graph as linkage_graph

import termios, fcntl, sys, os


def link_machine():
    print("start four_bar_links")

    # --グラフィックライブラリを使わずキー入力をとる--
    fd = sys.stdin.fileno()

    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)

    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)
    # ------------------------------------------------

    graph = linkage_graph()

    # リンクの長さ比
    # a : b : e = 100 : 160 : 100
    # f : g = 113.13 : 50
    # Z平面の位置
    four_bar = FourBarLinkage(a=0.025313, b=0.04050137, e=0.025313, g=0.010, angle_phi=60, angle_delta=0)
    four_bar.update_positions()

    four_bar2 = FourBarLinkage(a=0.025313, b=0.04050137, e=0.025313, g=0.010, angle_phi=60, angle_delta=0, offset = 300)
    four_bar2.update_positions()

    Ex = -200
    Ey = -200

    while True:
        # キー入力チェック
        try:
            c = sys.stdin.read(1)
            if c == 'q':
                break
        except IOError: pass

        # 角度変更
        four_bar.update_inverse_kinematics(x=four_bar.pos_ellipse[0] , y=four_bar.pos_ellipse[1] )
        four_bar.culc_ellipse()
        four_bar.update_positions()

        four_bar2.update_inverse_kinematics(x=four_bar2.pos_ellipse[0] , y=four_bar2.pos_ellipse[1] )
        four_bar2.culc_ellipse()
        four_bar2.update_positions()

        graph.draw(four_bar, four_bar2)

    # 終了チェック
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

if __name__ == '__main__':
    link_machine()
