import socket
from construct import Struct, Array, Int32ub, Int32ul, Int32sl

class ServoCmd:
    def __init__(self):
        self.a_angle = [0]*7

class ServoFb:
    def __init__(self, a_angle: list, a_vol: list, **kwargs):
        self.a_angle = a_angle
        self.a_vol = a_vol

ServoCmdStruct = Struct(
    "command" / Int32ul,
    "a_angle" / Array(7, Int32ul)
)

ServoFbStruct = Struct(
    "a_angle" / Array(7, Int32sl),
    "a_vol" / Array(7, Int32ul)
)

HOST = '192.168.1.100'
PORT = 80

def send_data(s):
    while True:
        servo_cmd = ServoCmd()
        cmd_data = ServoCmdStruct.build({"a_angle": [0]*7})
        s.sendall(cmd_data)
        time.sleep(1)
        print("send")


def recv_data(s):
    response_size = 56
    data = b""
    
    while len(data) < response_size:
        chunk = s.recv(response_size - len(data))
        
        if not chunk:
            raise Exception("Socket connection broken")
            
        data += chunk

    parsed_data = ServoFbStruct.parse(data)
    servo_fb = ServoFb(**parsed_data)
    print(servo_fb.a_angle)
    print(servo_fb.a_vol)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # タイムアウト時間の設定
    s.settimeout(10.0) 
    s.connect((HOST, PORT))

    while True:

        try:
            # コマンドを送信
            cmd_data = ServoCmdStruct.build({"command":0, "a_angle": [0]*7})
            print(cmd_data)
            s.sendall(cmd_data)

        except Exception as e:
            print("send")
            print(f"An error occurred: {e}")
            break

        try:
            # 応答を受信
            response_size = 56 # Arduinoから7つのunsigned intを2セット受け取るので、4*7*2=56バイトを読み込む
            data = s.recv(response_size)

            print("2")

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
            print("rev")
            print(f"An error occurred: {e}")
            break
except socket.error as e:
    print(f"Could not connect to server: {e}")

finally:
    s.close()
