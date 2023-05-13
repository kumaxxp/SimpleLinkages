# SimpleLinkages
Simple Linkages for my robots
自作リンクロボットの簡単な4節リンクのプログラムを検討。
4節リンクの動きをシミュレートして可視化し、設計を検討します。
4節リンク/リンク/ピン の3つのクラスを作成して、順々に進化させていきます。

**設計概要**

順運動で計算する場合、この構造はモーターの角度から5節リンク4節リンクの計算を順番に解いていくことで計算することができる。
また、以下のように単純化して計算することも可能となる。
<img src = "./doc/5節リンクのプログラムを検討2.drawio.png" width = 600>



**単純化**

逆運動を計算するとき、下の図のように構造を単純化して計算する。
B1-Yの長さはb、Y-Eの長さはl1+a+e、リンクE-Iの相互関係は固定されているので計算可能、E-I-Jの角度はFのモーターの角度と同じ値となる。B1-Y-Eの角度はB1,B2の角度によって割り出すことができるので、逆算も可能。

**逆運動**

歩行を単純に考えるため、IとJのどちらか、もしくは両方が接地している条件で逆運動計算をして、B1,B2の角度を確定させてから、順運動で各頂点の位置とリンクの角度を決定する。
例えば、I-Jが接地している条件で、IのX座標の位置を指定する。
Eの位置をIから相対的に割り出すと、逆運動によってB1,B2の角度を計算することができる。


<img src = "./doc/5節リンクのプログラムを単純化.drawio.png" width = 600>

---

# 設計

## 検討資料


[4節リンクのプログラムを検討](./doc/4節リンクのプログラム.md)を参照。

## 構成

以下のようなディレクトリ構成にします。

```
.
├── Linkages_lib
│   ├── __init__.py
│   ├── cpin.py
│   ├── clink.py
│   └── CFourBarLinkage.py
│
├── Linkages_lib_cli
│   └── call.py
└── setup.py

Python 3.8.10
OpenCV 4.5.4
moviepy 1.0.3

pip install moviepy 

Circle3D

## minicondaにsympyをインストールする
conda install sympy

```

PyDyで計算できそう
https://pydy.readthedocs.io/en/stable/examples/rocket-car.html
