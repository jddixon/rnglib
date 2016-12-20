#!/usr/bin/env python3
# rnglib/test_valid_file_name.py

from argparse import Namespace
import os
import unittest

from rnglib import valid_file_name


class TestValidFileName (unittest.TestCase):

    def test_file_names(self):
        self.assertTrue(valid_file_name('1'))
        self.assertTrue(valid_file_name('_'))
        self.assertTrue(valid_file_name('_.'))
        self.assertTrue(valid_file_name('_-'))

        self.assertFalse(valid_file_name(''))
        self.assertFalse(valid_file_name('-'))
        self.assertFalse(valid_file_name('~'))
        self.assertFalse(valid_file_name('$'))
        self.assertFalse(valid_file_name('?'))
        self.assertFalse(valid_file_name('!'))
        self.assertFalse(valid_file_name('.'))


if __name__ == '__main__':
    unittest.main()
