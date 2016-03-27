#!/usr/bin/python3

# testDataFile.py
import unittest

import rnglib


class TestDataFile (unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################
    def testSimplestConstructor(self):
        leaf0 = rnglib.DataFile("foo")
        self.assertEqual("foo", leaf0.name)
        self.assertEqual(None, leaf0.parent)
        self.assertEqual(leaf0.name, leaf0.path)

        leaf1 = rnglib.DataFile("bar")
        self.assertEqual("bar", leaf1.name)

        self.assertTrue(leaf0.equals(leaf0))
        self.assertFalse(leaf0.equals(leaf1))

if __name__ == '__main__':
    unittest.main()
