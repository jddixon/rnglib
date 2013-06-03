#!/usr/bin/python

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
        self.assertEquals( "foo", leaf0.name )
        self.assertEquals( None, leaf0.parent )
        self.assertEquals( leaf0.name, leaf0.path )

        leaf1 = rnglib.DataFile("bar")
        self.assertEquals( "bar", leaf1.name )

        self.assertTrue  ( leaf0.equals(leaf0) )
        self.assertFalse ( leaf0.equals(leaf1) )

if __name__ == '__main__':
    unittest.main()
