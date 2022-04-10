
============================================
`pytexit <https://pytexit.readthedocs.io>`__
============================================

Convert a Python expression to a LaTeX formula


.. image:: https://img.shields.io/pypi/v/pytexit.svg
    :target: https://pypi.python.org/pypi/pytexit
    :alt: PyPI

.. image:: https://img.shields.io/travis/erwanp/pytexit.svg
    :target: https://travis-ci.com/erwanp/pytexit
    :alt: Tests

.. image:: https://codecov.io/gh/erwanp/pytexit/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/erwanp/pytexit
    :alt: Coverage


Documentation
-------------

https://pytexit.readthedocs.io


.. image:: https://readthedocs.org/projects/pytexit/badge/
    :target: https://pytexit.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


Install
-------

``pytexit`` is on PyPi::

    pip install pytexit


Use
---

``pytexit`` features the ``py2tex``, ``for2tex`` ``for2py`` functions.

In a Terminal, use ``py2tex``::

    py2tex 'x = 2*sqrt(2*pi*k*T_e/m_e)*(DeltaE/(k*T_e))**2*a_0**2'

In a Python console, use ``py2tex``::

    from pytexit import py2tex
    py2tex('x = 2*sqrt(2*pi*k*T_e/m_e)*(DeltaE/(k*T_e))**2*a_0**2')

returns the corresponding LaTeX formula (to re-use in papers)::

    $$x=2\\sqrt{\\frac{2\\pi k T_e}{m_e}} \\left(\\frac{\\Delta E}{k T_e}\\right)^2 a_0^2$$

and (in ipython console only) prints the equation:

.. image:: https://github.com/erwanp/pytexit/blob/master/docs/output.png



References
----------

Initial work from Geoff Reedy on StackOverflow: https://stackoverflow.com/a/3874621/5622825  . Kudos.

Similar projects:

- https://github.com/iogf/lax  : "A pythonic way of writting latex."
- https://github.com/JelteF/PyLaTeX : "A Python library for creating LaTeX files"
- sympy can also write LaTeX output.
