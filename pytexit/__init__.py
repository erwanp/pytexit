# -*- coding: utf-8 -*-
"""
pytexit
"""

from __future__ import absolute_import

from .core import *
from .pytexit import py2tex, for2py, for2tex

def __get_version__():
    from os.path import join, dirname
    # Read version number from file
    with open(join(dirname(__file__), '__version__.txt')) as version_file:
        __version__ = version_file.read().strip()
    return __version__

__version__ = __get_version__()