import socket
from typing import Any
from leg_simulation.shared_data import SharedData, ServoCmd, ServoFb
from construct import Struct, Array, Int32ul, Int32sl

HOST: str = '192.168.1.100'
PORT: int = 80

ServoCmdStruct = Struct(
    "a_angle" / Array(7, Int32ul)
)

ServoFbStruct = Struct(
    "a_angle" / Array(7, Int32sl),
    "a_vol" / Array(7, Int32ul)
)

class WifiManager:
    def __init__(self, shared_data: SharedData) -> None:
        super().__init__()
        self.shared_data: SharedData = shared_data

        # 全て0で初期化
        self.cmd_data = ServoCmdStruct.build({"a_angle": [0]*7})
        self.fb_data  = ServoFbStruct.build({
            "a_angle": [0]*7,
            "a_vol": [0]*7
        })

    def run(self) -> None:

        # サーボコマンドオブジェクトの作成
        servo_cmd: ServoCmd = ServoCmd()

        # Constructを使いサーボコマンドオブジェクトをバイト列に変換
        cmd_data: bytes = ServoCmdStruct.build({"a_angle": servo_cmd.a_angle})

        s: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))

        print("start wifi")

        while True:

            try:
                # コマンドを送信
                s.sendall(cmd_data)

                # 応答を受信
                response_size: int = 56 # Arduinoから7つのunsigned intを2セット受け取るので、4*7*2=56バイトを読み込む
                data: bytes = s.recv(response_size)

                # 受信したデータをパース
                parsed_data: Any = ServoFbStruct.parse(data)

                # パースしたデータをServoFbオブジェクトに変換
                servo_fb: ServoFb = ServoFb(**parsed_data)

                #print(servo_fb.a_angle) # 受信した角度データを表示
                #print(servo_fb.a_vol)   # 受信した電圧データを表示

                self.shared_data.servo_fb = servo_fb # 共有メモリに保存

            except KeyboardInterrupt:
                print("Terminating...")
                break

            except Exception as e:
                print(f"An error occurred: {e}")
                break

        s.close()
