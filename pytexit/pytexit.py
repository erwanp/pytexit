# -*- coding: utf-8 -*-
"""
pytexit
----------    
Convert a Python expression in a LaTeX formula

Erwan Pannier

Based on a code sample from Geoff Reedy at 
http://stackoverflow.com/questions/3867028/converting-a-python-numeric-expression-to-latex

You may also be interested in the similar development from Beke,J that was built
on top of the same sample:
https://github.com/BekeJ/py2tex
BekeJ's code is designed to be used exclusively in an iPython console using 
%magic commands to perform unit aware calculations and return result in a nice
LaTeX format. 

This module isn't unit aware and isn't designed to perform calculations. It is 
a mere translator from Python expressions into LaTeX syntax. The idea behind it
was I wanted my Python formula to be the same objects as the LaTeX formula I 
write in my reports / papers. It allows me to:

- gain time
    I can write my LaTeX formulas directly from the Python expression
    
- check my Python formulas are correct
    once printed LaTeX is much more readable that a multiline Python expression

Examples
--------
  
    >>> from pytexit import py2tex
    >>> py2tex('x = 2*sqrt(2*pi*k*T_e/m_e)*(DeltaE/(k*T_e))**2*a_0**2')

Notes
-----

Current Features:
    
Successfully deal with most of the one or two parameter functions. Run the 
_test() function to have an idea of what's possible. 

Arbitrary syntax:
- Variables named after greek names are turned into LaTeX syntax
- 'numpy.sin / math.sin / np.sin' syntax still work as expected (all standard 
scientific module names are removed beforehand)
- quad() is converted into integrals
- list comprehensions are converted into LaTex syntaX. 
- 'a_p' variables are converted with "p" as subscript

Also note that iPython uses auto-completion to convert most of the latex 
identifiers in their unicode equivalent:

    >>> \alpha --> [Tab] --> α
    
- pytexit will recognize those unicode characters and convert them again in 
latex expressions
- there is a mode to output Python expressions in Word syntax. From version 2007
Word converts most LaTeX expressions in its own graphical representation. The 
Word mode here was just about replacing those LaTeX {} with Word ().
    
    >>> py2tex('sqrt(5/3)',output='word')


Upperscript formalism:

Python3 allows you to use almost every unicode character as a valid identifier
for a variable. For instance all the following characters are valid:

    >>> 'αβχδεφγψιθκλνηοπϕστωξℂΔΦΓΨΛΣℚℝΞ'

Also, 'ˆ' [chr(710)] is a valid Python3 identifier (^ isn't). Although I 
wouldn't call it recommanded, I find it convenient to name some of my variables 
with ˆ, such as α_iˆj (mostly because I want a direct Python -> LaTeX 
translation). The py2tex code below is aware of this and will perform the 
following conversion:

    Python -> Real
    
    >>> k_i_j  -> k_i,j
    >>> k_i__j -> k_(i_j) 
    >>> k_iˆj -> k_i^j
    >>> k_iˆˆj -> k_(i^j)
    >>> k_i__1_i__2ˆj__1ˆˆj__2 -> k_(i_1,i_2)^(j_1,j_2)

etc. k_i__j___1 is still a valid expression, although it quickly starts to be 
unreadable.


Tests:
    
I haven't deeply tested this module. Please let me know if anything goes wrong.
In particular I tried to make it Python-2 compatible but I'm not sure it's 
actually the case. 


Still WIP
----------    

#TODO:

- make it fully Python 2 compatible

- allow syntax "a*b = c" (not a valid Python expression, but convenient to type
    some LaTeX formula)
    
- code for numbered equations

- export all the conversions on an external text file 
    
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
           simplify_output=True, upperscript='ˆ', lowerscript='_', verbose=False):
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

    Output
    ------
    
    returns the latex expression in raw text, to be used in your reports or 
    to display in an IPython notebook
    
    Notes
    -----
    
    Will return '\\' instead of '\' because we don't want those to be 
    interpreted as regular expressions. Use print(result) to get the correct
    LaTex formula. 

    
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
    if output == 'tex':
        Visitor = LatexVisitor(dummy_var=dummy_var, upperscript=upperscript,
                               lowerscript=lowerscript, verbose=verbose)
    elif output == 'word':
        Visitor = WordVisitor(dummy_var=dummy_var, upperscript=upperscript,
                              lowerscript=lowerscript, verbose=verbose)
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

if __name__ == '__main__':
    
    from test.test_functions import run_all_tests
    uprint('Test =', bool(run_all_tests(True)))
    
