import socket
import time
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

    parsed_data: Any = ServoFbStruct.parse(data)
    servo_fb: ServoFb = ServoFb(**parsed_data)
#    print(servo_fb.a_angle)
#    print(servo_fb.a_vol)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # タイムアウト時間の設定
    s.settimeout(1.0) 
    s.connect((HOST, PORT))

    while True:
        
        time.sleep(0.05)    # 50ms間隔に設定。もう少し短くてもいいかも。

        try:
            # コマンドを送信
            cmd_data = ServoCmdStruct.build({"command":0, "a_angle": [1]*7})
            s.sendall(cmd_data)

        except Exception as e:
            print("send")
            print(f"An error occurred: {e}")
            break

        try:
            # 応答を受信
            recv_data(s)

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
