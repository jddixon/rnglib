# rnglib/__init__.py

"""
See docs.python.org/2/library/random.html for advice on subclassing
random.Random.  Override random(), seed(), getstate(), setstate(),
and jumpahead().  For a crypto-grade rng, all but the first of these
will be a no-op.
"""

import os
import random
import re
import shutil
import string

__version__ = '1.1.1'
__version_date__ = '2016-12-20'

__all__ = [ \
    # constants, so to speak
    '__version__', '__version_date__',
    'MAX_INT16', 'MAX_INT32', 'MAX_INT64',
    'FILE_NAME_CHARS', 'FILE_NAME_STARTERS',

    # functions
    'valid_file_name'

    # classes
    'SimpleRNG', 'SystemRNG', 'SecureRNG', 'DataFile'
]

# we pray for constant folding - and we would prefer that these be const
MAX_INT16 = 65536
MAX_INT32 = 65536 * 65536
MAX_INT64 = 65536 * 65536 * 65536 * 65536

FILE_NAME_CHARS =  \
    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-.'
FILE_NAME_STARTERS = \
    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_'

VALID_FILE_NAME_PAT = \
    r'^[' + FILE_NAME_STARTERS + '](?:' + FILE_NAME_CHARS + ')*'
VALID_FILE_NAME_RE = re.compile(VALID_FILE_NAME_PAT)


def valid_file_name(string):
    m = VALID_FILE_NAME_RE.match(string)
    return m is not None

# -------------------------------------------------------------------
# XXX USED ONLY IN TESTING XXX


class DataFile(object):
    """ this appears to be a stub """

    def __init__(self, name, parent=None):
        # XXX integrity checks
        self._name = name
        # XXX integrity checks
        self._parent = parent

    @property
    def name(self):
        """ Return the name of the data file. """
        return self._name

    @property
    def path(self):
        """ Return a relative or absolute path to the data file. """
        if self._parent:
            return os.path.join(self._parent.path, self._name)
        else:
            return self._name

    @property
    def parent(self):
        """ Return the name of the data file's parent. """
        return self._parent

    def __eq__(self, other):
        """ Return whether two data files are the same. """

        if self is other:
            return True
        if other is None or self.name != other.name:
            return False
        if self.parent and self.parent != other.parent:
            return False
        # XXX STUB - no content??
        return True

# -------------------------------------------------------------------


def _stubbed():
    """ Unimplemented function. """
    return None


def _not_implemented():
    """ Raise Noimplemented. """
    raise NotImplementedError('not implemented, stateless RNG')


