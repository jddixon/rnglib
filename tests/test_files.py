#!/usr/bin/env python3
# testDataFile.py

""" Exercise DataFile functionality. """

import unittest

import rnglib


class TestDataFile(unittest.TestCase):
    """ Exercise DataFile functionality. """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simplest_constructor(self):
        """ Verify that the constructor works correctly. """

        leaf0 = rnglib.DataFile("foo")
        self.assertEqual("foo", leaf0.name)
        self.assertEqual(None, leaf0.parent)
        self.assertEqual(leaf0.name, leaf0.path)

        leaf1 = rnglib.DataFile("bar")
        self.assertEqual("bar", leaf1.name)

        self.assertTrue(leaf0.__eq__(leaf0))
        self.assertEqual(leaf0, leaf0)
        self.assertFalse(leaf0.__eq__(leaf1))


if __name__ == '__main__':
    unittest.main()
