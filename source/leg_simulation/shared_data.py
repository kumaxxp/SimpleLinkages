# shared_data.py

import threading
from collections import deque
from typing import Any, Deque, Dict, List, Tuple

#from construct import Struct, Array, Int32ul, Int32sl

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class ServoCmd:
    def __init__(self):
        self.command:int = 0
        self.a_angle:List[int] = [0] * 7

class ServoFb:
    def __init__(self, **kwargs):   # Add **kwargs to accept any number of keyword arguments
        self.a_angle:List[int] = kwargs.get('a_angle', [0] * 7)
        self.a_vol:List[int] = kwargs.get('a_vol', [0] * 7)        

class SharedData(metaclass=Singleton):
    def __init__(self, queue_depth: int = 100):
        self.data: Dict[str, Deque[Tuple[int, Any]]] = {}
        self.queue_depth: int = queue_depth
        self.lock: threading.Lock = threading.Lock()

        self._servo_cmd_lock: threading.Lock = threading.Lock()
        self._servo_fb_lock: threading.Lock = threading.Lock()        

        # 全て0で初期化
        self._servo_cmd = ServoCmd()
        self._servo_fb  = ServoFb()

    def set_data(self, key: str, timestamp_ms: int, value: Any) -> None:
        with self.lock:
            if key not in self.data:
                self.data[key] = deque(maxlen=self.queue_depth)
            self.data[key].append((timestamp_ms, value))

    def get_data(self, key: str) -> List[Tuple[int, Any]]:
        with self.lock:
            return list(self.data.get(key, []))

    @property
    def servo_cmd(self) -> ServoCmd:
        with self._servo_cmd_lock:
            return self._servo_cmd

    @servo_cmd.setter
    def servo_cmd(self, value: ServoCmd) -> None:
        with self._servo_cmd_lock:
            self._servo_cmd = value

    @property
    def servo_fb(self) -> ServoFb:
        with self._servo_fb_lock:
            return self._servo_fb

    @servo_fb.setter
    def servo_fb(self, value: ServoFb) -> None:
        with self._servo_fb_lock:
            self._servo_fb = value
