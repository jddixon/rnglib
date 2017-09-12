#!/usr/bin/env python3
# testSystemRNG.py

""" Test the crypto-grade system random number generator. """

import os
import shutil
import time
import unittest
import rnglib

TEST_DIR = 'tmp'


class TestSystemRNG(unittest.TestCase):
    """ Test the crypto-grade system random number generator. """

    def setUp(self):
        now = time.time()
        self.rng = rnglib.SystemRNG(now)
        os.makedirs(TEST_DIR, exist_ok=True, mode=0o755)

    def tearDown(self):
        pass

    # utility functions #############################################
    def _build_data(self, count):
        self.assertTrue(count > 0)
        data = bytearray(count)
        for ndx in range(count):
            self.assertTrue(data[ndx] == 0)
        self.assertEqual(count, len(data))
        return data

#   # XXX NOT CURRENTLY USED
#   def set_a_bit(self, vector, value):
#       """ treat a 32 byte vector as a bit vector of 256 bits """
#       byte = int(value / 8)
#       bit = value % 8
#       vector[byte] |= 1 << bit
#       return vector

#   # XXX NOT CURRENTLY USED
#   def non_zero_bits(self, vector):
#       pass

    def test_constants(self):
        """ Verify constants have expected values. """
        max_int16 = rnglib.MAX_INT16
        max_int32 = rnglib.MAX_INT32
        max_int64 = rnglib.MAX_INT64

        self.assertEqual(65536, max_int16)
        self.assertEqual(max_int16 * max_int16, max_int32)
        self.assertEqual(max_int32 * max_int32, max_int64)

    def test_simplest_constructor(self):
        """ Verify local random number generator has been defined. """
        self.assertFalse(self.rng is None)

#   def test_seed(self):
#       pass

    def test_next_boolean(self):
        """ Test the secure next_boolean() function. """

        value = self.rng.next_boolean()
        self.assertTrue((value is True) or (value is False))
        self.assertTrue(isinstance(value, bool))

    def test_next_byte(self):
        """ Test the secure next_byte() function. """
        value = self.rng.next_byte()

        self.assertTrue((value >= 0) and (value < 256))
        # would like to test that the entire range is filled
        # where the cost of the test is reasonable

    def test_next_bytes(self):
        """ Test the secure next_bytes() function. """
        length = 16 + self.rng.next_byte()
        self.assertTrue((length >= 16) and (length < 272))
        data = self._build_data(length)      # builds a byte array
        self.rng.next_bytes(data)
        self.assertEqual(length, len(data))

    def test_next_file_name(self):
        """ Test the secure next_file_name() function. """
        for count in range(8):
            max_len = 16 + count
            name = self.rng.next_file_name(max_len)
            self.assertTrue(max_len > len(name))
            self.assertTrue(len(name) > 0)

    def test_next_data_file(self):
        """ Test the secure next_data_file() function. """
        for _ in range(9):
            file_len = 16 + self.rng.next_byte()
            (count, path_to_file) = self.rng.next_data_file(
                TEST_DIR, file_len + 1, file_len)
            self.assertTrue(os.path.exists(path_to_file))
            self.assertEqual(os.path.getsize(path_to_file), count)

    def do_next_data_dir_test(self, width, depth):
        """
        Test creating test data directory with these parameters.
        """
        dir_name = self.rng.next_file_name(8)
        dir_path = "%s/%s" % (TEST_DIR, dir_name)
        if os.path.exists(dir_path):
            if os.path.isfile(dir_path):
                os.unlink(dir_path)
            else:
                shutil.rmtree(dir_path)
        self.rng.next_data_dir(dir_path, width, depth, 32)

    def test_next_data_dir(self):
        """
        Test creating test data directories with various parameters.
        """
        self.do_next_data_dir_test(1, 1)
        self.do_next_data_dir_test(1, 4)
        self.do_next_data_dir_test(4, 1)
        self.do_next_data_dir_test(4, 4)

    def test_bulk_generation(self):
        """
        Test generating many AES iv+keys.
        """
        t0 = time.time()
        for i in range(10000):
            self.rng.some_bytes(16)     # discarding outputs
        t1 = time.time()
        print("time to generate 10,000 AES iv + key: %f seconds" % (t1 - t0))


if __name__ == '__main__':
    unittest.main()
