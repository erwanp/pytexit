# -*- coding: utf-8 -*-
"""
Parser and core Routines
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import re
import ast
from warnings import warn
from six.moves import range
from six.moves import map

unicode_tbl = {
    'α': 'alpha',
    'β': 'beta',
    'χ': 'chi',
    'δ': 'delta',
    'ε': 'epsilon',
    'γ': 'gamma',
    'ψ': 'psi',
    'θ': 'theta',
    'κ': 'kappa',
    'λ': 'lambda',
    'η': 'eta',
    'ν': 'nu',
    'π': 'pi',
    'ϕ': 'phi',
    'σ': 'sigma',
    'τ': 'tau',
    'ω': 'omega',
    'ξ': 'xi',
    'Δ': 'Delta',
    'φ': 'Phi',
    #    'Φ':'Phi',
    'Γ': 'Gamma',
    'Ψ': 'Psi',
    'Λ': 'Lambda',
    'Σ': 'Sigma',
    'Ξ': 'Xi'
}

fracs = {
    0.5: ['', 1, 2],
    -0.5: ['-', 1, 2],
    0.75: ['', 3, 4],
    -0.75: ['-', 3, 4],
    0.25: ['', 1, 4],
    -0.25: ['-', 1, 4]
}

# Modules removed from expressions:
clear_modules = ['math',
                 'np', 'numpy',
                 # Note that scipy.integrate must be placed before scipy as
                 # names are removed in this order
                 'scipy.integrate', 'scipy',
                 'df',  # not a module, but useful to clear pandas dataframe for readability
                 ]

# % Printing & encoding


def uprint(*expr):
    ''' Deals with encoding problems '''

    try:
        print(*expr)
    except UnicodeEncodeError:
        f = lambda expr: expr.encode(sys.stdout.encoding, errors='replace')
        print(*list(map(f, expr)))




class LatexVisitor(ast.NodeVisitor):
    ''' 
    Parameters
    ----------
    
    simplify_multipliers: bool
        if ``True``, simplify expression if multiplier is a float. Ex::
            
            2*a -> 2a 
            
            a * 3.5 -> 3.5 
            
        see :meth:`~pytexit.core.core.LatexVisitor.visit_BinOp` for more 
        information. Default ``True``.
    
    simplify_fractions: bool
        if ``True``, simplify fractions. 
        see :meth:`~pytexit.core.core.LatexVisitor.visit_BinOp` for more 
        information. Default ``False``.
        
    simplify_ints: bool
        see :meth:`~pytexit.core.core.LatexVisitor.visit_BinOp` for more 
        information. Default ``False``.
        
    '''
    
    def __init__(self, dummy_var='u', upperscript='ˆ', lowerscript='_',
                 verbose=False, simplify_multipliers=True, simplify_fractions=False,
                 simplify_ints=False):
        
        super(LatexVisitor, self).__init__()
        # super().__init__()  # doesn't work in Python 2.x
        self.dummy_var = dummy_var

        self.upper = upperscript
        self.lower = lowerscript

        self.verbose = verbose
        self.simplify_multipliers = simplify_multipliers
        self.simplify_fractions = simplify_fractions
        self.simplify_ints = simplify_ints

        self.precdic = {"Pow": 700,
                        "Div": 400,
                        "FloorDiv": 400,
                        "Mult": 400,
                        "Invert": 800,
                        "Compare": 300,
                        "Uadd": 800,
                        "Not": 800,
                        "USub": 800,
                        "Num": 1000,
                        "Constant": 1000,
                        "Assign": 300,
                        "Sub": 300,
                        "Add": 300,
                        "Mod": 500,
                        "ListComp": 1000,
                        "list": 1000,
                        "Call": 1000,
                        "Name": 1000
                        }

    def looks_like_int(self, a):
        """ Check if the input ``a`` looks like an integer """
        if self.simplify_ints:
            if not isinstance(a, str):
                a = str(a)
            try:
                value = float(a.split('.')[1]) == 0.0
            except (IndexError, ValueError):
                value = False
            return value
        else:
            return False

    def prec(self, n):
        if n.__class__.__name__ in self.precdic:
            return self.precdic[n.__class__.__name__]
        else:
            return getattr(self, 'prec_' + n.__class__.__name__, getattr(self, 'generic_prec'))(n)        

    def visit_ListComp(self, n, kwout=False):
        ''' Analyse a list comprehension
        Output :
        - kw : used by some functions to display nice formulas (e.g : sum)
        - args : standard output to display a range in other cases
        '''

        kw = {}

#        lc = n.args[0]
        comp = n.generators[0]
        kw['iterator'] = self.visit(comp.target)
        f = self.visit(comp.iter.func)

        if f == 'range':
            if len(comp.iter.args) > 1:
                kw['min'] = self.visit(comp.iter.args[0])
                kw['max'] = self.visit(comp.iter.args[1])
            else:
                kw['min'] = 0
                kw['max'] = self.visit(comp.iter.args[0])
            # Remove 1 for range max 
            try:
                kw['max'] = int(kw['max'])-1
            except ValueError:
                if kw['max'].endswith(r'+1'):
                    # write 'sum([... range(N+1)])' as (sum^N)
                    kw['max'] = kw['max'][:-2]
                else:
                    # write 'sum([... range(N)])' as (sum^N-1)
                    kw['max'] = r'{0}-1'.format(kw['max'])
            kw['content'] = self.visit(n.elt)

        args = r'%s, %s=%s..%s' % (
            kw['content'], kw['iterator'], kw['min'], kw['max'])

        if kwout:
            return args, kw
        else:
            return args

    def visit_list(self, n):
        self.generic_visit(n)

    def visit_Call(self, n):
        ''' Node details : n.args, n.func, n.keywords, n.kwargs'''
        func = self.visit(n.func)

        # Deal with list comprehension and complex formats
        if len(n.args)>0:
            blist = isinstance(n.args[0], ast.ListComp)
        else:
            blist = False

        if blist:
            args, kwargs = self.visit_ListComp(n.args[0], kwout=True)
        else:
            args = ', '.join(map(self.visit, n.args))

        # Usual math functions
        if func in ['cos', 'sin', 'tan',
                    'cosh', 'sinh', 'tanh']:
            return '{0}{1}'.format(func, self.parenthesis(args))
        elif func == 'sqrt':
            return self.sqrt(args)
        # by default log refers to log10 in Python. Unless people import it as
        # ln
        elif func in ['log', 'ln']:
            return r'\ln(%s)' % args
        elif func in ['log10']:
            return r'\log(%s)' % args
        elif func in ['arccos', 'acos']:
            return r'\arccos(%s)' % args
        elif func in ['arcsin', 'asin']:
            return r'\arcsin(%s)' % args
        elif func in ['atan', 'arctan']:
            return r'\arctan(%s)' % args
        elif func in ['arcsinh']:
            return r'\sinh^{-1}(%s)' % args
        elif func in ['arccosh']:
            return r'\cosh^{-1}(%s)' % args
        elif func in ['arctanh']:
            return r'\tanh^{-1}(%s)' % args
        elif func in ['power']:
            args = args.split(',')
            return self.power(self.parenthesis(args[0]), args[1])
        elif func in ['divide']:
            args = args.split(',')
            return self.division(args[0], args[1])
        elif func in ['abs', 'fabs']:
            return r'|%s|' % args

        # Additionnal functions (convention names, not in numpy library)
        elif func in ['kronecher', 'kron']:
            return r'\delta_{%s}' % args

        # Integrals
        # TODO : add this integral in a visit_tripOp function???
        elif func in ['quad']:
            (f,a,b) = list(map(self.visit, n.args))
            return r'\int_{%s}^{%s} %s(%s) d%s' %(a,b,f,self.dummy_var,self.dummy_var)
#
        # Sum
        elif func in ['sum']:
            if blist:
                return '\sum_{%s=%s}^{%s} %s' % (kwargs['iterator'], kwargs['min'],
                                                 kwargs['max'], kwargs['content'])
            else:
                return r'\sum %s' % (args)

        # Recurrent operator names
        elif func in ['f', 'g', 'h']:
            return r'%s{\left(%s\right)}' % (func, args)

        else:
            return self.operator(func, args)

    def visit_Name(self, n):
        ''' Special features:
        - Recognize underscripts in identifiers names (default: underscore)
        - Recognize upperscripts in identifiers names (default: ˆ, valid in Python3)
        Note that using ˆ is not recommanded in variable names because it may
        be confused with the operator ^, but in some special cases of extensively
        long formulas with lots of indices, it may help the readability of the
        code
        '''

        u = n.id.count(self.upper)
        if u > 1:
            if self.verbose:
                warn('Only one upperscript character supported per identifier')

        def build_tree(expr, level=1):
            ''' Builds a tree out of a valid Python identifier, according to the
            following proposed formalism:

            Formalism
            ----------
                Python -> Real

                k_i_j  -> k_i,j
                k_i__j -> k_(i_j)
                k_iˆj -> k_i^j
                k_iˆˆj -> k_(i^j)
                k_i__1_i__2ˆj__1ˆˆj__2 -> k_(i_1,i_2)^(j_1,j_2)

            Even if one may agree that this last expression isn't a very
            readable variable name.

            The idea behind this is that I want my Python formula to be the
            same objects as the LaTeX formula I write in my reports / papers

            It allows me to:
            - gain time
            - check my Python formula (once printed LaTeX is much more readable
            that a multiline Python expression)

            '''

#            sep0 = '[{0}][{1}]'.format(self.lower,self.upper)
            sep = '[{0}{1}]'.format(self.lower, self.upper)
            s = (re.split(r'(?<!{0})({0}{{{1}}})(?!{0})'.format(
                sep, level), expr))  # Also returns the pattern n
            t = {}  # build tree
            if self.verbose:
                uprint('  ' * (level - 1), 'val:', self.convert_symbols(s[0]))
            t['val'] = self.convert_symbols(s[0])
            t['low'] = []
            t['up'] = []
            for i in range(1, len(s), 2):
                p = s[i]
                if p == self.lower * level:
                    if self.verbose:
                        uprint('  ' * (level - 1), 'low:', s[i + 1])
                    t['low'].append(build_tree(s[i + 1], level + 1))
                elif p == self.upper * level:
                    if self.verbose:
                        uprint('  ' * (level - 1), 'up:', s[i + 1])
                    t['up'].append(build_tree(s[i + 1], level + 1))
                else:
                    raise ValueError('Undetected separator')
            return t

        def read_tree(t):
            ''' Write a LaTeX readable name '''
            r = t['val']
            if t['low'] != []:
                #                child = [self.group(read_tree(tc)) for tc in t['low']]
                child = [read_tree(tc) for tc in t['low']]
                r += '_{0}'.format(self.group(','.join(child)))
            if t['up'] != []:
                #                child = [self.group(read_tree(tc)) for tc in t['up']]
                child = [read_tree(tc) for tc in t['up']]
                r += '^{0}'.format(self.group(','.join(child)))
            return r

        return read_tree(build_tree(n.id))

#    def convert_underscores(self, expr):
#
#        s = expr.split(self.lower)
#
#        for i, m in enumerate(s):
#            s[i] = self.convert_symbols(m)
#
#        return s

    def convert_symbols(self, expr):
        m = expr
        # Standard greek letters
        if m in ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta',
                 'iota', 'kappa', 'mu', 'nu', 'xi', 'pi', 'rho', 'sigma',
                 'tau', 'phi', 'chi', 'psi', 'omega',
                 'Gamma', 'Delta', 'Theta', 'Lambda', 'Xi', 'Pi', 'Sigma', 'Upsilon',
                 'Phi', 'Psi', 'Omega']:
            m = r'\%s' % m

        # Unicode
#        elif m in unicode_tbl:
#            m = r'\%s' % unicode_tbl[m]
        # @EP: unicode is now removed in pre-processing, before Parsing begins.

        elif m in ['eps']:
            m = r'\epsilon'

        elif m in ['lbd']:  # lambda is not a valid identifier in Python so people use other things
            m = r'\lambda'

        elif m in ['Lbd']:
            m = r'\Lambda'

        elif m in ['inf', 'infinity', 'infty']:
            m = r'\infty'

        # Replace Delta even if not full word  - Allow for expressions such as
        # ΔE
        elif 'Delta' in m:
            m = m.replace('Delta', '\Delta ')

        return m

    def visit_UnaryOp(self, n):
        # Note: removed space between {0} and {1}... so that 10**-3 yields
        # $$10^{-3}$$ and not $$10^{- 3}$$

        if self.prec(n.op) > self.prec(n.operand):
            return r'{0}{1}'.format(self.visit(n.op),
                                    self.parenthesis(self.visit(n.operand)))
        else:
            return r'{0}{1}'.format(self.visit(n.op), self.visit(n.operand))

    def prec_UnaryOp(self, n):
        return self.prec(n.op)

    def visit_BinOp(self, n):
    
        if self.prec(n.op) > self.prec(n.left):
            left = self.parenthesis(self.visit(n.left))
        elif isinstance(n.op, ast.Pow) and self.prec(n.op) == self.prec(n.left):
            # Special case for power, which needs parentheses when combined to the left
            left = self.parenthesis(self.visit(n.left))
        else:
            left = self.visit(n.left)
        if self.prec(n.op) > self.prec(n.right):
            right = self.parenthesis(self.visit(n.right))
        else:
            right = self.visit(n.right)
 
        # Special binary operators
        if isinstance(n.op, ast.Div):
            if self.simplify_fractions:
                left_is_int = self.looks_like_int(left)
                right_is_int = self.looks_like_int(right)
                if left_is_int or right_is_int:
                    if left_is_int and right_is_int:
                        return self.division('%d' % int(float(left)),
                                             '%d' % int(float(right)))
                    elif left_is_int:
                        return self.division('%d' % int(float(left)),
                                             self.visit(n.right))
                    else:
                        return self.division(self.visit(n.left),
                                             '%d' % int(float(right)))
            return self.division(self.visit(n.left), self.visit(n.right))
        elif isinstance(n.op, ast.FloorDiv):
            return r'\left\lfloor\frac{%s}{%s}\right\rfloor' % \
                (self.visit(n.left), self.visit(n.right))
        elif isinstance(n.op, ast.Pow):
            return self.power(left, self.visit(n.right))
        elif isinstance(n.op, ast.Mult):

            def looks_like_float(a):
                ''' Care for the special case of 2 floats/integer
                We don't want 'a*2' where we could have simply written '2a' '''
                try:
                    float(a)
                    return True
                except ValueError:
                    return False

            left_is_float = looks_like_float(left)
            right_is_float = looks_like_float(right)

            # Get multiplication operator. Force x if floats are involved
            if left_is_float or right_is_float:
                operator = r'\times'
            else: # get standard Mult operator (see visit_Mult)
                operator = self.visit(n.op)

            if self.simplify_multipliers:
                
                # We simplify in some cases, for instance: a*2 -> 2a
                # First we need to know if both terms start with numbers
                if left[0] == '-':
                    left_starts_with_digit = left[1].isdigit()
                else:
                    left_starts_with_digit = left[0].isdigit()
                    
                if right[0] == '-':
                    right_starts_with_digit = right[1].isdigit()
                else:
                    right_starts_with_digit = right[0].isdigit()

                # Simplify
                # ... simplify (a*2 --> 2a)
                if right_is_float and not left_starts_with_digit: 
                    return r'{0}{1}'.format(right, left)
                # ... simplify (2*a --> 2a)
                elif left_is_float and not right_starts_with_digit:
                    return r'{0}{1}'.format(left, right)
                else:
                    return r'{0}{1}{2}'.format(left, operator, right)
            else:
                return r'{0}{1}{2}'.format(left, operator, right)
        else:
            return r'{0}{1}{2}'.format(left, self.visit(n.op), right)

    def prec_BinOp(self, n):
        return self.prec(n.op)

    def visit_Sub(self, n):
        return '-'

    def visit_Add(self, n):
        return '+'

    def visit_Mult(self, n):
#        return r'\cdot'   # no space in LaTeX (before:   r'\;'   )
        return r' '   # no space in LaTeX (before:   r'\;'   )

    def visit_Mod(self, n):
        return '\\bmod'

    def visit_LShift(self, n):
        return self.operator('shiftLeft')

    def visit_RShift(self, n):
        return self.operator('shiftRight')

    def visit_BitOr(self, n):
        return self.operator('or')

    def visit_BitXor(self, n):
        return self.operator('xor')

    def visit_BitAnd(self, n):
        return self.operator('and')

    def visit_Invert(self, n):
        return self.operator('invert')

    def visit_Not(self, n):
        return '\\neg'

    def visit_UAdd(self, n):
        return '+'

    def visit_USub(self, n):
        return '-'

    def visit_Num(self, n):
        if self.simplify_fractions:
            if any([n.n == key for key in fracs.keys()]):
                string = r'{0}\frac{{{1}}}{{{2}}}'.format(*fracs[n.n])
                return string
        if self.looks_like_int(n.n):
            return '%d' % n.n
        return str(n.n)

    # New visits
    def visit_Assign(self, n):
        ' Rewrite Assign function (instead of executing it)'
        return r'%s=%s' % (self.visit(n.targets[0]), self.visit(n.value))

    def visit_Compare(self, n):
        ' Rewrite Compare function (instead of executing it)'

        def visit_Op(op):
            ' Note : not called by visit like other visit functions'
            if isinstance(op, ast.Lt):
                return '<'
            elif isinstance(op, ast.LtE):
                return '<='
            elif isinstance(op, ast.Gt):
                return '>'
            elif isinstance(op, ast.GtE):
                return '>='
            elif isinstance(op, ast.Eq):
                return '='
            else:
                raise ValueError('Unknown comparator', op.__class__)

        return r'%s%s' % (self.visit(n.left), ''.join(['%s%s' % (visit_Op(n.ops[i]),
                                                                 self.visit(n.comparators[i])) for i in range(len(n.comparators))]))

    # Default
    def generic_visit(self, n):
        if isinstance(n, ast.AST):
            return r'' % (n.__class__.__name__, ', '.join(map(self.visit, [getattr(n, f) for f in n._fields])))
        else:
            return str(n)

    def generic_prec(self, n):
        return 0

    # LaTeX blocs
    def brackets(self, expr):
        ''' Enclose expr in {...} '''
        return r'{{{0}}}'.format(expr)

    def group(self,expr):
        ''' Returns expr, add brackets if needed'''
        if len(expr)==1:
            return expr
        else:
            return self.brackets(expr)

    def parenthesis(self,expr):
        return r'\left({0}\right)'.format(expr)

    def power(self, expr, power):
        return r'{0}^{1}'.format(self.group(expr), self.group(power))

    def division(self,up,down):
        return r'\frac{0}{1}'.format(self.brackets(up), self.brackets(down))

    def sqrt(self,args):
         return r'\sqrt{0}'.format(self.brackets(args))

    def operator(self, func, args=None):
        if args is None:
            return r'\operatorname{{{0}}}'.format(func)
        else:
            return r'\operatorname{{{0}}}\left({1}\right)'.format(func, args)

def preprocessing(expr):
    ''' Pre-process a string. In particular:
        
    - replace unicode values (so that even a Python 2 pytexit can parse formula
      with unicode, valid in Python 3 only)
    - clean: remove calls to librairies
    '''
    
    expr = replace_unicode(expr)
    expr = clean(expr)

    return expr

def replace_unicode(expr):
    
    for u in unicode_tbl:
        expr = expr.replace(u, unicode_tbl[u])
        
    return expr

def clean(expr):
    ''' Removes unnessary calls to libraries

    Examples
    --------

        np.exp(-3) would be read exp(-3)
    '''

    expr = expr.strip()  # remove spaces on the side

    for m in clear_modules:
        # Todo: some regexp here. re(<(+- */)). To make sure we're not removing
        # a variable name
        expr = expr.replace(m + '.', '')

    return expr


def simplify(s):
    ''' Cleans the generated text in post-processing '''

    # Remove unecessary parenthesis?
    # -------------
    # TODO: look for groups that looks like \(\([\(.+\)]*\)\ ),
    # (2 pairs of external parenthesis around any number (even 0) of closed pairs
    # of parenthesis)  -> then remove one of the the two external parenthesis
    # TRied with re.findall(r'\(\([^\(^\)]*(\([^\(^\)]+\))*[^\(^\)]*\)\)', s)  but
    # it doesnt work. One should better try to look for inner pairs and remove that
    # one after one..
    
    # Replace '\left(NUMBER\right)' with 'NUMBER'
    # ------------
    s = re.sub(r"\\left\(([\d\.]+)\\right\)", r"\1", s)

    # Improve readability:


    # Replace 'NUMBER e NUMBER' with powers of 10
    # ------------
    regexp = re.compile(r'(\d*\.{0,1}\d+)[e]([-+]?\d*\.{0,1}\d+)')

    matches = regexp.findall(s)
    splits = regexp.split(s)
    assert len(splits) == (len(matches) + 1) + (2 * len(matches))
    #                     splitted groups             prefactor, exponent

    new_s = ''
    # loop over all match and replace
    # ... I didnt find any better way to do that given that we want a conditional
    # ... replace (.sub wouldnt work)
    for i, (prefactor, exponent) in enumerate(matches):
        new_s += splits[3*i]

        if len(exponent) == 1:
            exp_str = r'{0}'.format(exponent)
        else:
            exp_str = r'{'+'{0}'.format(exponent)+'}'

        if prefactor == '1':
            new_s += r'10^{0}'.format(exp_str)
        else:
            new_s += r'{0}\times10^{1}'.format(prefactor, exp_str)
    if len(splits) % 3 == 1:  # add last ones
        new_s += splits[-1]
    s = new_s

    return s
