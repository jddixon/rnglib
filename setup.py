#!/usr/bin/python3
# rnglib/setup.py

""" Set up distutils for rnglib. """

import re
from distutils.core import setup
__version__ = re.search(r"__version__\s*=\s*'(.*)'",
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
      description='random number geerator library',
      url='https:/jddixon.github.io/rnglib',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python 3',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ])
