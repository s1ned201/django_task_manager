import random
import unittest

from src.task_manager.queue import Queue, EmptyQueueError


class TestQueue(unittest.TestCase):
    def test_queue_exists(self):
        queue = Queue()

    def test_queue_exists_strategy(self):
        queue = Queue('FIFO')

    def test_no_exists_strategy(self):
        with self.assertRaises(TypeError):
            queue = Queue('FIFA')

    def test_add_item_to_queue(self):
        queue = Queue('FIFO')
        queue.add(5)
        item = queue.storage[0]
        self.assertEqual(5, item)

    # def test_add_and_get_item_from_queue(self):
    #     queue = Queue('FIFO')
    #     queue.add(5)
    #     item = queue.remove()
    #     self.assertEqual(5, item)

    def test_get_item_from_empty_queue(self):
        queue = Queue('FIFO')
        with self.assertRaises(EmptyQueueError):
            queue.remove()

    # def test_add_and_get_multi_value_from_queue(self):
    #     queue = Queue('FIFO')
    #     queue.add(5)
    #     queue.add(4)
    #     queue.add(3)
    #     item = queue.remove()
    #     self.assertEqual(5, item)
    #     item = queue.remove()
    #     self.assertEqual(4, item)
    #     item = queue.remove()
    #     self.assertEqual(3, item)

    def test_add_many_random_items(self):
        queue = Queue('FIFO')
        queue.add(5)
        for _ in range(10):
            queue.add(random.randint(10, 20))

if __name__ == '__main__':
    unittest.main()