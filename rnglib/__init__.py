# rnglib/__init__.py

import os, random, shutil, string


# -------------------------------------------------------------------
# see docs.python.org/2/library/random.html for advice on subclassing
# random.Random.  Override random(), seed(), getstate(), setstate(),
# and jumpahead().  For a crypto-grade rng, all but the first of these
# will be a no-op.
# -------------------------------------------------------------------

__version__      = '0.7.3'
__version_date__ = '2013-06-16'

__all__ = [ \
            # constants, so to speak
            '__version__',      '__version_date__',
            'MAX_INT16',        'MAX_INT32',        'MAX_INT64',
            'FILE_NAME_CHARS',  'FILE_NAME_STARTERS',

            # classes
            "SimpleRNG",  "SystemRNG",
#           "SecureRNG",
          ]

# we pray for constant folding - and we would prefer that these be const
MAX_INT16 = 65536
MAX_INT32 = 65536 * 65536
MAX_INT64 = 65536 * 65536 * 65536 * 65536

FILE_NAME_CHARS =  \
    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-.'
FILE_NAME_STARTERS = \
    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_'

# -------------------------------------------------------------------

class DataFile(object):
    """ this appears to be a stub """

    def __init__(self, name, parent = None):
        # XXX integrity checks
        self._name = name
        # XXX integrity checks
        self._parent = parent

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        if self._parent:
            return os.path.join(self._parent.path, self._name)
        else:
            return self._name

    @property
    def parent(self):
        return self._parent

    def equals(self, other):
        if self == other:
            return True
        if other == None or self.name != other.name:
            return False
        if self.parent and self.parent != other.parent:
            return False
        # XXX STUB - no content??
        return True                                         # GEEP

# -------------------------------------------------------------------

def _stubbed():
    return None
def _notImplemented():
    raise NotImplementedError('not implemented, stateless RNG')

class CommonFunc(object):
    # XXX remove these ASAP; they are now at the module level
    @property
    def MAX_INT16(self):        return 65536
    @property
    def MAX_INT32(self):        return 65536 * 65536
    @property
    def MAX_INT64(self):        return 65536 * 65536 * 65536 * 65536

    @property
    def FILE_NAME_CHARS(self):
        return \
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-.'
    @property
    def FILE_NAME_STARTERS(self):
        return \
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_'
    # END remove these ASAP #########################################

    def nextBoolean(self):
        if self.random() >= 0.5:
            return True
        else:
            return False

    def nextByte(self, max = 256):
        
        if max < 1:
            max = 1
        elif max > 256:
            max = 256

        return int( max * self.random() )

    def _randBytes(self, n):
        for _ in xrange(n):
            yield random.getrandbits(8)

    def nextBytes(self, bs):
        """bs is a bytearray.  Fill it with random bytes."""
        if bs != None:
