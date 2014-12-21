#rnglib

A Python random number generator especially useful for generating 
quasi-random strings, data files, and directory trees containing
such random data files.

This package contains three classes, **SimpleRNG**, **SystemRNG**, 
and **SecureRNG**.  All of these subclass Python's "random" standard 
library and so random's functions can be called through any
of rnglib's three subclasses.

**SimpleRNG** is the fastest of the subclasses.  It uses the Mersenne
Twister and so is completely predictable with a very long period.
It is suitable where speed and predictability are both important.
That is, you can be certain that if you provide the same **seed**, then
the sequence of numbers generated will be exactly the same.  This is
often important for debugging.

**SystemRNG** is a secure random number generator, meaning that it is
extremely difficult or impossible to predict the next number 
generated in a sequence.  It is based on the system's /dev/urandom.
This relies in part upon entropy accumulated by the system; when 
this is insufficient (when we run out of entropy) it will revert to using 
a very secure programmable random number generator.

**SecureRNG** is a very secure random number generator based on 
/dev/random.  This also relies upon entropy accumulated by the
system, but will **block** when there is not enough entropy available
to generate the random value requested.  This means that it can be
very slow.

For normal use in testing, SimpleRNG is preferred.  When there is
a requirement for a reasonable level of security, as in the 
generation of passwords and cryptographic keys with reasonable 
strength, SystemRNG is recommended.  Where there is a need for 
very secure random values, use SecureRNG but expect to wait a 
while for results.

In addition to the functions available from Python's random package,
rnglib also provides

    nextBoolean()
    nextByte(max=256)
    nextBytes(buffer)
    nextInt16(max=65536])
    nextInt32(max=65536*65536)
    nextInt64(max=65536*65536*65536*65536)
    nextReal()
    nextFileName(maxLen)
    nextDataFile(dirName, maxLen, minLen=0)
    nextDataDir(pathToDir, depth, width, maxLen, minLen=0)

Given a buffer of arbitrary length, `nextBytes()` will fill it with random
bytes using the chosen random number generator (SimpleRNG, SystemRNG, 
or SecureRNG).

File names generated by `nextFileName()` are at least one character long.  
The first letter must be alphabetic (including the underscore) 
whereas other characters may also be numeric or either of dot and dash
("." and "-").

The function `nextDataFile()` creates a file with a random name in the
directory indicated.  The file length will vary from minLen (which 
defaults to zero) up to but excluding maxLen bytes.

The `nextDataDir()` function creates a directory structure that is
'depth' deep and 'width' wide, where the latter means that there 
will be that many files in each directory and subdirectory created
(where a file is either a data file or a directory). `depth` and
`width` must both be at least 1.  `maxLen` and `minLen` are used as in
`nextDataFile()`.

rnglib was implemented as part of the [XLattice](http://www.xlattice.org) 
project.  A Go language implementation forms part of 
[xlattice_go](https://gibhub.com/jddixon/xlattice_go).

## On-line Documentation

More information on the **rnglib** project can be found [here](https://jddixon.github.io/rnglib)
