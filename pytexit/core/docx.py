# -*- coding: utf-8 -*-
"""
Tools to deal with Word equations format


See Also
--------

if working with Word and Python, you may be interested in the python-docx 
package although equations are not yet supported.

"""

from .core import LatexVisitor

class WordVisitor(LatexVisitor):
    ''' A variant of the LatexVisitor to create Word readable equations 
    (to be inserted in Word equation tool)
    
    See Also
    --------
    
    if working with Word and Python, you may be interested in the python-docx 
    package although equations are not yet supported.
    
    '''

    # Word-readable blocks
    def group(self, expr):
        'Word will convert unnecessary parenthesis in equivalent LaTeX {} groups'
        return self.parenthesis(expr)

    def parenthesis(self, expr):
        'No spacing'
        return '({0})'.format(expr)

#    def power(self, expr, power):
#        'no { }'
#        return r'{0}^{1}'.format(expr, power)

    def division(self, up, down):
        'no frac'
        return r'({0}/{1})'.format(up, down)

    def visit_Mult(self, n):
        'No spacing'
        return r'\cdot'
#        return r''

    def sqrt(self, args):
        return r'\sqrt({0})'.format(args)

    def operator(self, func, args=None):
        if args is None:
            return r'{0}'.format(func)
        else:
            return r'{0}({1})'.format(func, args)