#           for i in range(len(bs)):
#               bs[i] = self.nextByte()
            n = len(bs)
            if n <= 64:
                val = bytearray(self._randBytes(n))
            else:
                val = bytearray(os.urandom(n))
            bs[:] = val

    def nextInt16(self, max = 65536):
        if (max <= 0) or (65536 < max):
            max = 65536
        return int( max * self.random() )

    def nextInt32(self, max = (65536*65536)):
        if (max <= 0) or ((65536*65536) < max):
            max = (65536*65536)
        return int (max * self.random() )

    def nextInt64(self, max = (65536*65536*65536*65536)):
        """ construed as unsigned 64 bit value """
        if (max <= 0) or ((65536*65536*65536*65536) < max):
            max = (65536*65536*65536*65536)
        return int( max * self.random() )

    def nextReal(self):
        return self.random()

    # ---------------------------------------------------------------

    # These produce strings which are acceptable POSIX file names
    # and also advance a cursor by a multiple of 64 bits.  All strings
    # are at least one byte and less than maxLen bytes n length.  We
    # arbitrarily limit file names to less than 256 characters.

    def _nextFileName(self, nameLen):
        """ always returns at least one character """
        maxStarterNdx = len(FILE_NAME_STARTERS)
        ndx  = self.nextByte(maxStarterNdx)
        name = FILE_NAME_STARTERS[ndx]
        maxCharNdx    = len(FILE_NAME_CHARS)
        for n in range(nameLen - 1):
            ndx  = self.nextByte(maxCharNdx)
            char = FILE_NAME_CHARS[ndx]
            name = name + char
        return name

    def nextFileName(self, maxLen):
        if maxLen < 2:
            maxLen = 2      # this is a ceiling which cannot be reached
        nameLen = 0
        while nameLen == 0:
            nameLen = self.nextByte(maxLen)     # so len < 256
        while True:
            name = self._nextFileName(nameLen)
            if (len(name) > 0) and (string.find(name, "..") == -1):
                break
        return name

    # These are operations on the file system.  Directory depth is at least 1
    # and no more than 'depth'.  Likewise for width, the number of
    # files in a directory, where a file is either a data file or a subdirectory.
    # The number of bytes in a file is at least minLen and less than maxLen.
    # Subdirectory names may be random

    def nextDataFile(self, dirName, maxLen, minLen = 0):
        # silently convert paramaters to reasonable values
        if minLen < 0:
            minLen = 0
        if maxLen < minLen + 1:
            maxLen = minLen + 1

        # loop until the file does not exist
        pathToFile = "%s/%s" % (dirName, self.nextFileName(16))
        while os.path.exists(pathToFile):
            pathToFile = "%s/%s" % (dirName, self.nextFileName(16))

        count = minLen + int(self.random() * (maxLen - minLen))
        data  = bytearray(count)
        self.nextBytes(data)            # fill with random bytes
        # seems likely to be very expensive
        s = ''.join( chr(b) for b in data )
        # XXX NEEDS try BLOCK
        with open(pathToFile, "w") as f:
            f.write(s)
            # could check file size with f.tell()
        return (count, pathToFile)

    # BUGS
    # * on at least one occasion with width = 4 only 3 files/directories
    #   were created at the top level (2 were subdirs)
    # DEFICIENCIES:
    # * no control over percentage of directories
    # * no guarantee that depth will be reached
    def nextDataDir(self, pathToDir, depth, width, maxLen, minLen = 0):
        """ creates a directory tree populated with data files """
        # number of directory levels; 1 means no subdirectories
        if depth < 1:
            depth = 1
        # number of members (files, subdirectories) at each level
        if width < 1:
            width = 1;
        if not os.path.exists(pathToDir):
            # XXX SHOULDTRY
            os.makedirs (pathToDir)
        subdirSoFar = 0
        for i in range( width ):
            if depth > 1:
                if (self.random() > 0.25) and ((i < width - 1) or (subdirSoFar > 0)):
                    # 25% are subdirs
                    # data file i
                    # SPECIFICATION ERROR: file name may not be unique
                    (count, pathToFile) = self.nextDataFile(pathToDir,
                                                        maxLen, minLen)
                else:
                    # directory
                    subdirSoFar += 1
                    # create unique name
                    fileName   = self.nextFileName(16)
                    pathToSubdir = "%s/%s" % (pathToDir, fileName)
                    self.nextDataDir(pathToSubdir, depth-1, width,
                                     maxLen, minLen)
            else:
                # data file
                # SPECIFICATION ERROR: file name may not be unique
                (count, pathToLeaf) = self.nextDataFile(pathToDir, maxLen, minLen) 

class SimpleRNG(random.Random, CommonFunc):
    # if salt is None, uses time of day as salt
    def __init__ (self, salt = None):
        super(SimpleRNG,self).__init__(salt)    # in first parent

class SystemRNG(random.SystemRandom, CommonFunc):
    """
    A more secure random number generator getting numbers from the
    system's /dev/urandom.  This will be slower than SimpleRNG but
    not so very slow as an RNG using /dev/random, which will block
    untl enough entropy accumulates.
    """
    def __init__ (self, salt = None):
        super(SystemRNG,self).__init__()    # in first parent, I hope
        # self.seed(salt)

class SecureRandom(random.Random):
    """
    Overrides Random.random(), stubs the other 5 functions.
    """

    def __init__ (self, salt = None):
        super(SecureRandom,self).__init__()
        # self.seed(salt)

    def random():
        # XXX STUB: MUST READ /dev/random for some number of bytes
        pass

    seed     = jumpahead    = _stubbed
    getstate = setstate     = _notImplemented

class SecureRNG(SecureRandom, CommonFunc):
    def __init__ (self, salt = 0):
        super(SecureRNG,self).__init__()    # in first parent, I hope
        # self.seed(salt)


# -------------------------------------------------------------------
#class SecureRNG(AbstractRNG):
#
#    # XXX THIS IS A STUB XXX
#
#    # XXX RECOPY FROM SimpleRNG
#
#    def seed(salt):                                         pass
#
#    # each of these operations is expected to advance a cursor by an integer
#    # multiple of 64 bits, 8 bytes
#
#
#    def nextBoolean():                                      pass
#
#    def nextByte():                                         pass
#
#    def nextBytes(len):                                     pass
#
#    def nextInt16():                                        pass
#
#    def nextInt32():                                        pass
#
#    def nextInt64():                                        pass
#    # construed as 64 bit value
#
#    def nextReal():                                         pass
#
#    # These produce strings which are acceptable POSIX file names
#    # All strings are at least one byte in length.
#
#    def nextName(maxLen):                                   pass
#
#    # These are operations on the file system.  Directory depth is at least 1
#    # and no more than 'depth'.  Likewise for width, the number of
#    # files in a directory, where a file is either a data file or a subdirectory.
#    # The number of bytes in a file is at least minLen and may not exceed maxLen.
#    # Subdirectory names may be random
#
#    def nextDataFile(name, minLen, maxLen):                 pass
#
#    def nextDataDir(name, depth, width, minLen, maxLen):    pass
#
