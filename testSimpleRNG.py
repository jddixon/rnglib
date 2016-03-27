#!/usr/bin/python3

# testSimpleRNG.py
import os
import shutil
import time
import unittest
import rnglib

TEST_DIR = 'tmp'


class TestSimpleRNG (unittest.TestCase):

    def setUp(self):
        now = time.time()
        self.rng = rnglib.SimpleRNG(now)
        if not os.path.exists(TEST_DIR):
            os.makedirs(TEST_DIR)

    def tearDown(self):
        pass

    # utility functions #############################################
    def _buildData(self, count):
        self.assertTrue(count > 0)
        data = bytearray(count)
        for i in range(count):
            self.assertTrue(data[i] == 0)
        self.assertEqual(count, len(data))
        return data

    # XXX NOT CURRENTLY USED
    def setABit(self, vector, value):
        """ treat a 32 byte vector as a bit vector of 256 bits """
        byte = int(value / 8)
        bit = value % 8
        vector[byte] |= 1 << bit
        return vector

    # XXX NOT CURRENTLY USED
    def nonZeroBits(self, vector):
        pass

    # actual unit tests #############################################
    def testConstants(self):
        maxInt16 = self.rng.MAX_INT16
        maxInt32 = self.rng.MAX_INT32
        maxInt64 = self.rng.MAX_INT64

        self.assertEqual(65536, maxInt16)
        self.assertEqual(maxInt16 * maxInt16, maxInt32)
        self.assertEqual(maxInt32 * maxInt32, maxInt64)

    def testSimplestConstructor(self):
        self.assertFalse(self.rng is None)

    def testSeed(self):
        seed = self.rng.nextInt16()

        # if the seed is the same, the numbers generated should be the same
        rng1 = rnglib.SimpleRNG(seed)
        rng2 = rnglib.SimpleRNG(seed)

        for i in range(16):
            a = rng1.nextInt16()
            b = rng2.nextInt16()
            self.assertEqual(a, b)

        # if the seeds differ, with a very high probability the numbers
        # generated should differ
        seed1 = (seed << 16) | seed
        seed2 = ~seed1
        rng1 = rnglib.SimpleRNG(seed1)
        rng2 = rnglib.SimpleRNG(seed2)
        a = rng1.nextInt16()
        b = rng2.nextInt16()
        self.assertTrue(a != b)

    def testNextBoolean(self):
        value = self.rng.nextBoolean()
        self.assertTrue((value == True) or (value == False))
        self.assertTrue(isinstance(value, bool))

    def testNextByte(self):
        value = self.rng.nextByte()
        byte = 0

        self.assertTrue((0 <= value) and (value < 256))
        # would like to test that the entire range is filled
        # where the cost of the test is reasonable

    def testNextBytes(self):
        length = 16 + self.rng.nextByte()
        self.assertTrue((16 <= length) and (length < 272))
        data = self._buildData(length)      # builds a byte array
        self.rng.nextBytes(data)
        self.assertEqual(length, len(data))

    def testNextFileName(self):
        for n in range(8):
            maxLen = 16 + n
            name = self.rng.nextFileName(maxLen)
            self.assertTrue(maxLen > len(name))
            self.assertTrue(0 < len(name))

    def testNextDataFile(self):
        for i in range(9):
            fileLen = 16 + self.rng.nextByte()
            (count, pathToFile) = self.rng.nextDataFile(TEST_DIR,
                                                        fileLen + 1, fileLen)
            self.assertTrue(os.path.exists(pathToFile))
            self.assertEqual(os.path.getsize(pathToFile), count)

    def testSomeBytes(self):
        now = time.time()
        rng = rnglib.SimpleRNG(now)
        for i in range(8):
            count = 1 + rng.nextInt16(16)
            b = rng.someBytes(count)
            self.assertEqual(len(b), count)
            self.assertTrue(isinstance(b, bytearray))

    def doNextDataDirTest(self, width, depth):
        dirName = self.rng.nextFileName(8)
        dirPath = "%s/%s" % (TEST_DIR, dirName)
        if os.path.exists(dirPath):
            if os.path.isfile(dirPath):
                os.unlink(dirPath)
            else:
                shutil.rmtree(dirPath)
        self.rng.nextDataDir(dirPath, width, depth, 32)

    def testNextDataDir(self):
        self.doNextDataDirTest(1, 1)
        self.doNextDataDirTest(1, 4)
        self.doNextDataDirTest(4, 1)
        self.doNextDataDirTest(4, 4)

if __name__ == '__main__':
    unittest.main()
