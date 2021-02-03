# -*- coding: utf-8 -*-
"""
Test pytextit 
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import sys
from pytexit import py2tex
from pytexit.pytexit import uprint, simplify

def test_py2tex(verbose=True, **kwargs):
    ''' 
    Note : for debugging use 
        pt = ast.parse(expr)
        print(ast.dump(pt))
    '''

    # Tests
    expr_py = [r'Re_x=(rho*v*x)/mu',
                r'2*sqrt(2*pi*k*T_e/m_e)*(DeltaE/(k*T_e))**2*a_0**2',
                r'f(x**2/y**3)',
                r'arctanh(x/sqrt(x))',
                r'quad(f,0,np.inf)',
                r'2*4',
                r'1<2<a<=5',
                r'np.std([f(i) for i in range(20)])',
                r'np.sum([i**2 for i in range(1,100)])==328350',
                r'theta = w_k * a ** 4 / t ** 4 / E + 2'
                ]
    
    expr_tex = [r'$$Re_x=\frac{\rho v x}{\mu}$$',
                r"$$2\sqrt{\frac{2\pi k T_e}{m_e}} \left(\frac{\Delta E}{k T_e}\right)^2 a_0^2$$",
                r"$$f{\left(\frac{x^2}{y^3}\right)}$$",
                r"$$\tanh^{-1}(\frac{x}{\sqrt{x}})$$",
                r"$$\int_{0}^{\infty} f(u) du$$",
                r'$$2\times4$$',
                r'$$1<2<a<=5$$',
                r'$$\operatorname{std}\left(f{\left(i\right)}, i=0..20\right)$$',
                r'$$\sum_{i=1}^{100} i^2=328350$$',
                r'$$\theta=\frac{a^{4} w_{k}}{E t^{4}}+2$$'
                ]
    
    for i, expr in enumerate(expr_py):
        if verbose:
            uprint('')
            uprint(u'ˆ')
            uprint(u'Python formula to convert: {0}'.format(expr))
            s = py2tex(expr)
            uprint('Got:')
            b = (expr_tex[i] == s)
            print(s)
#            uprint('.. correct =', b)
            if not b:
                uprint('Expected:\n', expr_tex[i])
                uprint('\n' * 3)
            assert b
        else:
            s = py2tex(expr, print_latex=False, print_formula=False)
            assert expr_tex[i] == s

    return True

def test_py2tex_py3only(verbose=True, **kwargs):
    ''' Some tests valid with Python 3 syntax only (Ex: unicodes: ˆ)'''
    
    if sys.version_info[0] != 3:
        if verbose: print('Not Python 3. Ignoring test_py2tex_py3only')
        return
    
    # Tests
    expr_py = [r'k_i__1_i__2ˆj__1ˆj__2',
               ]
    
    expr_tex = [r'$$k_{i_1,i_2}^{j_1,j_2}$$',
                ]
    
    for i, expr in enumerate(expr_py):
        if verbose:
            uprint('')
            uprint(u'ˆ')
            uprint(u'Python formula to convert: {0}'.format(expr))
            s = py2tex(expr)
            uprint('Got:')
            b = (expr_tex[i] == s)
            print(s)
#            uprint('.. correct =', b)
            if not b:
                uprint('Expected:\n', expr_tex[i])
                uprint('\n' * 3)
            assert b
        else:
            s = py2tex(expr, print_latex=False, print_formula=False)
            assert expr_tex[i] == s

    
    

def test_simplify(verbose=True, **kwargs):
    
    assert simplify('1e-20*11e2') == r'10^{-20}*11\times10^2'
    assert simplify('1e-20*11e-20+5+2') == r'10^{-20}*11\times10^{-20}+5+2'

def run_all_tests(verbose=True, **kwargs):
    
    test_py2tex(verbose=verbose, **kwargs)
    test_py2tex_py3only(verbose=verbose, **kwargs)
    test_simplify(verbose=verbose, **kwargs)

if __name__ == '__main__':
    run_all_tests(verbose=True)
    
    