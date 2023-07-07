# shared_data.py

import threading
from collections import deque
from typing import Any, Deque, Dict, List, Tuple

from construct import Struct, Array, Int32ul, Int32sl

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

class SharedData:
    def __init__(self, queue_depth: int = 100):
        self.data: Dict[str, Deque[Tuple[int, Any]]] = {}
        self.queue_depth: int = queue_depth
        self.lock: threading.Lock = threading.Lock()

    def set_data(self, key: str, timestamp_ms: int, value: Any) -> None:
        with self.lock:
            if key not in self.data:
                self.data[key] = deque(maxlen=self.queue_depth)
            self.data[key].append((timestamp_ms, value))

    def get_data(self, key: str) -> List[Tuple[int, Any]]:
        with self.lock:
            return list(self.data.get(key, []))


