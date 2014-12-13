#!/usr/bin/python3

# ~/dev/py/rnglib/testRandomFunc.py

import math, random, time
from rnglib import SimpleRNG

# This is not a test in the usual sense.  It exercises random.Random
# functions through a SimpleRNG instance and makes the results available
# for human inspection.

# This code is hacked from python2.7/random.py and so made available
# under the same license as Python itself.

def doTest( n, func, args):
    print("%u invocations of %s" % (n, func.__name__))
    total   = 0.0
    sqsum   = 0.0
    smallest= 1e10
    largest = -1e10
    t0      = time.time()
    for i in range(n):
        x       = func(*args)
        total  += x
        sqsum   = sqsum + x*x
        smallest= min(x, smallest)
        largest = max(x, largest)
    t1      = time.time()
    print("  %6.4f sec, " % round(t1-t0, 4), end=' ') 
    avg     = total/n
    stddev  = math.sqrt(sqsum/n - avg*avg)
    print('avg %g, stddev %g, min %g, max %g' % \
              (avg, stddev, smallest, largest))


def randTest(n=1000):
    rng = SimpleRNG()
    doTest(n, rng.random, ())
    doTest(n, rng.normalvariate, (0.0, 1.0))
    doTest(n, rng.lognormvariate, (0.0, 1.0))
    doTest(n, rng.vonmisesvariate, (0.0, 1.0))
    doTest(n, rng.gammavariate, (0.01, 1.0))
    doTest(n, rng.gammavariate, (0.1, 1.0))
    doTest(n, rng.gammavariate, (0.1, 2.0))
    doTest(n, rng.gammavariate, (0.5, 1.0))
    doTest(n, rng.gammavariate, (0.9, 1.0))
    doTest(n, rng.gammavariate, (1.0, 1.0))
    doTest(n, rng.gammavariate, (2.0, 1.0))
    doTest(n, rng.gammavariate, (20.0, 1.0))
    doTest(n, rng.gammavariate, (200.0, 1.0))
    doTest(n, rng.gauss, (0.0, 1.0))
    doTest(n, rng.betavariate, (3.0, 3.0))
    doTest(n, rng.triangular, (0.0, 1.0, 1.0/3.0))

if __name__ == '__main__':
    randTest()
