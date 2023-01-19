#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Linkages_lib.FourBarLinkage as FourBarLinkage
import Linkages_graph.linkage_graph as linkage_graph

def link_machine():
    print("start four_bar_links")

    graph = linkage_graph()

    # リンクの長さ比
    # a : b : e = 100 : 160 : 100
    # f : g = 113.13 : 50
    # Z平面の位置
    four_bar = FourBarLinkage(a=0.025313, b=0.04050137, e=0.025313, g=0.010, angle_phi=60, angle_delta=0)
    four_bar.update_positions()

    Ex = -200
    Ey = -200

    while True:

        # 角度変更
        four_bar.update_inverse_kinematics(x=four_bar.pos_ellipse[0] , y=four_bar.pos_ellipse[1] )
        four_bar.culc_ellipse()

        four_bar.update_positions()
        graph.draw(four_bar)

if __name__ == '__main__':
    link_machine()
