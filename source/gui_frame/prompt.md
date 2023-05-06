# ChatGPTに作業させるためのプロンプト

作業は以下の手順で行う。
+ 試作のプログラムを書く
+ テストコードを書く
+ テスト結果で問題があれば、chatGPTに修正してもらう
+ 正常動作したらクラスの仕様書を書く

この手順で実施することで、品質の高いソースコードを出力することができる。
クラス単独で機能を完結できるようにし、最終的にmainのループの中から呼び出すか、スレッドで起動できる形で実装する。


## クラスの仕様を書いてもらう

試作のソースコードを元に、クラス図を書いてもらうプロンプト。

---
xxxクラスの機能を表した詳細な仕様を説明してください。
仕様を読んだプログラマがpythonで実装できるように書いてください。
マークダウンでお願いします。

関数一覧は、以下のように整えてください。

#### 初期化関数 `__init__(self, )`
- 引数：
- 機能：

また、クラス図をplantumlで詳細に書いて実装に役立てることができるようにしてください。
以下、ソースコードです。

(以下、ソースを貼り付ける)

---

### スレッドで動かし、スレッド間でデータを共有する
スレッドを使用する場合は、以下のプロンプトを追加します。

---

このクラスはスレッドで起動できるようにします。

#### 実装例(objectというクラスを使用する場合)
スレッドセーフなデータ共有クラスSharedDataのインスタンスをインポートして初期化し、スレッド間で共有するデータがあるなら利用します。
(必要であればSharedDataクラスの実装をコピーします)

mainから以下のように初期化して実行を開始する想定でクラスを実装します。

```
    object_manager = object(shared_data)
    object_thread = threading.Thread(target=object_manager.run)
    object_thread.start()
    object_thread.join()
```

---

### mainループで動かすtkinterのGUIで、スレッド間でデータを共有する
tkinterでGUIを実装する場合、スレッドで動かすことが奨励されないため、サンプルのように実装します。
スレッドセーフなデータ共有クラスSharedDataのインスタンスをインポートして初期化し、スレッド間で共有するデータがあるなら利用します。
(必要であればSharedDataクラスの実装をコピーします)

mainから以下のように初期化して実行を開始する想定でクラスを実装します。
```
    object_manager = object(shared_data)
    object_thread.run()
```

このクラスの初期化や実行、コールバックの実装例です。
```
import tkinter as tk

class GuiManager(tk.Tk):
    def __init__(self, shared_data):
        super().__init__()
        self.title("GUI Manager")

    def _on_slider_change(self, value):
        self.shared_data.set_value("speed", float(value))

    def run(self):
        super().mainloop() # Change this line
```

### ディレクトリ構造を整えて、ライブラリの構成を初期化する

main.pyから、leg_simulationディレクトリのすべてのライブラリを呼び出すことができるように、__init__.pyを作ってください。
また、gui_frameディレクトリのライブラリも呼び出せるように__init__.pyを設定してください。

ディレクトリ構成は以下のようになっています。

source/
├── main.py
├── leg_simulation/
│   ├── leg.py
│   ├── linkage4bar.py
│   ├── linkage5bar.py
│   └── robot.py
│
├── gui_frame/
│   ├── GraphGui.py
│   ├── opengl_manager.py
│   ├── pygame_manager.py
│   └── shared_data.py


-------
課題1

脚の座標系はOKだが、ロボットの座標系はどのように決定したらよいか？
ロボットの未確定の座標系を中心に、脚の座標が伸びている。
仮に脚が両方とも地面と接しているとして、ロボットの座標系を計算する。それを初期値として設定する。

-------


-------
課題2

USBを経由してシリアル通信を行い、シリアルサーボと通信する。
このプログラムと同じ動きをハードウェアがするかどうかを比較、検証します。

-------

