# -*- coding: utf-8 -*-
"""

"""


from __future__ import absolute_import, division, print_function, unicode_literals

from pytexit import for2py, for2tex


def test_for2py(verbose=True, *args, **kwargs):

    examples = ["x=1.0d-2", "a=3.2d0+3d1", "3d-12"]
    output = ["x=1.0e-2", "a=3.2+3e1", "3e-12"]

    if verbose:
        print("FORTRAN\t\tPython")
    for a, o in zip(examples, output):
        if verbose:
            print(("{0}\t {1}".format(a, for2py(a))))
        assert for2py(a) == o


def test_for2tex(verbose=True, *args, **kwargs):

    assert (
        for2tex(
            (r"2.8d-11 * exp(-(26500 - 0.5 * 1.97 * 11600 )/T_gas)"),
            simplify_output=True,
        )
        == "$$2.8\\times{10}^{-11} e^{\\frac{-\\left(26500-0.5\\times"
        + "1.97\\times11600\\right)}{T_{gas}}}$$"
    )


if __name__ == "__main__":

    test_for2py()
    test_for2tex()
