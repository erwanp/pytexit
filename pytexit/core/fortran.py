# -*- coding: utf-8 -*-
"""
Tools to work with FORTRAN formula
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import re


def for2py(a):
    """Converts FORTRAN formula to Python Formula

    Examples
    --------

    convert FORTRAN formula to LaTeX with py2tex::

        py2tex(for2py($FORTRAN_FORMULA))

    """
    # Remove d0 with Python format
    regexp = re.compile(r"(\d*\.{0,1}\d+)[dD]0")
    a = regexp.sub(r"\1", a)

    # Replace Fortran double (ex: 1.0d-2) with Python format (ex: 1.0e-2)
    regexp = re.compile(r"(\d*\.{0,1}\d+)[dD]([-+]?\d+)")
    a = regexp.sub(r"\1e\2", a)

    return a


if __name__ == "__main__":

    from pytexit.test.test_fortran import test_for2py, test_for2tex

    test_for2py()
    test_for2tex()
