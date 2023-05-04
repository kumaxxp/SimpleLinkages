# shared_data.py

import threading
from collections import deque
from typing import Any, Deque, Dict, List, Tuple

class SharedData:
    def __init__(self, queue_depth: int = 10):
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


