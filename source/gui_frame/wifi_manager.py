import socket
from .shared_data import SharedData, ServoCmd, ServoFb, ServoCmdStruct, ServoFbStruct

HOST = '192.168.1.100'
PORT = 80

class WifiManager:
    def __init__(self, shared_data):
        super().__init__()
        self.shared_data = shared_data

    def run(self):

        # サーボコマンドオブジェクトの作成
        servo_cmd = ServoCmd()

        # Constructを使いサーボコマンドオブジェクトをバイト列に変換
        cmd_data = ServoCmdStruct.build({"a_angle": servo_cmd.a_angle})

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))

        while True:

            try:
                # コマンドを送信
                s.sendall(cmd_data)

                # 応答を受信
                response_size = 56 # Arduinoから7つのunsigned intを2セット受け取るので、4*7*2=56バイトを読み込む
                data = s.recv(response_size)

                # 受信したデータをパース
                parsed_data = ServoFbStruct.parse(data)

                # パースしたデータをServoFbオブジェクトに変換
                servo_fb = ServoFb(**parsed_data)

                print(servo_fb.a_angle) # 受信した角度データを表示
                print(servo_fb.a_vol)   # 受信した電圧データを表示

            except KeyboardInterrupt:
                print("Terminating...")
                break

            except Exception as e:
                print(f"An error occurred: {e}")
                break

        s.close()
