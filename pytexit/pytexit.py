# -*- coding: utf-8 -*-
"""

Convert a Python expression in a LaTeX formula

"""

from __future__ import absolute_import, division, print_function, unicode_literals

import ast
import sys
import six

try:
    from pytexit.core.core import LatexVisitor, preprocessing, simplify, uprint, replace_scientific
    from pytexit.core.docx import WordVisitor
    from pytexit.core.fortran import for2py
except:  # if run locally as a script
    from core.core import LatexVisitor, preprocessing, simplify, uprint, replace_scientific
    from core.docx import WordVisitor
    from core.fortran import for2py
try:
    import IPython.display
except:
    pass


def py2tex(
    expr,
    print_latex=True,
    print_formula=True,
    dummy_var="u",
    output="tex",
    tex_enclosure="$$",
    tex_multiplier=r"\times",
    simplify_output=True,
    upperscript="ˆ",
    lowerscript="_",
    verbose=False,
    simplify_fractions=False,
    simplify_ints=True,
    simplify_multipliers=True,
):
    """Return the LaTeX expression of a Python formula

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

    tex_enclosure: string
        enclosure for latex formula.

        Default: "$$""

    tex_multiplier: raw string
        multiplication operator for latex formula.

        r'\times':   2*2 -> 2 x 2 (Default)
        r'{\times}': 2*2 -> 2x2
        r'\cdot':    2*2 -> 2 · 2
        r'{\cdot}':  2*2 -> 2·2

    Other Parameters
    ----------------

    simplify_output: boolean
        if ``True``, simplify output. Ex::

            1x10^-5 --> 10^-5

        See :func:`~pytexit.core.core.simplify` for more information.
        Default ``True``

    simplify_ints: boolean
        if ``True``, simplify integers (useful for Python 2 expressions). Ex::

            1. --> 1

        See :class:`~pytexit.core.core.LatexVisitor` for more information.
        Default ``True``

    simplify_fractions: boolean
        if ``True``, simplify common fractions.  Ex::

            0.5 --> 1/2

        See :class:`~pytexit.core.core.LatexVisitor` for more information.
        Default ``False``

    simplify_multipliers: boolean
        if ``True``, simplify float multipliers during parsing. Ex::

            2*a  -> 2a

        See :class:`~pytexit.core.core.LatexVisitor` for more information.
        Default ``True``


    Returns
    -------

    returns the latex expression in raw text, to be used in your reports or
    to display in an IPython notebook

    Notes
    -----

    Will return ``'\\\\'`` instead of ``'\\'`` because we don't want those to be
    interpreted as regular expressions. Use ``print(result)`` to get the correct
    LaTex formula.

    See Also
    --------

    :func:`~pytexit.pytexit.for2tex`

    References
    ----------

    Initial work from Geoff Reedy on StackOverflow: https://stackoverflow.com/a/3874621/5622825 . Kudos.

    Similar projects:

    - https://github.com/iogf/lax  : "A pythonic way of writting latex."
    - https://github.com/JelteF/PyLaTeX : "A Python library for creating LaTeX files"
    - sympy can also write LaTeX output.

    """

    # Check inputs
    try:
        if sys.version_info > (3,):
            assert isinstance(expr, str)
        else:
            assert isinstance(expr, (str, six.text_type))
    except AssertionError:
        raise ValueError("Input must be a string")

    expr = preprocessing(expr, simplify_output)  # removes unicode, module calls, etc.

    # replace scientific notation with power of 10 (this needs to be done in
    # preprocessing since the ast parser will replace 1e3 with 1000.0)
    if simplify_output:
        expr = replace_scientific(expr)

    # Parse
    pt = ast.parse(expr)
    if output == "tex":  # LaTex output
        Visitor = LatexVisitor(
            dummy_var=dummy_var,
            upperscript=upperscript,
            lowerscript=lowerscript,
            verbose=verbose,
            simplify_multipliers=simplify_multipliers,
            simplify_fractions=simplify_fractions,
            simplify_ints=simplify_ints,
            tex_multiplier=tex_multiplier,
        )
    elif output == "word":  # Word output
        Visitor = WordVisitor(
            dummy_var=dummy_var,
            upperscript=upperscript,
            lowerscript=lowerscript,
            verbose=verbose,
            simplify_multipliers=simplify_multipliers,
            simplify_fractions=simplify_fractions,
            simplify_ints=simplify_ints,
            tex_multiplier=tex_multiplier,
        )
    else:
        raise ValueError("Unexpected output: {0}".format(output))
    if isinstance(pt.body[0], ast.Expr):
        # To deal with cases such as 'x=something'
        # TODO : one single command to start the visit?
        s = Visitor.visit(pt.body[0].value)
    else:  # For Compare / Assign expressions
        s = Visitor.visit(pt.body[0])

    # Simplify if asked for
    if simplify_output:
        s = simplify(s)

    if output == "tex":
        s = tex_enclosure + s + tex_enclosure

    # Output
    if print_latex and output == "tex":
        try:
            IPython.display.display(IPython.display.Latex(s))
        except:
            pass

    if print_formula:
        uprint(s)
    return s


def for2tex(a, **kwargs):
    """Converts FORTRAN formula to Python Formula

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

    convert FORTRAN formula to LaTeX with for2tex::

        for2tex(r'2.8d-11 * exp(-(26500 - 0.5 * 1.97 * 11600 )/Tgas)')

    See Also
    --------

    :func:`~pytexit.core.fortran.for2py`, :func:`~pytexit.pytexit.py2tex`

    """

    from pytexit import py2tex

    return py2tex(for2py(a), **kwargs)


if __name__ == "__main__":

    from test.test_functions import run_all_tests

    uprint("Test completed: ", bool(run_all_tests(True)))
