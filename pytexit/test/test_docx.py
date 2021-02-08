# -*- coding: utf-8 -*-
"""
Created on Tue May  1 12:13:09 2018

@author: erwan
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from pytexit import py2tex
from pytexit.pytexit import uprint

def test_py2tex_wordoutput(verbose=True, **kwargs):
    '''  Convert Python expression to Word readable output
    '''

    # Tests
    expr_py = [r'2*sqrt(2*pi*k*T_e/m_e)*(DeltaE/(k*T_e))**2*a_0**2',
                ]
    
    expr_docx = [r'2\sqrt((2\pi\cdotk\cdotT_(e)/m_(e)))\cdot(((\Delta E/k\cdotT_(e))))^(2)\cdot(a_(0))^(2)']
    
    for i, expr in enumerate(expr_py):
        if verbose: 
            uprint('')
            uprint(u'ˆ')
            uprint(u'Python formula to convert: {0}'.format(expr))
            s = py2tex(expr, output='word')
            uprint('Got:')
            b = (expr_docx[i] == s)
            print(s)
#            uprint('.. correct =', b)
            if not b:
                uprint('Expected Word-readable output:\n', expr_docx[i])
                uprint('\n' * 3)
            assert b
        else:
            s = py2tex(expr, output='word', print_latex=False, print_formula=False)
            assert expr_docx[i] == s

if __name__ == '__main__':
    
    test_py2tex_wordoutput()
    