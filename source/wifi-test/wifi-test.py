import socket
from construct import Struct, Array, Int32ub
import threading
import time

class ServoCmd:
    def __init__(self):
        self.a_angle = [0]*7

class ServoFb:
    def __init__(self, a_angle: list, a_vol: list, **kwargs):
        self.a_angle = a_angle
        self.a_vol = a_vol

ServoCmdStruct = Struct(
    "a_angle" / Array(7, Int32ub)
)

ServoFbStruct = Struct(
    "a_angle" / Array(7, Int32ub),
    "a_vol" / Array(7, Int32ub)
)

HOST = '192.168.1.100'
PORT = 80

def send_data(s):
    while True:
        servo_cmd = ServoCmd()
        cmd_data = ServoCmdStruct.build({"a_angle": servo_cmd.a_angle})
        s.sendall(cmd_data)
        time.sleep(1)
        print("send")


def recv_data(s):
    response_size = 56
    while True:
        data = s.recv(response_size)
        parsed_data = ServoFbStruct.parse(data)
        servo_fb = ServoFb(**parsed_data)
        print(servo_fb.a_angle)
        print(servo_fb.a_vol)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    time.sleep(1)

    send_thread = threading.Thread(target=send_data, args=(s,))
    recv_thread = threading.Thread(target=recv_data, args=(s,))

    send_thread.start()
    recv_thread.start()

    send_thread.join()
    recv_thread.join()
