#!/usr/bin/python3

# rnglib/setup.py

import re
from distutils.core import setup
__version__ = re.search("__version__\s*=\s*'(.*)'",
                        open('rnglib/__init__.py').read()).group(1)

# see http://docs.python.org/distutils/setupscript.html

setup(name='rnglib',
      version=__version__,
      author='Jim Dixon',
      author_email='jddixon@gmail.com',
      py_modules=[],
      packages=['rnglib', ],
      # following could be in scripts/ subdir
      scripts=[],          # front end module(s)
      # MISSING description
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
      ],
      )