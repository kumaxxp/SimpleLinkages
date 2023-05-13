import serial
import time

LOBOT_SERVO_FRAME_HEADER = 0x55
LOBOT_SERVO_VIN_READ = 0x1E

# シリアルポートの設定
port = "COM3"  # Windows の場合
# port = "/dev/ttyS0"  # Linux / macOS の場合
baudrate = 115200
timeout = 1

def lobot_check_sum(buf):
    if len(buf) < 6:
        raise ValueError("Input bytearray should have at least 6 elements")

    temp = sum(buf[:5])
    temp = ~temp
    i = temp & 0xFF
    return i

def byte_to_hw(low, high):
    return (high << 8) + low


def lobot_serial_servo_read_vin(serial_x, id):
    count = 10000

    buf = bytearray(6)
    buf[0] = buf[1] = LOBOT_SERVO_FRAME_HEADER
    buf[2] = id
    buf[3] = 5
    buf[4] = LOBOT_SERVO_VIN_READ
    buf[5] = lobot_check_sum(buf)

    time.sleep(0.1)

    received_data = ser.read(6)
    print(received_data)
    print(len(received_data))
    if len(received_data) > 0 :
        ret = byte_to_hw(buf[4], buf[3])
    else:
        ret = -2048

    return ret


def send_command(servo_id, command, param1=None, param2=None):
    data = bytearray([0x55, 0x55, servo_id])
    data.append(command)
    
    if param1 is not None:
        data.append(param1)
    if param2 is not None:
        data.append(param2)

    sum = lobot_check_sum(data)
    data.append(sum)

    ser.write(data)
    time.sleep(0.01)

def read_response():
    response = ser.read(6) # レスポンスデータ長さ: 4バイト
    if len(response) == 4:
        return response[2] | (response[3] << 8)
    else:
        return None


# シリアルポートのオープン
ser = serial.Serial(port, baudrate, timeout=timeout)

# IDリストを定義（複数サーボモーターがある場合）
servo_id = 6

# 電圧取得コマンド（コマンド値 7）を送信
vin = lobot_serial_servo_read_vin(ser, servo_id)
print(vin)

# 電圧レスポンスを読み取り表示
if vin is not None:
    print(f"Servo ID {servo_id}: Voltage = {vin/100} V")
else:
    print(f"Servo ID {servo_id}: Error reading voltage")

# 現在位置取得コマンド（コマンド値 8）を送信
#    send_command(servo_id, 8)
#
#    # 現在位置レスポンスを読み取り表示
#    position = read_response()
#    if position is not None:
#        print(f"Servo ID {servo_id}: Current Position = {position}")
#    else:
#        print(f"Servo ID {servo_id}: Error reading position")

time.sleep(1)

ser.close()

