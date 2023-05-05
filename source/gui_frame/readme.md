# 歩行ロボットのシミュレーションGUIフレーム

```
project/
|-- main.py
|-- config.py
|-- draw_functions.py
|-- utils.py
|-- window_handlers.py
|-- readme.md
```

各ファイルの説明:

1. `main.py`: プログラムのメイン部分。他のモジュールをインポートして実行します。
2. `config.py`: 全体的な設定を保存する。ウィンドウサイズやカメラ設定など。
3. `draw_functions.py`: オブジェクトの描画に関連する関数を記述する。
4. `utils.py`: 汎用的な関数を保存する。例えば、速度に基づいて色を取得する関数など。
5. `window_handlers.py`: PygameおよびOpenGLのウィンドウ処理とイベント処理を行う。
6. `readme.md`: この文書


-------

main.py - エントリーポイントとしてプログラムを実行
GuiManager - GUI操作を管理
OpenGLManager - 3D画面の描画を担当
PygameManager - 2D画面の描画を担当
SharedData - 変数を共有するためのデータクラス

**初期化**
```plantuml

@startuml

!define main_style #FFD700
!define other_style #98FB98

class main.py << (M, main_style) >> {
  +main()
}

class GuiManager << (O, other_style) >> {
  +__init__(shared_data: SharedData)
  +run(): None
}

class OpenGLManager << (O, other_style) >> {
  +__init__(initial_time: float, shared_data: SharedData)
  +run(): None
}

class PygameManager << (O, other_style) >> {
  +__init__(shared_data: SharedData)
  +run(): None
}

class SharedData << (O, other_style) >> {
  +__init__()
}

main ..> GuiManager: creates
main ..> OpenGLManager: creates
main ..> PygameManager: creates
main -> SharedData: creates

GuiManager --> SharedData: accesses
OpenGLManager --> SharedData: accesses
PygameManager --> SharedData: accesses

@enduml

```

---

**実行時**
```plantuml

@startuml

!define other_style #98FB98

class GuiManager << (O, other_style) >> {
  +__init__(shared_data: SharedData)
  -_on_slider_change(value: float)
  +run(): None
}

class OpenGLManager << (O, other_style) >> {
  +__init__(initial_time: float, shared_data: SharedData)
  +run(): None
  -init_glut(): None
  -display_callback(): None
}

class PygameManager << (O, other_style) >> {
  +__init__(shared_data: SharedData)
  +run(): None
}

class SharedData << (O, other_style) >> {
  +__init__()
  +set_value(key: str, value: Any): None
  +get_value(key: str) -> Union[Any, None]
}

GuiManager -right-> SharedData: accesses
OpenGLManager --> SharedData: accesses
PygameManager -down-> SharedData: accesses
GuiManager --|> tk.Tk

@enduml


```

各クラスの仕様書をChatGPTに書いてもらうため、今まで作ったテスト用のソフトを渡して指示を出します。
以下、指示を出すときのテンプレです。

>OpenGLManagerクラスの機能を表した詳細な仕様を説明してください。
仕様を読んだプログラマがpythonで実装できるように書いてください。
マークダウンでお願いします。
また、OpenGLManagerのクラス図をplantumlで詳細に書いて実装に役立てることができるようにしてください。
以下、ソースコードです。

以下の出力を得ました。

---

以下は、`OpenGLManager` クラスの機能を表した詳細な仕様です。

## OpenGLManagerクラス仕様

### 概要
`OpenGLManager` クラスは、3Dオブジェクトの表示と操作を行うためのクラスです。OpenGLを使用して3Dオブジェクトを描画し、キーボードコールバックを利用してカメラの位置を制御します。

### 初期化関数 `__init__(self, initial_time, shared_data)`
- 引数：
  - `initial_time`: アプリケーションの開始時刻
  - `shared_data`: 他のマネージャと共有するデータを持つ `SharedData` インスタンス
- 機能：`initial_time` と `shared_data` をインスタンス変数に保存します。

