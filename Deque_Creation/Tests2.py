#!/usr/bin/python3

import unittest

from Deque import Deque


class DequeTests(unittest.TestCase):

    def test_is_empty(self):
        deque = Deque()
        self.assertTrue(deque.is_empty())
        deque.push_back(0)
        self.assertFalse(deque.is_empty())
        deque.pop_front()
        self.assertTrue(deque.is_empty())
        deque.push_front(0)
        self.assertFalse(deque.is_empty())
        deque.pop_back()
        self.assertTrue(deque.is_empty())

    def test_len(self):
        deque = Deque()
        self.assertEqual(len(deque), 0)
        for i in range(0, 10):
            deque.push_front(i)
            self.assertEqual(i + 1, len(deque))
        for i in range(0, 10):
            deque.pop_front()
            self.assertEqual(9 - i, len(deque))

    def test_push_front(self):
        deque = Deque()
        for i in range(0, 10):
            deque.push_front(i)
            self.assertEqual(i, deque.peek_front())
            self.assertEqual(i + 1, len(deque))
        self.assertEqual(0, deque.peek_back())

    def test_push_back(self):
        deque = Deque()
        for i in range(0, 10):
            deque.push_back(i)
            self.assertEqual(i, deque.peek_back())
            self.assertEqual(i + 1, len(deque))
        self.assertEqual(0, deque.peek_front())

    def test_pop_front(self):
        deque = Deque()
        for i in range(0, 10):
            deque.push_back(i)

        for i in range(0, 10):
            self.assertEqual(i, deque.pop_front())
            self.assertEqual(9 - i, len(deque))
        self.assertTrue(deque.is_empty())
        self.assertRaises(IndexError, deque.pop_front)

    def test_pop_back(self):
        deque = Deque()
        for i in range(0, 10):
            deque.push_front(i)

        for i in range(0, 10):
            self.assertEqual(i, deque.pop_back())
            self.assertEqual(9 - i, len(deque))
        self.assertTrue(deque.is_empty())
        self.assertRaises(IndexError, deque.pop_back)

    def test_iter(self):
        deque = Deque()
        for i in range(0, 10):
            deque.push_back(i)

        for (i, j) in zip(range(0, 10), deque):
            self.assertEqual(i, j)

    def test_clear(self):
        deque = Deque()
        for i in range(0, 10):
            deque.push_back(i)

        self.assertFalse(deque.is_empty())
        deque.clear()
        self.assertTrue(deque.is_empty())
        self.assertEqual(0, len(deque))
        self.assertRaises(IndexError, deque.peek_front)
        self.assertRaises(IndexError, deque.peek_back)
        self.assertRaises(IndexError, deque.pop_front)
        self.assertRaises(IndexError, deque.pop_back)

    def test_retain_if(self):
        deque = Deque()
        for i in range(0, 10):
            deque.push_back(i)

        deque.retain_if(lambda x: x % 2 != 0)
        self.assertEqual(5, len(deque))

        for (i, j) in zip(range(1, 10, 2), deque):
            self.assertEqual(i, j)

if __name__ == '__main__':
    unittest.main()
