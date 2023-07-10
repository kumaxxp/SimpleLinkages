import socket
import time
from typing import Any
from leg_simulation.shared_data import SharedData, ServoCmd, ServoFb
from construct import Struct, Array, Int32ul, Int32sl

HOST: str = '192.168.1.100'
PORT: int = 80

ServoCmdStruct = Struct(
    "command" / Int32ul,
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
#        self.cmd_data = ServoCmdStruct.build({"a_angle": [0]*7})
        self.fb_data  = ServoFbStruct.build({
            "a_angle": [0]*7,
            "a_vol": [0]*7
        })

    def recv_data(self, s) -> ServoFb: 
        response_size = 56
        data = b""
        
        while len(data) < response_size:
            chunk = s.recv(response_size - len(data))
            
            if not chunk:
                raise Exception("Socket connection broken")
                
            data += chunk

        parsed_data: Any = ServoFbStruct.parse(data)
        servo_fb: ServoFb = ServoFb(**parsed_data)
    #    print(servo_fb.a_angle)
    #    print(servo_fb.a_vol)

        return servo_fb

    def run(self) -> None:

        # サーボコマンドオブジェクトの作成
        servo_cmd: ServoCmd = ServoCmd()

        # Constructを使いサーボコマンドオブジェクトをバイト列に変換
        cmd_data: bytes = ServoCmdStruct.build({"command": servo_cmd.command, "a_angle": servo_cmd.a_angle})

        s: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # タイムアウト時間の設定
            s.settimeout(1.0) 
            s.connect((HOST, PORT))

            print("start wifi")

            while True:

                time.sleep(0.01)    # 50ms間隔に設定。もう少し短くてもいいかも。

                try:
                    # コマンドを送信
                    s.sendall(cmd_data)
                                
                except Exception as e:
                    print("send")
                    print(f"An error occurred: {e}")
                    break

                try:
                    # 応答を受信し、 共有メモリに保存
                    self.shared_data.servo_fb = self.recv_data(s)                    

                except KeyboardInterrupt:
                    print("Terminating...")
                    break

                except Exception as e:
                    print("rev")
                    print(f"An error occurred: {e}")
                    break
                
        except socket.error as e:
            print(f"Could not connect to server: {e}")

        finally:
            s.close()
