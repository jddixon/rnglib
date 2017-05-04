#!/usr/bin/env python3
# ~/dev/py/rnglib/testRandomFunc.py

""" Exercise the random number generator functions. """

import math
import time
import unittest

from rnglib import SimpleRNG


class TestRandomFunc(unittest.TestCase):
    """
    Exercise the random number generator functions.

    This is not a test in the usual sense.  It exercises random.Random
    functions through a SimpleRNG instance and makes the results available
    for human inspection.

    This code is hacked from python2.7/random.py and so made available
    under the same license as Python itself.
   """

    def do_test(self, count, func, args):
        """ Carry out tests with specified parameters. """

        # print("%u invocations of %s" % (n, func.__name__))
        total = 0.0
        sqsum = 0.0
        smallest = 1e10
        largest = -1e10
        t00 = time.time()
        for _ in range(count):
            xxx = func(*args)
            total += xxx
            sqsum = sqsum + xxx * xxx
            smallest = min(xxx, smallest)
            largest = max(xxx, largest)
        t01 = time.time()
        print("  %6.4f sec, " % round(t01 - t00, 4), end=' ')
        avg = total / count
        stddev = math.sqrt(sqsum / count - avg * avg)
        print('avg %g, stddev %g, min %g, max %g' %
              (avg, stddev, smallest, largest))

    def rand_test(self, count=1000):
        """ Repeath a suite of tests N times. """

        rng = SimpleRNG(time.time())
        self.do_test(count, rng.random, ())
        self.do_test(count, rng.normalvariate, (0.0, 1.0))
        self.do_test(count, rng.lognormvariate, (0.0, 1.0))
        self.do_test(count, rng.vonmisesvariate, (0.0, 1.0))
        self.do_test(count, rng.gammavariate, (0.01, 1.0))
        self.do_test(count, rng.gammavariate, (0.1, 1.0))
        self.do_test(count, rng.gammavariate, (0.1, 2.0))
        self.do_test(count, rng.gammavariate, (0.5, 1.0))
        self.do_test(count, rng.gammavariate, (0.9, 1.0))
        self.do_test(count, rng.gammavariate, (1.0, 1.0))
        self.do_test(count, rng.gammavariate, (2.0, 1.0))
        self.do_test(count, rng.gammavariate, (20.0, 1.0))
        self.do_test(count, rng.gammavariate, (200.0, 1.0))
        self.do_test(count, rng.gauss, (0.0, 1.0))
        self.do_test(count, rng.betavariate, (3.0, 3.0))
        self.do_test(count, rng.triangular, (0.0, 1.0, 1.0 / 3.0))

    def test_rand_test(self):
        """ Repeat the test suite a thousand times. """

        self.rand_test(count=1000)


if __name__ == '__main__':
    unittest.main()
