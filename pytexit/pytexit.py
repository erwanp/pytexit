# -*- coding: utf-8 -*-
"""

=======
pytexit
=======

Convert a Python expression in a LaTeX formula

Install
-------

`pytexit` is on PyPi::

    pip install pytexit


Use
---

In a Terminal::

    py2tex 'x = 2*sqrt(2*pi*k*T_e/m_e)*(DeltaE/(k*T_e))**2*a_0**2'

In a Python console::

    from pytexit import py2tex
    py2tex('x = 2*sqrt(2*pi*k*T_e/m_e)*(DeltaE/(k*T_e))**2*a_0**2')

returns the corresponding LaTeX formula (to re-use in papers)::

    $$x=2\\sqrt{\\frac{2\\pi k T_e}{m_e}} \\left(\\frac{\\Delta E}{k T_e}\\right)^2 a_0^2$$

and (in ipython console only) prints the equation:

.. image:: https://github.com/erwanp/pytexit/blob/master/docs/output.png


Notes
-----

This module isn't unit aware and isn't designed to perform calculations. It is
a mere translator from Python expressions into LaTeX syntax. The idea behind it
was I wanted my Python formula to be the same objects as the LaTeX formula I
write in my reports / papers. It allows me to gain time (I can write my LaTeX
formulas directly from the Python expression), and check my Python formulas are correct
(once printed LaTeX is much more readable that a multiline Python expression)

References
----------

Based on a code sample from Geoff Reedy on `StackOverflow <http://stackoverflow.com/questions/3867028/converting-a-python-numeric-expression-to-latex>`__


You may also be interested in the similar development from `BekeJ <https://github.com/BekeJ/py2tex>`__ that was built
on top of the same sample.
BekeJ's code is designed to be used exclusively in an iPython console using
%magic commands to perform unit aware calculations and return result in a nice
LaTeX format.

Sympy also has some nice LaTeX output, but it requires declaring your symbolic
variables and isn't as fast as a one-line console command in pytexit.

Current Features
----------------

Successfully deal with most of the one or two parameter functions. Run the
_test() function to have an idea of what's possible.

Arbitrary syntax:

- Variables named after Greek names are turned into LaTeX syntax

- 'numpy.sin / math.sin / np.sin' syntax still work as expected (all standard
scientific module names are removed beforehand)

- quad() is converted into integrals

- list comprehensions are converted into LaTex syntaX.

- 'a_p' variables are converted with "p" as subscript

Also note that iPython uses auto-completion to convert most of the latex
identifiers in their Unicode equivalent::

    \alpha --> [Tab] --> α

- pytexit will recognize those Unicode characters and convert them again in
latex expressions

- there is a mode to output Python expressions in Word syntax. From version 2007
Word converts most LaTeX expressions in its own graphical representation. The
Word mode here was just about replacing those LaTeX {} with Word ()::

    py2tex('sqrt(5/3)',output='word')


Test
----

In order to enforce cross-version compatibility and non-regression, `pytexit` is
now tested with `pytest` and Travis. Run the test suite locally from a terminal with::

    pip install pytest
    pytest


Changes
-------

- 0.2.1 : full Python 2 support, added automated tests with pytest and Travis

- 0.1.11 : make it reliable: added pytest, Travis, code coverage

- 0.1.8 : fixed console script on Unix systems

- 0.1.4 : partial Python 2 support


Still WIP
---------

Todo:

- allow syntax "a*b = c" (not a valid Python expression, but convenient to type
  some LaTeX formula)

- code for numbered equations

- export all the conversions on an external text file


Links
-----

Github::

    https://github.com/erwanp/pytexit


"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
import ast
import six
try:
    from pytexit.core.core import clean, LatexVisitor, uprint, simplify
    from pytexit.core.docx import WordVisitor
    from pytexit.core.fortran import for2py
except:     # if run locally as a script
    from core.core import clean, LatexVisitor, uprint, simplify
    from core.docx import WordVisitor
    from core.fortran import for2py
try:
    import IPython.display
except:
    pass

def py2tex(expr, print_latex=True, print_formula=True, dummy_var='u', output='tex',
           simplify_output=True, upperscript='ˆ', lowerscript='_', verbose=False,
           simplify_fractions=False, simplify_ints=False):
    ''' Return the LaTeX expression of a Python formula

    Parameters
    ----------
    expr: string
        a Python expression

    print_latex: boolean
        if True, prints the latex expression in the console

    dummy_var: string
        dummy variable displayed in integrals

    output: 'tex' / 'word'
        if 'tex', output latex formula. If word, output a Word MathTex formula
        (may be a little different)

    simplify_output: boolean
        if True, simplify output. Ex: 1x10^-5 --> 10^-5. Default True

    simplify_ints: boolean
        if True, simplify integers. Ex: 1.0 --> 1.  Default False

    simplify_fractions: boolean
        if True, simplify common fractions.  Ex: 0.5 --> 1/2. Default False

    Output
    ------

    returns the latex expression in raw text, to be used in your reports or
    to display in an IPython notebook

    Notes
    -----

    Will return '\\' instead of '\' because we don't want those to be
    interpreted as regular expressions. Use print(result) to get the correct
    LaTex formula.

    See Also
    --------

    :func:`~pytexit.pytexit.for2tex`

    '''

    try:
        if sys.version_info > (3,):
            assert(isinstance(expr, str))
        else:
            assert(isinstance(expr,(str,six.text_type)))
    except AssertionError:
        raise ValueError('Input must be a string')

    expr = clean(expr)  # removes module calls, etc.

    # Parse
    pt = ast.parse(expr)
    if output == 'tex':  # LaTex output
        Visitor = LatexVisitor(dummy_var=dummy_var, upperscript=upperscript,
                               lowerscript=lowerscript, verbose=verbose,
                               simplify=simplify_output,
                               simplify_fractions=simplify_fractions,
                               simplify_ints=simplify_ints)
    elif output == 'word':  # Word output
        Visitor = WordVisitor(dummy_var=dummy_var, upperscript=upperscript,
                              lowerscript=lowerscript, verbose=verbose,
                              simplify=simplify_output)
    else:
        raise ValueError('Unexpected output: {0}'.format(output))
    if isinstance(pt.body[0], ast.Expr):
        # To deal with cases such as 'x=something'
        # TODO : one single command to start the visit?
        s = Visitor.visit(pt.body[0].value)
    else:  # For Compare / Assign expressions
        s = Visitor.visit(pt.body[0])

    # Simplify if asked for
    if simplify_output:
        s = simplify(s)

    if output == 'tex':
        s = '$$' + s + '$$'

    # Output
    if print_latex and output == 'tex':
        try:
            IPython.display.display(IPython.display.Latex(s))
        except:
            pass

    if print_formula:
        uprint(s)
    return s



def for2tex(a, **kwargs):
    ''' Converts FORTRAN formula to Python Formula

    Parameters
    ----------

    a: str
        FORTRAN formula

    Other Parameters
    ----------------

    kwargs: dict
        forwarded to :func:`~pytexit.py2tex` function. See :func:`~pytexit.py2tex`
        doc.

    Examples
    --------

    convert FORTRAN formula to LaTeX with for2tex:

        for2tex(r'2.8d-11 * exp(-(26500 - 0.5 * 1.97 * 11600 )/Tgas)')

    See Also
    --------

    :func:`~pytexit.core.fortran.for2py`, :func:`~pytexit.pytexit.py2tex`

    '''

    from pytexit import py2tex

    return py2tex(for2py(a), **kwargs)



if __name__ == '__main__':

    from test.test_functions import run_all_tests
    uprint('Test =', bool(run_all_tests(True)))
