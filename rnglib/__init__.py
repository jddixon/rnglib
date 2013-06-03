# rnglib/__init__.py

import os, random, shutil, string
from abc import ABCMeta, abstractmethod, abstractproperty;


__version__      = '0.6.2'
__version_date__ = '2012-06-01'

__all__ = [ \
            # constants, so to speak
            '__version__', '__version_date__',
            # classes
            "AbstractFile", "AbstractRNG", "DataFile", "SecureRNG",
            "SimpleRNG",
          ]

# -------------------------------------------------------------------
class AbstractFile():
    __metaclass__ = ABCMeta

    @abstractproperty
    def name(self):                                         pass
    
    @abstractproperty
    def path(self):                                         pass

# -------------------------------------------------------------------
# rnglib/AbstractRNG.py

class AbstractRNG():
    __metaclass__ = ABCMeta

    # MyRandom interface

    @abstractmethod
    def seed(salt):                                         pass

    # each of these operations is expected to advance a cursor by an integer
    # multiple of 64 bits, 8 bytes

    @abstractmethod
    def nextBoolean():                                      pass
    @abstractmethod
    def nextByte():                                         pass
    @abstractmethod
    def nextBytes(len):                                     pass
    @abstractmethod
    def nextInt16():                                        pass
    @abstractmethod
    def nextInt32():                                        pass
    @abstractmethod
    def nextInt64():                                        pass
    # construed as 64 bit value
    @abstractmethod
    def nextReal():                                         pass

    # These produce strings which are acceptable POSIX file names
    # and also advance a cursor by a multiple of 64 bits.  All strings
    # are at least one byte and less than maxLen bytes in length.
    @abstractmethod
    def nextFileName(maxLen):                               pass

    # These are operations on the file system.  Directory depth is at least 1
    # and no more than 'depth'.  Likewise for width, the number of
    # files in a directory, where a file is either a data file or a subdirectory.
    # The number of bytes in a file is at least minLen and may not exceed maxLen.
    # Subdirectory names may be random
    @abstractmethod
    def nextDataFile(name, minLen, maxLen):                 pass
    @abstractmethod
    def nextDataDir(name, depth, width, minLen, maxLen):    pass

# -------------------------------------------------------------------

class DataFile(AbstractFile):
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
        return True          

# -------------------------------------------------------------------
class SecureRNG(AbstractRNG):

    # XXX THIS IS A STUB XXX

    # XXX RECOPY FROM SimpleRNG

    def seed(salt):                                         pass

    # each of these operations is expected to advance a cursor by an integer
    # multiple of 64 bits, 8 bytes


    def nextBoolean():                                      pass

    def nextByte():                                         pass

    def nextBytes(len):                                     pass

    def nextInt16():                                        pass

    def nextInt32():                                        pass

    def nextInt64():                                        pass
    # construed as 64 bit value

    def nextReal():                                         pass

    # These produce strings which are acceptable POSIX file names
    # and also advance a cursor by a multiple of 64 bits.  All strings
    # are at least one byte in length.

    def nextName(maxLen):                                   pass

    # These are operations on the file system.  Directory depth is at least 1
    # and no more than 'depth'.  Likewise for width, the number of
    # files in a directory, where a file is either a data file or a subdirectory.
    # The number of bytes in a file is at least minLen and may not exceed maxLen.
    # Subdirectory names may be random

    def nextDataFile(name, minLen, maxLen):                 pass

    def nextDataDir(name, depth, width, minLen, maxLen):    pass

# -------------------------------------------------------------------

class SimpleRNG(AbstractRNG):

    # we pray for constant folding
    @property
    def MAX_INT16(self):
        return 65536
    @property
    def MAX_INT32(self):
        return 65536 * 65536
    @property
    def MAX_INT64(self):
        return 65536 * 65536 * 65536 * 65536

    @property
    def FILE_NAME_STARTERS(self):
        return \
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_'

    @property
    def FILE_NAME_CHARS(self):
        return \
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-.'

    def __init__ (self, salt = 0):
        self.seed(salt)

    def seed(self, salt):
        random.seed(salt)

    # TENTATIVELy: each of these operations is expected to advance a 
    # cursor by an integer multiple of 64 bits, 8 bytes

    def nextBoolean(self):
        if random.random() >= 0.5:
            return True
        else:
            return False

    def nextByte(self, max = 256):
        if max < 1:
            max = 1
        elif max > 256:
            max = 256
        return int( max * random.random() ) 

    def nextBytes(self, bs):
        """bs is a bytesarray.  Fill it with random bytes."""
        if bs != None:
            for i in range(len(bs)):
                bs[i] = self.nextByte()

    def nextInt16(self, max = 65536):
        if (max <= 0) or (65536 < max):
            max = 65536
        return int( max * random.random() )

    def nextInt32(self, max = (65536*65536)):
        if (max <= 0) or ((65536*65536) < max):
            max = (65536*65536)
        return int (max * random.random() )

    def nextInt64(self, max = (65536*65536*65536*65536)):
        """ construed as unsigned 64 bit value """
        if (max <= 0) or ((65536*65536*65536*65536) < max):
            max = (65536*65536*65536*65536)
        return int( max * random.random() )

    def nextReal(self):
        return random.random()

    # ---------------------------------------------------------------

    # These produce strings which are acceptable POSIX file names
    # and also advance a cursor by a multiple of 64 bits.  All strings
    # are at least one byte and less than maxLen bytes n length.  We 
    # arbitrarily limit file names to less than 256 characters.

    def _nextFileName(self, nameLen):
        """ always returns at least one character """
        maxStarterNdx = len(self.FILE_NAME_STARTERS)
        ndx  = self.nextByte(maxStarterNdx)
        name = self.FILE_NAME_STARTERS[ndx]
        maxCharNdx    = len(self.FILE_NAME_CHARS)    
        for n in range(nameLen - 1):
            ndx  = self.nextByte(maxCharNdx)
            char = self.FILE_NAME_CHARS[ndx]
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

        count = minLen + int(random.random() * (maxLen - minLen))
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
            os.mkdir (pathToDir)
        subdirSoFar = 0
        for i in range( width ):
            if depth > 1:
                if (random.random() > 0.25) and ((i < width - 1) or (subdirSoFar > 0)):
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



