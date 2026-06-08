import unittest
from src.task_manager.queue import UniqueQueue

class TestUniqueQueue(unittest.TestCase):
    def test_lifo_push_unique_elements(self):
        queue = UniqueQueue(lifo=True)

        self.assertTrue(queue.push(1))
        self.assertTrue(queue.push(2))
        self.assertTrue(queue.push(3))

        self.assertEqual(queue.size, 3)
        self.assertEqual(queue.to_list(), [1, 2, 3])

    def test_lifo_push_duplicate_elements(self):
        queue = UniqueQueue(lifo=True)
        queue.push(1)
        queue.push(2)
        queue.push(3)
        self.assertFalse(queue.push(1))
        self.assertFalse(queue.push(2))
        self.assertFalse(queue.push(3))
        self.assertEqual(queue.size, 3)
        self.assertEqual(queue.to_list(), [1, 2, 3])

    def test_lifo_pop_order(self):
        queue = UniqueQueue(lifo=True)
        queue.push(10)
        queue.push(20)
        queue.push(30)
        self.assertEqual(queue.pop(), 30)
        self.assertEqual(queue.pop(), 20)
        self.assertEqual(queue.pop(), 10)
        self.assertEqual(queue.size, 0)

    def test_lifo_peek_method(self):
        queue = UniqueQueue(lifo=True)
        queue.push('a')
        queue.push('b')
        queue.push('c')
        self.assertEqual(queue.peek(), 'c')
        self.assertEqual(queue.size, 3)
        queue.pop()
        self.assertEqual(queue.peek(), 'b')
        self.assertEqual(queue.size, 2)

    def test_size_property(self):
        queue = UniqueQueue(lifo=False)
        self.assertEqual(queue.size, 0)
        self.assertEqual(len(queue), 0)
        queue.push(100)
        queue.push(200)
        queue.push(300)
        self.assertEqual(queue.size, 3)
        self.assertEqual(len(queue), 3)
        queue.pop()
        self.assertEqual(queue.size, 2)

    def test_last_property(self):
        queue = UniqueQueue(lifo=False)
        queue.push('first')
        self.assertEqual(queue.last, 'first')
        queue.push('second')
        self.assertEqual(queue.last, 'second')
        queue.push('third')
        self.assertEqual(queue.last, 'third')
        queue.pop()
        self.assertEqual(queue.last, 'third')

    def test_last_property_empty_queue(self):
        queue = UniqueQueue(lifo=False)
        with self.assertRaises(IndexError) as context:
            _ = queue.last
        self.assertIn("empty", str(context.exception).lower())

    def test_last_after_multiple_operations(self):
        queue = UniqueQueue(lifo=True)
        queue.push(42)
        self.assertEqual(queue.last, 42)
        queue.push("hello")
        self.assertEqual(queue.last, "hello")
        queue.push((1, 2, 3))
        self.assertEqual(queue.last, (1, 2, 3))
        queue.pop()
        self.assertEqual(queue.last, "hello")
        queue.push(True)
        self.assertEqual(queue.last, True)

    def test_first_property_fifo(self):
        queue = UniqueQueue(lifo=False)
        queue.push(1)
        queue.push(2)
        queue.push(3)
        self.assertEqual(queue.first, 1)

        queue.pop()
        self.assertEqual(queue.first, 2)

        queue.pop()
        self.assertEqual(queue.first, 3)

    def test_clear_method(self):
        queue = UniqueQueue(lifo=False)
        queue.push(1)
        queue.push(2)
        queue.push(3)
        self.assertEqual(queue.size, 3)
        queue.clear()
        self.assertEqual(queue.size, 0)
        self.assertEqual(queue.to_list(), [])
        self.assertNotIn(1, queue)
        queue.push(100)
        self.assertEqual(queue.size, 1)
        self.assertEqual(queue.last, 100)


if __name__ == '__main__':
    unittest.main(verbosity=2)