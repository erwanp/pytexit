# -*- coding: utf-8 -*-
"""
Tools to work with FORTRAN formula
"""

import re

def for2py(a):
    
    ''' Converts FORTRAN formula to Python Formula
    
    Examples
    --------
    
    convert FORTRAN formula to LaTeX with py2tex:
    
        py2tex(for2py($FORTRAN_FORMULA))
    
    '''
    
    # Replace Fortran double (ex: 1.0d-2) with Python format (ex: 1.0e-2)
    regexp = re.compile(r'(\d*\.\d+)[dD]([-+]?\d+)')
    a = regexp.sub(r'\1e\2', a)
    
    return a


if __name__ == '__main__':
    
    examples = ['1.0d-2']
    
    for a in examples:
        print('{0} converted from Fortran to Python: {1}'.format(a, for2py(a)))