### run(self)
- 機能: GLUTを初期化し、ウィンドウを作成します。プロジェクション行列を設定し、GLUTのメインループに入ります。

### init_glut(self)
- 機能: GLUTを初期化し、描画モード、ウィンドウサイズ、ウィンドウタイトルを設定します。深度テストを有効にし、背景色を設定します。さらに、GLUTのコールバック関数を設定します。

### display_callback(self)
- 機能: ディスプレイコールバック関数です。画面をクリアし、`shared_data` から現在の速度を取得します。オブジェクトの位置を更新し、3Dオブジェクトを描画します。カメラの位置を更新し、バッファを入れ替えます。

以下は、`OpenGLManager` クラスの詳細なPlantUMLクラス図です:

```plantuml
@startuml

!define main_style #FFD700
!define other_style #98FB98

class OpenGLManager << (O, other_style) >> {
  -initial_time: float
  -shared_data: SharedData
  +__init__(initial_time: float, shared_data: SharedData): None
  +run(): None
  -init_glut(): None
  -display_callback(): None
}

class SharedData << (O, other_style) >> {
  +__init__()
}

interface draw_functions << (O, other_style) >> {
  +draw_2d_objects(object_position: Tuple[float, float]): None
  +draw_3d_objects(object_position: Tuple[float, float, float]): None
}

interface window_handlers << (O, other_style) >> {
  +set_camera_position(object_position: Tuple[float, float, float]): None
  +keyboard_callback(key: int, x: int, y: int): None
}

OpenGLManager --> SharedData: accesses
OpenGLManager --> draw_functions: uses
OpenGLManager --> window_handlers: uses

@enduml
```

このクラス図では、`OpenGLManager` クラスが `SharedData` クラスとインターフェース (`draw_functions` および `window_handlers`) を使用していることが示されています。また、主要なメソッドと属性がリストされています。これにより、プログラマはクラスを実装する際に必要な情報が得られます。

---

>PygameManagerクラスの機能を表した詳細な仕様を説明してください。
仕様を読んだプログラマがpythonで実装できるように書いてください。
マークダウンでお願いします。
また、PygameManagerのクラス図をplantumlで詳細に書いて実装に役立てることができるようにしてください。
以下、ソースコードです。

以下の出力を得ました。

---

以下は、`PygameManager` クラスの機能を表した詳細な仕様です。

## PygameManagerクラス仕様

### 概要
`PygameManager` クラスは、2Dオブジェクトの表示と制御を行うためのクラスです。Pygameを使用してウィンドウを作成し、2Dオブジェクトを描画します。物体の位置や速度を共有データとして利用します。

### 初期化関数 `__init__(self, shared_data)`
- 引数：
  - `shared_data`: 他のマネージャと共有するデータを持つ `SharedData` インスタンス
- 機能：`shared_data` をインスタンス変数に保存し、時間データ、速度データ、線の色、原点座標、軸スケールを初期化します。

### run(self)
- 機能: Pygameを初期化し、ウィンドウを作成します。ウィンドウタイトルを設定し、イベントループを開始します。画面を更新し、2Dオブジェクトを描画します。終了イベントが発生したらループを抜け、Pygameを終了します。

以下は、`PygameManager` クラスの詳細なPlantUMLクラス図です:

```plantuml
@startuml

!define main_style #FFD700
!define other_style #98FB98

class PygameManager << (O, other_style) >> {
  -shared_data: SharedData
  -time_data: List[float]
  -speed_data: List[float]
  -line_color: Tuple[int, int, int]
  -origin: Tuple[int, int]
  -axis_scale: Tuple[int, int]
  +__init__(shared_data: SharedData): None
  +run(): None
}

class SharedData << (O, other_style) >> {
  +__init__()
}

interface draw_functions << (O, other_style) >> {
  +draw_2d_objects(screen: pygame.Surface): None
}

PygameManager --> SharedData: accesses
PygameManager --> draw_functions: uses

@enduml
```

