import time
import serial
from functools import reduce

# Constants
LOBOT_SERVO_FRAME_HEADER = 0x55
LOBOT_SERVO_POS_READ = 0x1C
LOBOT_SERVO_MOVE_TIME_WRITE = 0x01
LOBOT_SERVO_VIN_READ = 0x1B
LOBOT_SERVO_MOVE_STOP = 0x0C
LOBOT_SERVO_ID_WRITE = 0x0D
LOBOT_SERVO_OR_MOTOR_MODE_WRITE = 0x1D
LOBOT_SERVO_LOAD_OR_UNLOAD_WRITE = 0x1F

ID1 = 1
ID2 = 2
KEY1 = 2
KEY2 = 3


def get_low_byte(x):
    return x & 0xFF


def get_high_byte(x):
    return (x >> 8) & 0xFF


def byte_to_hw(a, b):
    return ((a << 8) | b)


def lobot_checksum(buf):
    # Add all bytes and take the one's complement of the sum
    temp = reduce(
        lambda acc, x: acc + x,
        buf[2:buf[3] + 2],
        0,
    )
    temp = ~temp
    return temp & 0xFF

# ...

def lobot_serial_servo_move(serial_x, servo_id, position, move_time):
    if position < 0:
        position = 0
    if position > 1000:
        position = 1000

    buf = bytearray(10)
    buf[0] = buf[1] = LOBOT_SERVO_FRAME_HEADER
    buf[2] = servo_id
    buf[3] = 7
    buf[4] = LOBOT_SERVO_MOVE_TIME_WRITE
    buf[5] = get_low_byte(position)
    buf[6] = get_high_byte(position)
    buf[7] = get_low_byte(move_time)
    buf[8] = get_high_byte(move_time)
    buf[9] = lobot_checksum(buf)

    # Write the command to the serial port
    serial_x.write(bytes(buf))

def lobot_serial_servo_stop_move(serial_x, servo_id):
    buf = bytearray(6)
    buf[0] = buf[1] = LOBOT_SERVO_FRAME_HEADER
    buf[2] = servo_id
    buf[3] = 3
    buf[4] = LOBOT_SERVO_MOVE_STOP
    buf[5] = lobot_checksum(buf)

    serial_x.write(bytes(buf))

def lobot_serial_servo_set_id(serial_x, old_id, new_id):
    buf = bytearray(7)
    buf[0] = buf[1] = LOBOT_SERVO_FRAME_HEADER
    buf[2] = old_id
    buf[3] = 4
    buf[4] = LOBOT_SERVO_ID_WRITE
    buf[5] = new_id
    buf[6] = lobot_checksum(buf)

    serial_x.write(bytes(buf))

def lobot_serial_servo_set_mode(serial_x, servo_id, mode, speed):
    buf = bytearray(10)
    buf[0] = buf[1] = LOBOT_SERVO_FRAME_HEADER
    buf[2] = servo_id
    buf[3] = 7
    buf[4] = LOBOT_SERVO_OR_MOTOR_MODE_WRITE
    buf[5] = mode
    buf[6] = 0
    buf[7] = get_low_byte(speed)
    buf[8] = get_high_byte(speed)
    buf[9] = lobot_checksum(buf)

    serial_x.write(bytes(buf))

def lobot_serial_servo_load(serial_x, servo_id):
    buf = bytearray(7)
    buf[0] = buf[1] = LOBOT_SERVO_FRAME_HEADER
    buf[2] = servo_id
    buf[3] = 4
    buf[4] = LOBOT_SERVO_LOAD_OR_UNLOAD_WRITE
    buf[5] = 1
    buf[6] = lobot_checksum(buf)

    serial_x.write(bytes(buf))

def lobot_serial_servo_unload(serial_x, servo_id):
    buf = bytearray(7)
    buf[0] = buf[1] = LOBOT_SERVO_FRAME_HEADER
    buf[2] = servo_id
    buf[3] = 4
    buf[4] = LOBOT_SERVO_LOAD_OR_UNLOAD_WRITE
    buf[5] = 0
    buf[6] = lobot_checksum(buf)

    serial_x.write(bytes(buf))

