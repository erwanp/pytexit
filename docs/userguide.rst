
Convert a Python expression to a LaTeX formula

Install
-------

``pytexit`` is on PyPi::

    pip install pytexit


Use
---

``pytexit`` features the :func:`~pytexit.pytexit.py2tex`, :func:`~pytexit.pytexit.for2tex`
and :func:`~pytexit.core.fortran.for2py` functions.

In a Terminal, use ``py2tex``::

    py2tex 'x = 2*sqrt(2*pi*k*T_e/m_e)*(DeltaE/(k*T_e))**2*a_0**2'

In a Python console, use :func:`~pytexit.pytexit.py2tex`::

    from pytexit import py2tex
    py2tex('x = 2*sqrt(2*pi*k*T_e/m_e)*(DeltaE/(k*T_e))**2*a_0**2')

returns the corresponding LaTeX formula (to re-use in papers)::

    $$x=2\\sqrt{\\frac{2\\pi k T_e}{m_e}} \\left(\\frac{\\Delta E}{k T_e}\\right)^2 a_0^2$$

and (in ipython console only) prints the equation:

.. image:: output.png

Current Features
----------------

Successfully deal with most of the one or two parameter functions. Run the
_test() function to have an idea of what's possible.

Arbitrary syntax:

- Variables named after Greek names are turned into LaTeX syntax::

    py2tex("Re_x=(rho*v*x)/mu")

.. math::
    Re_x=\frac{\rho v x}{\mu}


- 'numpy.sin / math.sin / np.sin' syntax still work as expected (all standard
  scientific module names are removed beforehand)::

    py2tex('numpy.arccos(x)')

.. math::
    \\arccos(x)

- quad() is converted into integrals::

    py2tex("quad(f,0,np.inf)")

.. math::
        \int_{0}^{\infty} f(u) du

- list comprehensions are converted into LaTex syntaX::

    py2tex("np.sum([i**2 for i in range(1,101)])==338350")

.. math::
    \sum_{i=1}^{100} i^2=338350

- ``a_subˆsuper`` variables are converted with "sub" as subscript and "super" as superscript::

    py2tex('a_subˆsuper')

.. math::
    a_{sub}^{super}

Note that "ˆ" is the circumflex accent instead of the caret sign "^", and is a valid Python variable name::

   a_iˆj=1      # valid in Python3

- complex sub/superscript such as second order sub/superscript and comma are supported::

    py2tex('k_i__1_i__2ˆj__1ˆj__2')

.. math::
    k_{i_1,i_2}^{j_1,j_2}

  More detailed rules::

        python -> latex
        k_i_j  -> k_i,j
        k_i__j -> k_(i_j)
        k_iˆj -> k_i^j
        k_iˆˆj -> k_(i^j)
        k_i__1_i__2ˆj__1ˆˆj__2 -> k_(i_1,i_2)^(j_1,j_2)


Also note that iPython uses auto-completion to convert most of the latex
identifiers in their Unicode equivalent::

    \alpha --> [press Tab] --> α

- pytexit will recognize those Unicode characters and convert them again in
  latex expressions::

    py2tex('arcsin(α)')

.. math::
    \arcsin(\alpha)

.. list-table:: Supported Unicode Characters
   :widths: 25 25 50
   :header-rows: 1

   * - Character
     - Name
     - As chr()
   * - α
     - alpha
     - chr(945)
   * - β
     - beta
     - chr(946)
   * - χ
     - chi
     - chr(967)
   * - δ
     - delta
     - chr(916)
   * - ÷
     - division
     - chr(247)
   * - ε
     - epsilon
     - chr(949)
   * - γ
     - gamma
     - chr(947)
   * - ψ
     - psi
     - chr(968)
   * - θ
     - theta
     - chr(952)
   * - κ
     - kappa
     - chr(954)
   * - λ
     - lambda
     - chr(955)
   * - lambda
     - lambda
     - chr(955)
   * - η
     - eta
     - chr(951)
   * - ν
     - nu
     - chr(957)
   * - π
     - pi
     - chr(960)
   * - ϕ
     - phi
     - chr(981)
   * - σ
     - omega
     - chr(963)
   * - τ
     - tau
     - chr(964)
   * - ω
     - omega
     - chr(969)
   * - ξ
     - xi
     - chr(958)
   * - Δ
     - Delta
     - chr(916)
   * - φ
     - Phi
     - chr(966)
   * - Γ
     - Gamma
     - chr(915)
   * - Ψ
     - Psi
     - chr(936)
   * - α
     - alpha
     - chr(945)
   * - Λ
     - Lambda
     - chr(923)
   * - Σ
     - Sigma
     - chr(931)
   * - Ξ
     - Xi
     - chr(926)

- there is a mode to output Python expressions in Word syntax. From version 2007
  Word converts most LaTeX expressions in its own graphical representation. The
  Word mode here was just about replacing those LaTeX {} with Word ()::

    py2tex('sqrt(5/3)',output='word')

Notes
-----

This module isn't unit aware and isn't designed to perform calculations. It is
a mere translator from Python expressions into LaTeX syntax. The idea behind it
was I wanted my Python formula to be the same objects as the LaTeX formula I
write in my reports / papers. It allows me to gain time (I can write my LaTeX
formulas directly from the Python expression), and check my Python formulas are correct
(once printed LaTeX is much more readable that a multiline Python expression)


``pytexit`` can also convert FORTRAN formulas to Python (:func:`~pytexit.core.fortran.for2py`)
and LaTeX (:func:`~pytexit.pytexit.for2tex`)::

	from pytexit import for2tex
	for2tex(r'2.8d-11 * exp(-(26500 - 0.5 * 1.97 * 11600 )/Tgas)')

Finally, ``pytexit`` output can be made compatible with Word equation editor with
the ``output='word'`` option of :func:`~pytexit.pytexit.py2tex`::

	from pytexit import py2tex
	py2tex(r'2*sqrt(2*pi*k*T_e/m_e)*(DeltaE/(k*T_e))**2*a_0**2', output='word')

The latest output will typically replace all brackets {} with parenthesis () that are correctly
interpreted by Word, and keep keywords that are correctly evaluated by Word (`\pi` or `\cdot`)

By default, you have the option to enable/diable printing the given formula or the LaTeX, by passing your
preferences as parameters to the ``pytexit.py2tex``::
    
    from pytexit import py2tex
    py2tex(r'4*sqrt(2*pi*R)',print_formula = False,print_latex = True)

You can also set them globaly by changing ``pytexit.PRINT_FORMULA`` or ``pytexit.PRINT_LATEX``. their values determine
what will happen when you don't override them when calling the function. For Example::
    
    import pytexit
    pytexit.py2tex(r'x=1.0d-2') # both formula and LaTeX will be printed 
    pytexit.py2tex(r'4*sqrt(2*pi*R)',print_formula = False,print_latex = True) # only LaTeX will be printed

    pytexit.PRINT_FORMULA, pytexit.PRINT_LATEX = True, False
    pytexit.py2tex(r'a=3.2d0+3d1') # only formula will be printed
    pytexit.py2text(r'2*sqrt(2*pi*k*T_e/m_e)*(DeltaE/(k*T_e))**2*a_0**2',print_formula = False) # nothing will be printed


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