このクラス図では、`PygameManager` クラスが `SharedData` クラスとインターフェース `draw_functions` を使用していることが示されています。また、主要なメソッドと属性がリストされています。これにより、プログラマはクラスを実装する際に必要な情報が得られます。

---

>GuiManagerクラスの機能を表した詳細な仕様を説明してください。
仕様を読んだプログラマがpythonで実装できるように書いてください。
マークダウンでお願いします。
また、GuiManagerのクラス図をplantumlで詳細に書いて実装に役立てることができるようにしてください。
以下、ソースコードです。

---

以下は、`GuiManager` クラスの機能を表した詳細な仕様です。

## GuiManagerクラス仕様

### 概要
`GuiManager`クラスは、共有データとグラフィカルユーザーインターフェース(GUI)管理用のクラスです。tkinter ライブラリを使用し、スライダーを作成してキー "speed" の値を変更できます。

### 初期化関数 `__init__(self, shared_data)`
- 引数：
  - `shared_data`: SharedData オブジェクト
- 機能：ウィンドウタイトルと共有データポインタを設定します。また、水平スライダーも作成し、初期値を 0 に設定します。スライダーが変更されるたびに、`_on_slider_change` 関数が呼び出されます。

### _on_slider_change(self, value)
- 引数：
  - `value`: スライダーから取得した新しい値
- 機能：共有データオブジェクト内のキー "speed" の値をスライダーの値に更新します。

### run(self)
- 機能：Tkinter の mainloop を呼び出し、GUIを実行します。

以下は、`GuiManager` クラスの詳細なPlantUMLクラス図です:

```plantuml
@startuml

!define main_style #FFD700
!define other_style #98FB98

class GuiManager << (O, other_style) >> {
  -shared_data: SharedData
  -scale: tk.Scale
  +__init__(shared_data: SharedData)
  +run(): None
  -_on_slider_change(value: float): None
}

GuiManager -- SharedData

@enduml
```

このクラス図では、`GuiManager` クラスが `SharedData` クラスと関連があり、主要なメソッドや属性がリストされています。これにより、プログラマはクラスを実装する際に必要な情報が得られます。

---

>draw_functions.pyの機能を表した詳細な仕様を説明してください。
仕様を読んだプログラマがpythonで実装できるように書いてください。
マークダウンでお願いします。
また、draw_functions.pyのクラス図をplantumlで詳細に書いて実装に役立てることができるようにしてください。
以下、ソースコードです。

---

以下は、`draw_functions.py` の機能を表した詳細な仕様です。

## draw_functions.py 仕様

### 概要
`draw_functions.py`モジュールでは、3D オブジェクトと 2D オブジェクトの描画関数が提供されています。これらの関数は、OpenGL および Pygame ライブラリを使用してグラフィックスを描画します。

### draw_3d_objects(object_position)
- 引数：
  - `object_position`: オブジェクトの位置タプル（x, y, z）
- 機能：与えられたオブジェクトの位置において、速度に基づいた色で球体を描画します。また、頂点と線を描画します。
  
### draw_2d_objects(screen)
- 引数：
  - `screen`: Pygame スクリーンオブジェクト
- 機能：Pygame を使用して、スクリーン上に静的な円と線を描画します。

以下は、`draw_functions.py` モジュールの詳細な PlantUML クラス図です:

```plantuml
@startuml

!define other_style #98FB98

class draw_functions << (O, other_style) >> {
  +draw_3d_objects(object_position: Tuple[float, float, float]): None
  +draw_2d_objects(screen: pygame.display): None
}

@enduml
```

このクラス図では、描画関数がどのような引数を受け取り、どのような機能を持っているかをリストしています。これにより、プログラマはモジュールを実装する際に必要な情報が得られます。

---

>windows_handlers.pyの機能を表した詳細な仕様を説明してください。
仕様を読んだプログラマがpythonで実装できるように書いてください。
マークダウンでお願いします。
また、windows_handlers.pyのクラス図をplantumlで詳細に書いて実装に役立てることができるようにしてください。
以下、ソースコードです。

---

以下は、`windows_handlers.py` の機能を表した詳細な仕様です。