def lobot_serial_servo_receive_handle(serial_x, buf):
    length = serial_x.read(2)
    if length and len(length) == 2:
        length = int.from_bytes(length, byteorder='big')
        data = bytearray(serial_x.read(length - 1))
        data.insert(0, length[0])
        data.insert(1, length[1])
        data.append(serial_x.read(1)[0])
        if (
            data[0] == LOBOT_SERVO_FRAME_HEADER
            and data[1] == LOBOT_SERVO_FRAME_HEADER
            and lobot_checksum(data) == data[-1]
        ):
            return data[2:-1]
    return None

def lobot_serial_servo_read_position(serial_x, servo_id):
    count = 10000
    ret = None

    buf = bytearray(6)
    buf[0] = buf[1] = LOBOT_SERVO_FRAME_HEADER
    buf[2] = servo_id
    buf[3] = 3
    buf[4] = LOBOT_SERVO_POS_READ
    buf[5] = lobot_checksum(buf)

    while serial_x.in_waiting:
        serial_x.read()

    serial_x.write(bytes(buf))

    while not serial_x.in_waiting:
        count -= 1
        if count < 0:
            return -1

    response = lobot_serial_servo_receive_handle(serial_x, buf)
    if response is not None:
        ret = byte_to_hw(response[2], response[1])
    else:
        ret = -1

    return ret

def lobot_serial_servo_read_vin(serial_x, servo_id):
    count = 10000
    ret = None

    buf = bytearray(6)
#    buf[0] = buf[1] = LOBOT_SERVO_FRAME_HEADER
#    buf[2] = servo_id
#    buf[3] = 5
#    buf[4] = LOBOT_SERVO_VIN_READ
#    buf[5] = lobot_checksum(buf)

    buf[0] = buf[1] = LOBOT_SERVO_FRAME_HEADER
    buf[2] = 2
    buf[3] = 15

    time.sleep(0.01)
    
    while serial_x.in_waiting:
        serial_x.read()

    serial_x.write(bytes(buf))
        

    response = lobot_serial_servo_receive_handle(serial_x, buf)
    if response is not None:
        ret = int.from_bytes(response[1:3], byteorder='big', signed=True)
    else:
        ret = -2048

    return ret

# ... (Include remaining functions)

serial_port = serial.Serial("COM_PORT", 115200, timeout=1)  # Replace COM_PORT with your actual port

id1_pos_list = [100, 200, 300, 400]
id2_pos_list = [100, 200, 300, 400]

mode = 0
step = 0
run = False

while True:
    if mode == 0:
        if run:
            lobot_serial_servo_move(serial_port, ID1, id1_pos_list[step], 500)
            lobot_serial_servo_move(serial_port, ID2, id2_pos_list[step], 500)
            step += 1
            if step == 4:
                step = 0
                run = False
            time.sleep(1)
        
        key2_pressed = False   # Implement checking for KEY2 using GPIO pin
        if key2_pressed:
            time.sleep(0.01)
            key2_pressed = False   # Check again to debounce
            if not key2_pressed:
                run = True
                step = 0
                time.sleep(0.5)

        key1_pressed = False   # Implement checking for KEY1 using GPIO pin
        if key1_pressed:
            time.sleep(0.01)
            key1_pressed = False   # Check again to debounce
            if not key1_pressed:
                # Unload servos here
                mode = 1
                step = 0
                time.sleep(0.5)

    if mode == 1:
        key2_pressed = False
        if key2_pressed:
            time.sleep(0.01)
            key2_pressed = False
            if not key2_pressed:
                id1_pos_list[step] = lobot_serial_servo_read_position(serial_port, ID1)
                id2_pos_list[step] = lobot_serial_servo_read_position(serial_port, ID2)
                step += 1
                if step == 4:
                    step = 0
                time.sleep(0.5)

        key1_pressed = False
        if key1_pressed:
            time.sleep(0.01)
            key1_pressed = False
            if not key1_pressed:
                # Move servos to current position here
                mode = 0
                time.sleep(0.5)
