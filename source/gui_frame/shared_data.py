import threading

class SharedData:
    def __init__(self):
        self.values = {}
        self.locks = {}

    def set_value(self, key, value):
        if key not in self.locks:
            self.locks[key] = threading.Lock()

        with self.locks[key]:
            self.values[key] = value
    
    def get_value(self, key):
        lock = self.locks.get(key)
        value = self.values.get(key, None)

        # 以前の値を使用 (ロックがかかっている場合は更新を待たずに取得)
        if lock is not None and not lock.locked():
            with lock:
                value = self.values.get(key, None)

        return value
    