## windows_handlers.py 仕様

### 概要
`windows_handlers.py` モジュールでは、キーボード入力の処理とウィンドウ表示に関連する関数が提供されています。また、OpenGLおよびPygameライブラリを使用してグラフィックスを描画します。

### keyboard_callback(key, x, y)
- 引数：
  - `key`: 押されたキーコード
  - `x`, `y`: キーイベント時のマウスポインタの座標
- 機能：特定のキー入力に応じて速度を増減させ、現在の速度をコンソールに出力します。

### set_camera_position(object_position, distance=10)
- 引数：
  - `object_position`: オブジェクトの位置タプル（x, y, z）
  - `distance`: カメラからオブジェクトまでの距離（デフォルトは10）
- 機能：カメラの位置と注視点を設定し、3Dシーンの表示を更新します。

### draw_graph(screen, data, color, origin, axis_scale)
- 引数：
  - `screen`: Pygame スクリーンオブジェクト
  - `data`: グラフに表示するデータのリスト
  - `color`: グラフの線の色
  - `origin`: グラフの原点座標（x, y）
  - `axis_scale`: x軸およびy軸の単位スケール
- 機能：Pygameを使用して、指定されたデータをグラフとして描画します。

### draw_pygame_window()
- 引数：なし
- 機能：Pygameウィンドウを作成し、2Dオブジェクトとグラフを描画します。ウィンドウが閉じられるか、Escキーが押されるまで実行を継続します。

以下は、`windows_handlers.py` モジュールの詳細な PlantUML クラス図です:

```plantuml
@startuml

!define other_style #98FB98

class windows_handlers << (O, other_style) >> {
  +keyboard_callback(key: int, x: int, y: int): None
  +set_camera_position(object_position: Tuple[float, float, float], distance: float = 10): None
  +draw_graph(screen: pygame.display, data: List[int], color: Tuple[int, int, int], origin: Tuple[int, int], axis_scale: Tuple[int, int]): None
  +draw_pygame_window(): None
}

@enduml
```

このクラス図では、各関数がどのような引数を受け取り、どのような機能を持っているかをリストしています。これにより、プログラマはモジュールを実装する際に必要な情報が得られます。

---

>GuiManagerWithPlotの機能を表した詳細な仕様を説明してください。
仕様を読んだプログラマがpythonで実装できるように書いてください。
マークダウンでお願いします。
また、GuiManagerWithPlotのクラス図をplantumlで詳細に書いて実装に役立てることができるようにしてください。
以下、ソースコードです。

---

## GuiManagerWithPlotクラス仕様

### 概要
`GuiManagerWithPlot`クラスは、`GuiManager`クラスを継承し、GUIに時系列の速度グラフを表示する機能を追加したクラスです。MatplotlibとTkinterが使用されています。

### 初期化関数 `__init__(self, shared_data)`
- 引数：
  - `shared_data`: SharedData オブジェクト
- 機能：親クラスの `__init__` を呼び出し、Matplotlibのfigureとsubplotを初期化し、キャンバスを作成してウィンドウに配置します。時系列の速度グラフをプロットします。

### plot_time_speed_graph(self)
- 機能：共有データから `time` と `speed` のデータを取得し、時系列の速度グラフをプロットして画面上に表示します。

### _on_slider_change(self, value)
- 引数：
  - `value`: スライダーから取得した新しい値
- 機能：親クラスの `_on_slider_change` メソッドを呼び出し、共有データオブジェクト内のキー "speed" の値をスライダーの値に更新します。その後、時系列の速度グラフを更新します。

以下は、`GuiManagerWithPlot` クラスの詳細なPlantUMLクラス図です:

```plantuml
@startuml

!define main_style #FFD700
!define other_style #98FB98

class GuiManager << (O, other_style) >> {
  -shared_data: SharedData
  -scale: tk.Scale
  +__init__(shared_data: SharedData)
  +run(): None
  -_on_slider_change(value: float): None
}

class GuiManagerWithPlot << (O, main_style) >> {
  -figure: plt.Figure 
  -plot: plt.Subplot
  -canvas: FigureCanvasTkAgg
  +__init__(shared_data: SharedData)
  +plot_time_speed_graph(): None
  -_on_slider_change(value: float): None
}

GuiManagerWithPlot --|> GuiManager
GuiManager -- SharedData

@enduml
```

