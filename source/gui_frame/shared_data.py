# shared_data.py

import threading
from collections import deque
from typing import Any, Deque, Dict, List, Tuple

from construct import Struct, Array, Int32ul, Int32sl

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class ServoCmd:
    def __init__(self):
        self.a_angle = [0]*7

class ServoFb:
    def __init__(self, a_angle: list, a_vol: list, **kwargs):
        self.a_angle = a_angle
        self.a_vol = a_vol

ServoCmdStruct = Struct(
    "a_angle" / Array(7, Int32ul)
)

ServoFbStruct = Struct(
    "a_angle" / Array(7, Int32sl),
    "a_vol" / Array(7, Int32ul)
)

class SharedData(metaclass=Singleton):
    def __init__(self, queue_depth: int = 100):
        self.data: Dict[str, Deque[Tuple[int, Any]]] = {}
        self.queue_depth: int = queue_depth
        self.lock: threading.Lock = threading.Lock()

        self._servo_cmd_lock: threading.Lock = threading.Lock()
        self._servo_fb_lock: threading.Lock = threading.Lock()        

        # 全て0で初期化
        self.servo_cmd = ServoCmdStruct.build({"a_angle": [0]*7})
        self.servo_fb  = ServoFbStruct.build({
            "a_angle": [0]*7,
            "a_vol": [0]*7
        })

    def set_data(self, key: str, timestamp_ms: int, value: Any) -> None:
        with self.lock:
            if key not in self.data:
                self.data[key] = deque(maxlen=self.queue_depth)
            self.data[key].append((timestamp_ms, value))

    def get_data(self, key: str) -> List[Tuple[int, Any]]:
        with self.lock:
            return list(self.data.get(key, []))

    @property
    def servo_cmd(self):
        with self._servo_cmd_lock:
            return self._servo_cmd

    @servo_cmd.setter
    def servo_cmd(self, value):
        with self._servo_cmd_lock:
            self._servo_cmd = value

    @property
    def servo_fb(self):
        with self._servo_fb_lock:
            return self._servo_fb

    @servo_fb.setter
    def servo_fb(self, value):
        with self._servo_fb_lock:
            self._servo_fb = value
            
