#!/usr/bin/python3

import unittest, re

from HashMap import HashMap, word_frequency

letters = ['alfa', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot', 'golf', 'hotel', 'india', 'juliett', 'kilo',
           'lima', 'mike', 'november', 'oscar', 'papa', 'quebec', 'romeo', 'sierra', 'tango', 'uniform', 'victor',
           'whiskey', 'x-ray', 'yankee', 'zulu']


def sanitize(word):
    return re.sub(r'[^\w\s]', '', word).lower()


class HashMapTests(unittest.TestCase):

    def test_len(self):
        hashmap = HashMap()
        for i, l in enumerate(letters):
            hashmap[l] = i
            self.assertEqual(i + 1, len(hashmap))
        for l in letters:
            hashmap[l] = len(l)
            self.assertEqual(len(letters), len(hashmap))
        for i, l in enumerate(letters):
            del hashmap[l]
            self.assertEqual(len(letters) - i - 1, len(hashmap))

    def test_contains(self):
        hashmap = HashMap()
        for l in letters:
            self.assertFalse(l in hashmap)
            hashmap[l] = l
            self.assertTrue(l in hashmap)
        for l in letters:
            self.assertTrue(l in hashmap)
            del hashmap[l]
            self.assertFalse(l in hashmap)

    def test_insert(self):
        hashmap = HashMap()
        for i, l in enumerate(letters):
            self.assertFalse(l in hashmap)
            hashmap[l] = i
            self.assertTrue(l in hashmap)
        for l in letters:
            self.assertTrue(l in hashmap)
            hashmap[l] = len(l)
            self.assertTrue(l in hashmap)

    def test_get(self):
        hashmap = HashMap()
        for i, l in enumerate(letters):
            self.assertRaises(KeyError, hashmap.__getitem__, l)
            hashmap[l] = i
            self.assertEqual(i, hashmap[l])
        for i, l in enumerate(letters):
            self.assertEqual(i, hashmap[l])
            hashmap[l] = len(l)
            self.assertEqual(len(l), hashmap[l])
        for l in letters:
            self.assertEqual(len(l), hashmap[l])
            del hashmap[l]
            self.assertRaises(KeyError, hashmap.__getitem__, l)

    def test_delete(self):
        hashmap = HashMap()
        for l in letters:
            self.assertRaises(KeyError, hashmap.__delitem__, l)
        for l in letters:
            hashmap[l] = l
        for i, l in enumerate(letters):
            self.assertTrue(l in hashmap)
            del hashmap[l]
            self.assertFalse(l in hashmap)
        self.assertTrue(hashmap.is_empty())
        for l in enumerate(letters):
            self.assertFalse(l in hashmap)
            self.assertRaises(KeyError, hashmap.__delitem__, l)

    def test_load(self):
        hashmap = HashMap()
        self.assertGreaterEqual(1.0, hashmap.max_load_factor)
        self.assertAlmostEqual(0, hashmap.load())
        for l in letters:
            hashmap[l] = l
            self.assertLessEqual(0.05, hashmap.load())
            self.assertGreaterEqual(hashmap.max_load_factor, hashmap.load())
        for l in letters:
            self.assertLessEqual(0.05, hashmap.load())
            self.assertGreaterEqual(hashmap.max_load_factor, hashmap.load())
            del hashmap[l]
        self.assertAlmostEqual(0, hashmap.load())
        for l in letters:
            hashmap[l] = l
            self.assertLessEqual(0.05, hashmap.load())
            self.assertGreaterEqual(hashmap.max_load_factor, hashmap.load())
        load = hashmap.load()
        for l in letters:
            hashmap[l] = len(l)
            self.assertAlmostEqual(load, hashmap.load())
        hashmap.clear()
        self.assertAlmostEqual(0, hashmap.load())
        self.assertGreaterEqual(1.0, hashmap.max_load_factor)

    def test_keys(self):
        hashmap = HashMap()
        for l in letters:
            hashmap[l] = l
        self.assertEqual(len(letters), len(hashmap.keys()))
        self.assertSetEqual(set(letters), hashmap.keys())

    def test_clear(self):
        hashmap = HashMap()
        for l in letters:
            hashmap[l] = l
        self.assertFalse(hashmap.is_empty())
        hashmap.clear()
        self.assertTrue(hashmap.is_empty())
        self.assertAlmostEqual(0, hashmap.load())
        for l in letters:
            self.assertFalse(l in hashmap)
            self.assertRaises(KeyError, hashmap.__getitem__, l)
            self.assertRaises(KeyError, hashmap.__delitem__, l)
#
    def test_iter(self):
        hashmap = HashMap()
        for l in letters:
            hashmap[l] = l
        expected = {l:l for l in letters}
        actual = {k:v for k, v in hashmap}
        self.assertDictEqual(expected, actual)
#
    def test_word_frequency(self):
        with open('romeojuliet.txt', 'r') as reader:
            freq = word_frequency(sanitize(word) for line in reader for word in line.split())
            self.assertEqual(3741, len(freq))
            self.assertEqual(293, freq['romeo'])
            self.assertEqual(176, freq['juliet'])
#
    def test_large_size(self):
        hashmap = HashMap()
        for i in range(10000):
            self.assertFalse(i in hashmap)
            hashmap[i] = i
            self.assertTrue(i in hashmap)
            self.assertEqual(i, hashmap[i])
        self.assertLessEqual(0.05, hashmap.load())
        self.assertGreaterEqual(hashmap.max_load_factor, hashmap.load())

        load = hashmap.load()
        for i in range(10000):
            self.assertTrue(i in hashmap)
            self.assertEqual(i, hashmap[i])
            hashmap[i] = i * i
            self.assertTrue(i in hashmap)
            self.assertEqual(i * i, hashmap[i])
        self.assertAlmostEqual(load, hashmap.load())

        for i in range(10000):
            self.assertTrue(i in hashmap)
            self.assertEqual(i * i, hashmap[i])
            del hashmap[i]
            self.assertFalse(i in hashmap)
        self.assertAlmostEqual(0, hashmap.load())
#
#    def test_sequence(self):
#        pass


if __name__ == '__main__':
    unittest.main()