このクラス図では、`GuiManagerWithPlot` クラスが `GuiManager` クラスを継承しており、主要なメソッドや属性がリストされています。これにより、プログラマはクラスを実装する際に必要な情報が得られます。

>GuiManagerWithPlotクラスですが、スライダコントロールの値は、shared_dataに格納されるので、_on_slider_changeをオーバーライドする必要はありません。
また、継承は構造がわかりにくくなるので、なるべく避けてください。

おっしゃる通り、`_on_slider_change` メソッドのオーバーライドは不要です。また、継承ではなくコンポジションを使用した以下のような設計に変更します。

### GuiManagerWithPlotクラス仕様 (修正版)

#### 概要
`GuiManagerWithPlot` クラスは、GUI に時系列の速度グラフを表示する機能を追加したクラスです。このクラスは、`GuiManager` を使っていますが、継承ではなくコンポジションを使用しています。Matplotlib と Tkinter が使用されています。

#### 初期化関数 `__init__(self, shared_data)`
- 引数：
  - `shared_data`: SharedData オブジェクト
- 機能：`GuiManager` クラスのインスタンスを作成し、初期化します。さらに、Matplotlib の figure と subplot を初期化し、キャンバスを作成してウィンドウに配置します。時系列の速度グラフをプロットします。

```python
class GuiManagerWithPlot:
    def __init__(self, shared_data):
        self.gui_manager = GuiManager(shared_data)
        self.gui_manager.root.title("Gui with Time-Speed Graph")
        
        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.plot = self.figure.add_subplot(1, 1, 1)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.gui_manager.root)
        
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # スライダーのコールバック関数を変更
        self.gui_manager.scale.config(command=self.plot_time_speed_graph)
        self.plot_time_speed_graph()
```

#### plot_time_speed_graph(self, *args)
- 機能：共有データから `time` と `speed` のデータを取得し、時系列の速度グラフをプロットして画面上に表示します。

```python
def plot_time_speed_graph(self, *args):
    time_data = self.gui_manager.shared_data["time"]
    speed_data = self.gui_manager.shared_data["speed"]

    self.plot.clear()
    self.plot.plot(time_data, speed_data, label="Speed vs Time")
    self.plot.set_title("Time-Speed Graph")
    self.plot.set_xlabel("Time")
    self.plot.set_ylabel("Speed")
    self.plot.legend()

    self.canvas.draw()
```

以下は、`GuiManagerWithPlot` クラスの修正されたクラス図です：

```plantuml
@startuml

!define main_style #FFD700
!define other_style #98FB98

class GuiManager << (O, other_style) >> {
  -shared_data: SharedData
  -scale: tk.Scale
  +__init__(shared_data: SharedData)
  +run(): None
}

class GuiManagerWithPlot << (O, main_style) >> {
  -gui_manager: GuiManager
  -figure: plt.Figure 
  -plot: plt.Subplot
  -canvas: FigureCanvasTkAgg
  +__init__(shared_data: SharedData)
  +plot_time_speed_graph(*args): None
}

GuiManagerWithPlot "1" *-- "1" GuiManager
GuiManager -- SharedData

@enduml
```

このクラス図で、`GuiManagerWithPlot` クラスは `GuiManager` クラスのインスタンスを持っており、主要なメソッドや属性がリストされています。これにより、プログラマはクラスを実装する際に必要な情報が得られます。


`GuiManager` の機能を拡張するのではなく、時系列の速度グラフを表示する機能が追加された独自の GUI を実装しているため、`TimeSpeedGraphGui` というクラス名に変更します。以下は修正した仕様です。

### TimeSpeedGraphGui クラス仕様 (修正版)

