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


----

2023/7/2
必要な作業

+ PCからの切断後、再接続待ちになるようにArduino側のソフトを改良する...完了
+ Constructを使って、通信データのパースが楽にできるように実装する...完了
+ サーボからの角度データ、電圧を受信して、PC側に表示する
  + Arduinoのwifiテストサンプルをサーボコントロール側にマージする...完了
+ PC側の機構データに反映して、脚の角度が可視化できるようにする
  + ワイヤーフレーム表示に反映する
    + まず、wifi-test.pyの実装をmain.pyにマージして、通信データを受信...完了
    + 他のライブラリとの関係をクラス図にして、受信したデータを
        self.robot.set_angles(theta1, theta2)
        self.robot.update_position()
      の形で値をセットして、アップデートして角度を決める。
      サーボのポイントから角度を割り出す関数を作成して、その角度をrobotにセットする。
    


+ 原点調整ができるようにする。調整モードで立ち上げた後、微調整してファイルに保存し、次回起動時は微調整値を読み込んで起動する

```plantuml
@startuml

class Robot <<Singleton>> {
}

class SharedData {

}

class GraphGui {
    +run()
}

GraphGui -left- SharedData 

class OpenGLManager {
   +run()
}

OpenGLManager -- Robot 

class PygameManager {
    +run()
}

PygameManager -- Robot 

class WifiManager {
    +run()
}

WifiManager -right- SharedData 

SharedData o-u- Robot 

note top of OpenGLManager
  ロボットを3D表示する
end note

note top of PygameManager
  ロボットを2D表示する
end note

note left of Robot
  ロボットの情報を保持
  現在の状態を常時計算する
  <b>スイッチの切り替え</b>で、
  wifi経由で実機を反映するか、
  PCのシミュレーションか選択
end note

note bottom of WifiManager
  実機とWifi接続して、
  ハードのデータを取得する
end note

note bottom of GraphGui
  PCのGUIからユーザの
  入力を取得する
end note

note bottom of SharedData
  スレッドセーフに
  データを共有する
end note

@enduml

```