class CommonFunc(object):
    """
    Parent class for RNG classes.

    This class contains convenience functions to be added to Random.
    """

    # OBSOLETE ------------------------------------------------------
    # These are renamed per PEP 8.

    def nextBoolean(self):
        """ Return a quasi-random boolean value. """
        return self.next_boolean()

    def nextByte(self, max_=256):
        """ Return a quasi-random byte value between 0 and max_ inclusive. """
        return self.next_byte(max_)

    def nextBytes(self, bs_):
        """bs is a bytearray.  Fill it with random bytes."""
        return self.next_bytes(bs_)

    def someBytes(self, count):
        """ return a bytearray of N random bytes """
        return self.some_bytes(count)

    def nextInt16(self, max_=65536):
        """ Return a quasi-random 16-bit int. """
        return self.next_int16(max_)

    def nextInt32(self, max_=(65536 * 65536)):
        """ Return a quasi-random 32-bit int < max_. """
        return self.next_int32(max_)

    def nextInt64(self, max_=(65536 * 65536 * 65536 * 65536)):
        """ Return a quasi-random 64-bit int < max_. """
        return self.next_int64(max_)

    def nextReal(self):
        """ Return a quasi-random floating-point number. """
        return self.next_real()

    def nextFileName(self, max_len):
        """ Return a legal file name with 0 < length < max_len). """
        return self.next_file_name(max_len)

    def nextDataFile(self, dir_name, max_len, min_len=0):
        """
        Return a data file in directory dir_name with a quasi-random name
        and contents.   The file is at least min_len bytes log and less than
        max_len bytes long.  Parameters are silently converted to reasonable
        values if necessary.
        """
        return self.next_data_file(dir_name, max_len, min_len)

    def nextDataDir(self, path_to_dir, depth, width, max_len, min_len=0):
        """ creates a directory tree populated with data files """
        return self.next_data_dir(path_to_dir, depth, width, max_len, min_len)

    # END OBSOLETE --------------------------------------------------

    def random(self):
        """ Subclasses must override. """
        raise NotImplementedError

    def next_boolean(self):
        """ Return a quasi-random boolean value. """

        return self.random() >= 0.5

    def next_byte(self, max_=256):
        """ Return a quasi-random byte value between 0 and 255 inclusive. """

        if max_ < 1:
            max_ = 1
        elif max_ > 256:
            max_ = 256

        return int(max_ * self.random())

    def _rand_bytes(self, count):
        for _ in range(count):
            yield random.getrandbits(8)

    def next_bytes(self, bs_):
        """bs_ is a bytearray.  Fill it with random bytes."""
        if bs_ is not None:
            #           for i in range(len(bs_)):
            #               bs_[i] = self.nextByte()
            lbs = len(bs_)
            if lbs <= 64:
                val = bytearray(self._rand_bytes(lbs))
            else:
                val = bytearray(os.urandom(lbs))
            bs_[:] = val

    def some_bytes(self, count):
        """ return a bytearray of N random bytes """
        buffer = bytearray(count)
        self.next_bytes(buffer)
        return buffer

    def next_int16(self, max_=65536):
        """ Return a quasi-random 16-bit int < max_. """

        if (max_ <= 0) or (max_ > 65536):
            max_ = 65536
        return int(max_ * self.random())

    def next_int32(self, max_=(65536 * 65536)):
        """ Return a quasi-random 32-bit int < max_. """
        if (max_ <= 0) or ((65536 * 65536) < max_):
            max_ = (65536 * 65536)
        return int(max_ * self.random())

    def next_int64(self, max_=(65536 * 65536 * 65536 * 65536)):
        """ Return a quasi-random 64-bit int < max_. """

        if (max_ <= 0) or ((65536 * 65536 * 65536 * 65536) < max_):
            max_ = (65536 * 65536 * 65536 * 65536)
        return int(max_ * self.random())

    def next_real(self):
        """ Return a quasi-random floating-point number. """

        return self.random()

    # ---------------------------------------------------------------

    # These produce strings which are acceptable POSIX file names
    # and also advance a cursor by a multiple of 64 bits.  All strings
    # are at least one byte and less than max_Len bytes n length.  We
    # arbitrarily limit file names to less than 256 characters.

    def _next_file_name(self, name_len):
        """ Always returns at least one character. """

        max_starter_ndx = len(FILE_NAME_STARTERS)
        ndx = self.nextByte(max_starter_ndx)
        name = FILE_NAME_STARTERS[ndx]
        max_char_ndx = len(FILE_NAME_CHARS)
        for _ in range(name_len - 1):
            ndx = self.nextByte(max_char_ndx)
            char = FILE_NAME_CHARS[ndx]
            name = name + char
        return name

    def next_file_name(self, max_len):
        """ Return a legal file name with 0 < length < max_len). """
        if max_len < 2:
            max_len = 2      # this is a ceiling which cannot be reached
        name_len = 0
        while name_len == 0:
            name_len = self.nextByte(max_len)     # so len < 256
        while True:
            name = self._next_file_name(name_len)
            if (len(name) > 0) and (name.find("..") == -1):
                break
        return name

    # These are operations on the file system.  Directory depth is at least 1
    # and no more than 'depth'.  Likewise for width, the number of
    # files in a directory, where a file is either a data file or a subdirectory.
    # The number of bytes in a file is at least min_len and less than max_len.
    # Subdirectory names may be random

    def next_data_file(self, dir_name, max_len, min_len=0):
        """
        Return a data file in directory dir_name with a quasi-random name
        and contents.   The file is at least min_len bytes log and less than
        max_len bytes long.  Parameters are silently converted to reasonable
        values if necessary.
        """

        if min_len < 0:
            min_len = 0
        if max_len < min_len + 1:
            max_len = min_len + 1

        # loop until name does not match existing file
        path_to_file = "%s/%s" % (dir_name, self.next_file_name(16))
        while os.path.exists(path_to_file):
            path_to_file = "%s/%s" % (dir_name, self.next_file_name(16))

        count = min_len + int(self.random() * (max_len - min_len))
        data = self.some_bytes(count)

        # XXX NEEDS try BLOCK
        with open(path_to_file, "wb") as file:
            file.write(data)
            # could check file size with file.tell()
        return (count, path_to_file)

    # BUGS
    # * on at least one occasion with width = 4 only 3 files/directories
    #   were created at the top level (2 were subdirs)
    # DEFICIENCIES:
    # * no control over percentage of directories
    # * no guarantee that depth will be reached
    def next_data_dir(self, path_to_dir, depth, width, max_len, min_len=0):
        """ creates a directory tree populated with data files """
        # number of directory levels; 1 means no subdirectories
        if depth < 1:
            depth = 1
        # number of members (files, subdirectories) at each level
        if width < 1:
            width = 1
        if not os.path.exists(path_to_dir):
            # XXX SHOULDTRY
            os.makedirs(path_to_dir)
        subdir_so_far = 0
        for i in range(width):
            if depth > 1:
                if (self.random() > 0.25) and (
                        (i < width - 1) or (subdir_so_far > 0)):
                    # 25% are subdirs
                    # data file i
                    # SPECIFICATION ERROR: file name may not be unique
                    (_, path_to_file) = self.next_data_file(
                        path_to_dir, max_len, min_len)
                else:
                    # directory
                    subdir_so_far += 1
                    # create unique name
                    file_name = self.nextFileName(16)
                    path_to_subdir = "%s/%s" % (path_to_dir, file_name)
                    self.next_data_dir(path_to_subdir, depth - 1, width,
                                       max_len, min_len)
            else:
                # data file
                # SPECIFICATION ERROR: file name may not be unique
                (_, path_to_leaf) = self.next_data_file(
                    path_to_dir, max_len, min_len)


class SimpleRNG(random.Random, CommonFunc):
    """ if salt is None, uses time of day as salt """

    def __init__(self, salt=None):
        super().__init__(salt)    # in first parent


class SystemRNG(random.SystemRandom, CommonFunc):
    """
    A more secure random number generator getting numbers from the
    system's /dev/urandom.  This will be slower than SimpleRNG but
    not so very slow as an RNG using /dev/random, which will block
    untl enough entropy accumulates.
    """

    def __init__(self, salt=None):
        super().__init__()    # in first parent, I hope
        # self.seed(salt)


class SecureRandom(random.Random):
    """
    Overrides Random.random(), stubs the other 5 functions.
    """

    def __init__(self, salt=None):
        super().__init__()
        # self.seed(salt)

    def random(self):
        # XXX STUB: MUST READ /dev/random for some number of bytes
        pass

    seed = _stubbed
    jumpahead = _stubbed

    getstate = _not_implemented
    setstate = _not_implemented


class SecureRNG(SecureRandom, CommonFunc):

    def __init__(self, salt=0):
        super().__init__()    # in first parent, I hope
        # self.seed(salt)

#    # XXX THIS IS A STUB XXX