#### 概要
`TimeSpeedGraphGui` クラスは、GUI に時系列の速度グラフを表示する機能を実現したクラスです。このクラスは、`GuiManager` を使っていますが、継承ではなくコンポジションを使用しています。Matplotlib と Tkinter が使用されています。

#### 初期化関数 `__init__(self, shared_data)`
- 引数：
  - `shared_data`: SharedData オブジェクト
- 機能：`GuiManager` クラスのインスタンスを作成し、初期化します。さらに、Matplotlib の figure と subplot を初期化し、キャンバスを作成してウィンドウに配置します。時系列の速度グラフをプロットします。

```python
class TimeSpeedGraphGui:
    def __init__(self, shared_data):
        self.gui_manager = GuiManager(shared_data)
        self.gui_manager.root.title("Time-Speed Graph")
        
        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.plot = self.figure.add_subplot(1, 1, 1)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.gui_manager.root)
        
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # スライダーのコールバック関数を変更
        self.gui_manager.scale.config(command=self.plot_time_speed_graph)
        self.plot_time_speed_graph()
```

#### plot_time_speed_graph(self, *args)
- 機能：共有データから `time` と `speed` のデータを取得し、時系列の速度グラフをプロットして画面上に表示します。

```python
def plot_time_speed_graph(self, *args):
    time_data = self.gui_manager.shared_data["time"]
    speed_data = self.gui_manager.shared_data["speed"]

    self.plot.clear()
    self.plot.plot(time_data, speed_data, label="Speed vs Time")
    self.plot.set_title("Time-Speed Graph")
    self.plot.set_xlabel("Time")
    self.plot.set_ylabel("Speed")
    self.plot.legend()

    self.canvas.draw()
```

以下は、`TimeSpeedGraphGui` クラスの修正されたクラス図です：

```plantuml
@startuml

!define main_style #FFD700
!define other_style #98FB98

class GuiManager << (O, other_style) >> {
  -shared_data: SharedData
  -scale: tk.Scale
  +__init__(shared_data: SharedData)
  +run(): None
}

class TimeSpeedGraphGui << (O, main_style) >> {
  -gui_manager: GuiManager
  -figure: plt.Figure 
  -plot: plt.Subplot
  -canvas: FigureCanvasTkAgg
  +__init__(shared_data: SharedData)
  +plot_time_speed_graph(*args): None
}

TimeSpeedGraphGui "1" *-- "1" GuiManager
GuiManager -- SharedData

@enduml
```

このクラス図では、`TimeSpeedGraphGui` クラスが `GuiManager` クラスのインスタンスを持っており、主要なメソッドや属性がリストされています。これにより、プログラマはクラスを実装する際に必要な情報が得られます。

---

>クラス図を見て検討しましたが、GuiManagerが試作実装であまり機能が実装されていないため、無理に使用しなくてもソースコードをコピーし、GraphGuiクラスとして単独のクラスとして実装するべきだと考えます。
おそらく、GuiManagerクラスは使わなくなると思われますし、都度、コールバック関数をオーバーライドして書き換える必要がなくなります。
この仕様変更に合わせて仕様書やクラス図を変更してください。

---

`GraphGui` クラスとして単独のクラスを実装する仕様変更に合わせて、以下が修正された仕様です。

### GraphGui クラス仕様 (修正版)

#### 概要
`GraphGui` クラスは、時系列の速度グラフを表示する機能を実現したクラスです。このクラスでは、Matplotlib と Tkinter が使用されています。

#### 初期化関数 `__init__(self, shared_data)`
- 引数：
  - `shared_data`: SharedData オブジェクト
- 機能：ウィンドウのタイトルを設定し、初期化します。さらに、Matplotlib の figure と subplot を初期化し、キャンバスを作成してウィンドウに配置します。時系列の速度グラフをプロットします。

```python
class GraphGui:
    def __init__(self, shared_data):
        self.shared_data = shared_data
        self.root = tk.Tk()
        self.root.title("Time-Speed Graph")
        
        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.plot = self.figure.add_subplot(1, 1, 1)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # スライダーのコールバック関数を変更
        self.scale = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, command=self.plot_time_speed_graph)
        self.scale.pack(fill=tk.X, expand=True)

        self.plot_time_speed_graph()
```

