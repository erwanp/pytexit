
.. image:: https://img.shields.io/pypi/v/pytexit.svg
    :target: https://pypi.python.org/pypi/pytexit
    :alt: PyPI

.. image:: https://img.shields.io/travis/erwanp/pytexit.svg
    :target: https://travis-ci.org/erwanp/pytexit
    :alt: Tests
    
.. image:: https://codecov.io/gh/erwanp/pytexit/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/erwanp/pytexit
    :alt: Coverage
  
=======
pytexit
=======

Description
-----------

Convert a Python expression in a LaTeX formula

Github::

    https://github.com/erwanp/pytexit

This module isn't unit aware and isn't designed to perform calculations. It is 
a mere translator from Python expressions into LaTeX syntax. The idea behind it
was I wanted my Python formula to be the same objects as the LaTeX formula I 
write in my reports / papers. It allows me to:

- gain time: 
    I can write my LaTeX formulas directly from the Python expression
    
- check my Python formulas are correct:
    once printed LaTeX is much more readable that a multiline Python expression

This is my one of my first released modules, I'll be pleased to have any advice or 
feedback, mostly concerning cross-platform compatibility issues.

References
----------

Based on a code sample from Geoff Reedy on [StackOverflow](http://stackoverflow.com/questions/3867028/converting-a-python-numeric-expression-to-latex
)

You may also be interested in the similar development from [BekeJ](
https://github.com/BekeJ/py2tex) that was built
on top of the same sample. 
BekeJ's code is designed to be used exclusively in an iPython console using 
%magic commands to perform unit aware calculations and return result in a nice
LaTeX format. 

Sympy also has some nice LaTeX output, but it requires declaring your symbolic
variables and isn't as fast as a one-line console command in pytexit.

Install
-------

`pytexit` is on PyPi::

    pip install pytexit

    
Use
---

In a Python console::

    from pytexit import py2tex
    py2tex('x = 2*sqrt(2*pi*k*T_e/m_e)*(DeltaE/(k*T_e))**2*a_0**2')

    
Will display the following equation:

.. image:: https://github.com/erwanp/pytexit/blob/master/docs/output.png

And the corresponding LaTeX formula::

    $$x=2\\sqrt{\\frac{2\\pi k T_e}{m_e}} \\left(\\frac{\\Delta E}{k T_e}\\right)^2 a_0^2$$

You may also use it directly from a terminal::

    py2tex 'x = 2*sqrt(2*pi*k*T_e/m_e)*(DeltaE/(k*T_e))**2*a_0**2'


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


Upperscript formalism
---------------------

(experimental)

Python3 allows you to use almost every Unicode character as a valid identifier
for a variable. For instance all the following characters are valid: 
`αβχδεφγψιθκλνηοπϕστωξℂΔΦΓΨΛΣℚℝΞ`

Also, `ˆ` [chr(710)] is a valid Python3 identifier (`^` isn't). Although I 
wouldn't call it recommended, I find it convenient to name some of my variables 
with `ˆ`, such as `α_iˆj` (mostly because I want a direct Python -> LaTeX 
translation). The py2tex function is aware of this and will perform the 
following conversion:

Python -> Real::

    k_i_j  -> k_i,j
    k_i__j -> k_(i_j) 
    k_iˆj -> k_i^j
    k_iˆˆj -> k_(i^j)
    k_i__1_i__2ˆj__1ˆˆj__2 -> k_(i_1,i_2)^(j_1,j_2)
    
etc. `k_i__j___1` is still a valid expression, although it quickly starts to be 
unreadable.


Test
----

In order to enforce cross-version compatibility and non-regression, `pytexit` is 
now tested with `pytest` and Travis. Run the test suite locally from a terminal with::

    pip install pytest 
    pytest 


Changes
-------

- 0.1.11 : make it reliable: added pytest, Travis, code coverage

- 0.1.8 : fixed console script on Unix systems

- 0.1.4 : partial Python 2 support


Still WIP
---------

Todo:

- make it fully Python 2 compatible

- allow syntax "a*b = c" (not a valid Python expression, but convenient to type 
  some LaTeX formula)
    
- code for numbered equations

- export all the conversions on an external text file 
    
*Erwan Pannier*
