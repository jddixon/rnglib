#!/usr/bin/env python3
# rnglib/test_valid_file_name.py

""" Exercise the valid_file_name() function. """

import unittest

from rnglib import valid_file_name


class TestValidFileName(unittest.TestCase):
    """ Exercise the valid_file_name() function. """

    def test_file_names(self):
        """
        Verify that known good and known bad names succeed or fail
        as appropriate.
        """
        self.assertTrue(valid_file_name('1'))
        self.assertTrue(valid_file_name('_'))
        self.assertTrue(valid_file_name('_.'))
        self.assertTrue(valid_file_name('_-'))

        self.assertTrue(valid_file_name('1abc._'))
        self.assertTrue(valid_file_name('abc._def'))
        self.assertTrue(valid_file_name('QRS.T..UV_def'))

        self.assertFalse(valid_file_name(''))
        self.assertFalse(valid_file_name('-'))
        self.assertFalse(valid_file_name('~'))
        self.assertFalse(valid_file_name('$'))
        self.assertFalse(valid_file_name('?'))
        self.assertFalse(valid_file_name('!'))
        self.assertFalse(valid_file_name('.'))

        self.assertFalse(valid_file_name('1abc ._'))    # contains a space
        self.assertFalse(valid_file_name('1abc\t._'))   # contains a tab
        self.assertFalse(valid_file_name('QRS.T..UV_def$'))  # dollar sign


if __name__ == '__main__':
    unittest.main()