#### plot_time_speed_graph(self, *args)
- 機能：共有データから `time` と `speed` のデータを取得し、時系列の速度グラフをプロットして画面上に表示します。

```python
def plot_time_speed_graph(self, *args):
    time_data = self.shared_data["time"]
    speed_data = self.shared_data["speed"]

    self.plot.clear()
    self.plot.plot(time_data, speed_data, label="Speed vs Time")
    self.plot.set_title("Time-Speed Graph")
    self.plot.set_xlabel("Time")
    self.plot.set_ylabel("Speed")
    self.plot.legend()

    self.canvas.draw()
```

#### run(self)
- 機能：Tkinter イベントループを開始します。

```python
def run(self):
    self.root.mainloop()
```

以下は、`GraphGui` クラスの修正されたクラス図です：

```plantuml
@startuml

!define main_style #FFD700

class GraphGui << (O, main_style) >> {
  -shared_data: SharedData
  -root: tk.Tk
  -figure: plt.Figure 
  -plot: plt.Subplot
  -canvas: FigureCanvasTkAgg
  -scale: tk.Scale
  +__init__(shared_data: SharedData)
  +plot_time_speed_graph(*args): None
  +run(): None
}

GraphGui -- SharedData

@enduml
```

このクラス図では、`GraphGui` クラスが `SharedData` クラスとの関連を持っており、主要なメソッドや属性がリストされています。これにより、プログラマはクラスを実装する際に必要な情報が得られます。

---
---
# 再設計
---
SharedDataクラスの機能を表した詳細な仕様を説明してください。
仕様を読んだプログラマがpythonで実装できるように書いてください。
マークダウンでお願いします。

関数一覧は、以下のように整えてください。

#### 初期化関数 `__init__(self, )`
- 引数：
- 機能：

また、クラス図をplantumlで詳細に書いて実装に役立てることができるようにしてください。
以下、ソースコードです。

---

### SharedDataクラスの仕様

`SharedData` クラスは、複数のスレッド間で共有されるデータを格納し、アクセスするためのクラスです。このクラスには、以下の機能があります。

#### 初期化関数 `__init__(self, queue_depth: int = 10)`
- 引数：
  - `queue_depth`: それぞれのキーに対するデータの最大保存個数を指定します。デフォルトは10です。
- 機能：`queue_depth` を指定してインスタンスを初期化します。

#### データ設定関数 `set_data(self, key: str, timestamp_ms: int, value: Any) -> None`
- 引数：
  - `key`: データにアクセスするためのキーです。
  - `timestamp_ms`: 設定されるデータのタイムスタンプ（ミリ秒）を指定します。
  - `value`: 設定する任意のデータです。
- 機能：データを設定します。

#### データ取得関数 `get_data(self, key: str) -> List[Tuple[int, Any]]`
- 引数：
  - `key`: 取得したいデータのキーを指定します。
- 機能：指定したキーに関連付けられたデータのリストを取得します。
- 戻り値：リストの各要素は `(timestamp_ms, value)` の形式のタプルです。

### SharedDataクラス図 (PlantUML)

```puml
@startuml
class SharedData {
    + __init__(queue_depth: int = 10)
    + set_data(key: str, timestamp_ms: int, value: Any): None
    + get_data(key: str) -> List[Tuple[int, Any]]
    - data: Dict[str, Deque[Tuple[int, Any]]]
    - queue_depth: int
    - lock: threading.Lock
}
@enduml
```

このクラス図は、`SharedData` クラスの構造を示しています。`__init__()`, `set_data()` および `get_data()` といったメソッドが公開されており、内部には `data`, `queue_depth`, `lock` を保持しています。

上記仕様とクラス図を参照して、プログラマはPythonで実装することができます。

3D表示する
source\leg_simulation\main.py

2D表示する
source\Linkages.py

