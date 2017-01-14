# rnglib

A Python random number generator especially useful for generating
quasi-random strings, data files, and directory trees containing
random numbers of data files with random names and random content.

## Classes

This package contains three classes, **SimpleRNG**, **SystemRNG**,
and **SecureRNG**.  All of these subclass Python's `random` standard
library and so `random`'s functions can be called through any
of `rnglib`'s three subclasses.

**SimpleRNG** is the fastest of the subclasses.  It uses the
[Mersenne Twister](https://en.wikipedia.org/wiki/Mersenne_Twister)
and so is completely predictable with a very long period.
It is suitable where speed and predictability are both important.
That is, you can be certain that if you provide the same
[seed](https://en.wikipedia.org/wiki/Random_seed),
then the sequence of numbers generated will be exactly the same.  This is
often important for debugging.

**SystemRNG** is a secure random number generator, meaning that it is
extremely difficult or impossible to predict the next number
generated in a sequence.  It is based on the system's `/dev/urandom`.
This relies in part upon
[entropy](https://en.wikipedia.org/wiki/Entropy (Computing))
accumulated by the system; when
this is insufficient (when we run out of entropy) it will revert to using
a very secure programmable random number generator.

**SecureRNG** is a very secure random number generator based
`/dev/random`.  This also relies upon entropy accumulated by the
system, but will **block** when there is not enough entropy available
to generate the random value requested.  This means that it can be
very slow.

For normal use in testing, `SimpleRNG` is preferred.  When there is
a requirement for a reasonable level of security, as in the
generation of passwords and cryptographic keys with reasonable
strength, `SystemRNG` is recommended.  Where there is a need for
very secure random values, use `SecureRNG` but expect to wait a
while for results.

## Functions

In addition to the functions available from Python's `random` package,
`rnglib` also provides

	next_boolean()
	next_byte(max=256)
	next_bytes(buffer)
	next_int16(max=65536])
	next_int32(max=65536*65536)
	next_int64(max=65536*65536*65536*65536)
	next_real()
	next_file_name(max_len)
	next_data_file(dir_name, max_len, min_len=0)
	next_data_dir(pathToDir, depth, width, max_len, min_len=0)

Given a buffer of arbitrary length, `next_bytes()` will fill it with random
bytes using the chosen random number generator (`SimpleRNG`, `SystemRNG`,
or `SecureRNG`).

File names generated by `next_file_name()` are at least one character long.
The first letter must be alphabetic (including the underscore)
whereas other characters may also be numeric or either of dot and dash
("." and "-").

The function `next_data_file()` creates a file with a random name in the
directory indicated.  The file length will vary from min_len (which
defaults to zero) up to but excluding max_len bytes.

The `next_data_dir()` function creates a directory structure that is
'depth' deep and 'width' wide, where the latter means that there
will be that many files in each directory and subdirectory created
(where a file is either a data file or a directory). `depth` and
`width` must both be at least 1.  `max_len` and `min_len` are used as in
`next_data_file()`.

## History

`rnglib` was implemented as part of the
[XLattice](http://www.xlattice.org)
project.  A Go language implementation forms part of
[xlattice_go.](https://github.com/jddixon/xlattice_go)

## Project Status

Stable, good benchmarks.


## On-line Documentation

More information on the **rnglib** project can be found
[here](https://jddixon.github.io/rnglib)
