import sys
sys.path.append("../")

import threading
import time
import unittest
from shared_data import SharedData

def write_data(shared_data: SharedData, key: str, start_timestamp: int) -> None:
    for i in range(3):
        shared_data.set_data(key, start_timestamp + i * 1000, f"value{i}")
        time.sleep(0.1)

class TestSharedDataThreads(unittest.TestCase):
    def test_set_and_get_data_with_threads(self):
        shared_data = SharedData(queue_depth=3)
        writer_thread1 = threading.Thread(target=write_data, args=(shared_data, "example_key1", 1000))
        writer_thread2 = threading.Thread(target=write_data, args=(shared_data, "example_key2", 3000))

        # スレッドの開始
        writer_thread1.start()
        writer_thread2.start()

        # スレッドが終了するまで待機
        writer_thread1.join()
        writer_thread2.join()

        # データを取得して検証
        self.assertEqual(shared_data.get_data("example_key1"), [(1000, "value0"), (2000, "value1"), (3000, "value2")])
        self.assertEqual(shared_data.get_data("example_key2"), [(3000, "value0"), (4000, "value1"), (5000, "value2")])

class TestSharedData(unittest.TestCase):
    def test_set_and_get_data(self):
        shared_data = SharedData(queue_depth=3)

        # データを設定
        shared_data.set_data("example_key1", 1000, "value1")
        shared_data.set_data("example_key1", 2000, "value2")
        shared_data.set_data("example_key2", 3000, "value3")

        # データを取得して検証
        self.assertEqual(shared_data.get_data("example_key1"), [(1000, "value1"), (2000, "value2")])
        self.assertEqual(shared_data.get_data("example_key2"), [(3000, "value3")])

        # キューが最大長さに達した場合のテスト
        shared_data.set_data("example_key1", 4000, "value4")
        shared_data.set_data("example_key1", 5000, "value5")
        self.assertEqual(shared_data.get_data("example_key1"), [(2000, "value2"), (4000, "value4"), (5000, "value5")])

        # 存在しないキーのデータ取得テスト
        self.assertEqual(shared_data.get_data("unknown_key"), [])

if __name__ == '__main__':
    unittest.main()
