# -*- coding: utf-8 -*-
"""
pytexit
----------    
Convert a Python expression in a LaTeX formula

Erwan Pannier
Non Equilibrium Plasma Group - EM2C Laboratory, CentraleSupélec / CNRS UPR 288

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

Use
----------  
    >>> from pytexit import py2tex
    >>> py2tex('x = 2*sqrt(2*pi*k*T_e/m_e)*(DeltaE/(k*T_e))**2*a_0**2')

Current Features
----------    
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


Upperscript formalism
----------    
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


Test
----------    
I haven't deeply tested this module. Please let me know if anything goes wrong.
In particular I tried to make it Python-2 compatible but I'm not sure it's 
actually the case. 


Still WIP
----------    

#TODO:

- make it Python 2 compatible

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
import re
from warnings import warn

try:
    import IPython.display
except:
    pass

unicode = {
    'α':'alpha',
    'β':'beta',
    'χ':'chi',
    'δ':'delta',
    'ε':'epsilon',
    'γ':'gamma',
    'ψ':'psi',
    'θ':'theta',
    'κ':'kappa',
    'λ':'lambda',
    'η':'eta',
    'ν':'nu',
    'π':'pi',
    'ϕ':'phi',
    'σ':'sigma',
    'τ':'tau',
    'ω':'omega',
    'ξ':'xi',
    'Δ':'Delta',
    'φ':'Phi',
#    'Φ':'Phi',
    'Γ':'Gamma',
    'Ψ':'Psi',
    'Λ':'Lambda',
    'Σ':'Sigma',
    'Ξ':'Xi'
    }

# Modules removed from expressions:
clear_modules=['math',
               'np','numpy',
               'scipy.integrate','scipy' # Note that scipy.integrate must be placed before scipy as names are removed in this order
               ] 

class LatexVisitor(ast.NodeVisitor):

    def __init__(self,dummy_var='u',upperscript='ˆ',lowerscript='_',
                 verbose=False):
        super().__init__()
        self.dummy_var = dummy_var
        
        self.upper = upperscript
        self.lower = lowerscript
        
        self.verbose = verbose

    def prec(self, n):
        return getattr(self, 'prec_'+n.__class__.__name__, getattr(self, 'generic_prec'))(n)

    def visit_ListComp(self,n,kwout=False):
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
            if len(comp.iter.args)>1:
                kw['min'] = self.visit(comp.iter.args[0])
                kw['max'] = self.visit(comp.iter.args[1])
            else:
                kw['min'] = 0
                kw['max'] = self.visit(comp.iter.args[0])
            kw['content'] = self.visit(n.elt)
            
        args = r'%s, %s=%s..%s'%(kw['content'],kw['iterator'],kw['min'],kw['max'])

        if kwout:            
            return args, kw
        else:
            return args
        
    def prec_ListComp(self, n):
        return 1000

    def visit_list(self,n):
        self.generic_visit(n)
        
    def prec_list(self, n):
        return 1000

    def visit_Call(self, n):
        ''' Node details : n.args, n.func, n.keywords, n.kwargs'''
        func = self.visit(n.func)
        
        # Deal with list comprehension and complex formats
        blist = isinstance(n.args[0],ast.ListComp)
        
        if blist:
            args, kwargs = self.visit_ListComp(n.args[0],kwout=True)
        else:
            args = ', '.join(map(self.visit, n.args))
        
        
        # Usual math functions
        if func in ['cos','sin','tan',
                    'cosh','sinh','tanh']:
            return '{0}{1}'.format(func,self.parenthesis(args))
        elif func  == 'sqrt':
            return self.sqrt(args)
        elif func in ['log','ln']:  # by default log refers to log10 in Python. Unless people import it as ln
            return r'\ln(%s)' %args
        elif func in ['log10']:
            return r'\log(%s)' %args
        elif func in ['arccos','acos']:
            return r'\arccos(%s)' %args
        elif func in ['arcsin','asin']:
            return r'\arcsin(%s)' %args
        elif func in ['atan','arctan']:
            return r'\arctan(%s)' %args
        elif func in ['arcsinh']:
            return r'\sinh^{-1}(%s)' %args
        elif func in ['arccosh']:
            return r'\cosh^{-1}(%s)' %args
        elif func in ['arctanh']:
            return r'\tanh^{-1}(%s)' %args
        elif func in ['abs','fabs']:
            return r'|%s|' %args
            
        # Additionnal functions (convention names, not in numpy library)
        elif func in ['kronecher','kron']:
            return r'\delta_{%s}' %args
        
        # Integrals
        # TODO : add this integral in a visit_tripOp function???
        elif func in ['quad']:
            (f,a,b) = map(self.visit, n.args)
            return r'\int_{%s}^{%s} %s(%s) d%s' %(a,b,f,self.dummy_var,self.dummy_var)
#                
        # Sum
        elif func in ['sum']:
            if blist:
                return '\sum_{%s=%s}^{%s} %s'%(kwargs['iterator'],kwargs['min'],
                                                kwargs['max'], kwargs['content'])
            else:
                return r'\sum %s' %(args)

        # Recurrent operator names
        elif func in ['f','g','h']:
            return r'%s{\left(%s\right)}' %(func,args)

        else:
            return self.operator(func,args)

    def prec_Call(self, n):
        return 1000

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
        if u>1: 
            if self.verbose: warn('Only one upperscript character supported per identifier')
           
        def build_tree(expr,level=1):     
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
            sep = '[{0}{1}]'.format(self.lower,self.upper)
            s = (re.split(r'(?<!{0})({0}{{{1}}})(?!{0})'.format(sep,level), expr))  # Also returns the pattern n 
            t = {} # build tree
            if self.verbose: uprint('  '*(level-1),'val:',self.convert_symbols(s[0]))
            t['val'] = self.convert_symbols(s[0])
            t['low'] = []
            t['up'] = []
            for i in range(1,len(s),2):
                p = s[i]
                if p == self.lower*level:
                    if self.verbose: uprint('  '*(level-1),'low:',s[i+1])
                    t['low'].append(build_tree(s[i+1],level+1))
                elif p == self.upper*level:
                    if self.verbose: uprint('  '*(level-1),'up:',s[i+1])
                    t['up'].append(build_tree(s[i+1],level+1))
                else:
                    raise ValueError('Undetected separator')
            return t
            
        def read_tree(t):
            ''' Write a LaTeX readable name '''
            r = t['val']
            if t['low']!=[]:
#                child = [self.group(read_tree(tc)) for tc in t['low']]
                child = [read_tree(tc) for tc in t['low']]
                r+='_{0}'.format(self.group(','.join(child)))
            if t['up']!=[]:
#                child = [self.group(read_tree(tc)) for tc in t['up']]
                child = [read_tree(tc) for tc in t['up']]
                r+='^{0}'.format(self.group(','.join(child)))
            return r
            
        return read_tree(build_tree(n.id))
    
    def convert_underscores(self,expr):
        
        s = expr.split(self.lower)
        
        for i,m in enumerate(s):
            s[i] = self.convert_symbols(m)
        
        return s
            

    def convert_symbols(self,expr):
        m = expr        
        
        # Standard greek letters
        if m in ['alpha','beta','gamma','delta','epsilon','zeta','eta','theta',
                    'iota','kappa','mu','nu','xi','pi','rho','sigma',
                    'tau','phi','chi','psi','omega',
                    'Gamma','Delta','Theta','Lambda','Xi','Pi','Sigma','Upsilon',
                    'Phi','Psi','Omega']:
            m = r'\%s'%m
        
        # Unicode
        elif m in unicode:
            m = r'\%s'%unicode[m]
        
        elif m in ['eps']:
            m  = r'\epsilon'
            
        elif m in ['lbd']: # lambda is not a valid identifier in Python so people use other things
            m = r'\lambda'
            
        elif m in ['Lbd']:
            m = r'\Lambda'
            
        elif m in ['inf','infinity','infty']:
            m = r'\infty'
            
        # Replace Delta even if not full word  - Allow for expressions such as ΔE
        elif 'Delta' in m:
            m = m.replace('Delta','\Delta ')
        
        return m

    def prec_Name(self, n):
        return 1000

    def visit_UnaryOp(self, n):
        if self.prec(n.op) > self.prec(n.operand):
            return r'{0} {1}'.format(self.visit(n.op), self.parenthesis(self.visit(n.operand)))
        else:
            return r'{0} {1}'.format(self.visit(n.op), self.visit(n.operand))

    def prec_UnaryOp(self, n):
        return self.prec(n.op)

    def visit_BinOp(self, n):
        if self.prec(n.op) > self.prec(n.left):
            left = self.parenthesis(self.visit(n.left))
        else:
            left = self.visit(n.left)
        if self.prec(n.op) > self.prec(n.right):
            right = self.parenthesis(self.visit(n.right))
        else:
            right = self.visit(n.right)
        
        # Special binary operators
        if isinstance(n.op, ast.Div):
            return self.division(self.visit(n.left), self.visit(n.right))
        elif isinstance(n.op, ast.FloorDiv):
            return r'\left\lfloor\frac{%s}{%s}\right\rfloor' % (self.visit(n.left), self.visit(n.right))
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
            
            if left_is_float & right_is_float:
                return r'{0}\times{1}'.format(left, right)
            elif right_is_float: # revert (a*2 --> 2 a)
                return r'{0}{1}{2}'.format(right, self.visit(n.op), left)
            else: # At least one of the 2 is not an integer
                return r'{0}{1}{2}'.format(left, self.visit(n.op), right)
        else:
            return r'{0}{1}{2}'.format(left, self.visit(n.op), right)

    def prec_BinOp(self, n):
        return self.prec(n.op)

    def visit_Sub(self, n):
        return '-'

    def prec_Sub(self, n):
        return 300

    def visit_Add(self, n):
        return '+'

    def prec_Add(self, n):
        return 300

    def visit_Mult(self, n):
        return r'\,' # reduced space from: r'\;'

    def prec_Mult(self, n):
        return 400

    def visit_Mod(self, n):
        return '\\bmod'

    def prec_Mod(self, n):
        return 500

    def prec_Pow(self, n):
        return 700

    def prec_Div(self, n):
        return 400

    def prec_FloorDiv(self, n):
        return 400

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

    def prec_Invert(self, n):
        return 800

    def visit_Not(self, n):
        return '\\neg'

    def prec_Not(self, n):
        return 800

    def visit_UAdd(self, n):
        return '+'

    def prec_UAdd(self, n):
        return 800

    def visit_USub(self, n):
        return '-'

    def prec_USub(self, n):
        return 800
        
    def visit_Num(self, n):
        return str(n.n)

    def prec_Num(self, n):
        return 1000

    # New visits
    def visit_Assign(self, n):
        ' Rewrite Assign function (instead of executing it)'
        return r'%s=%s'%(self.visit(n.targets[0]),self.visit(n.value))

    def prec_Assign(self, n):
        return 300 # arbitrary ?

    def visit_Compare(self, n):
        ' Rewrite Compare function (instead of executing it)'

        def visit_Op(op):
            ' Note : not called by visit like other visit functions'
            if isinstance(op,ast.Lt):
                return '<'
            elif isinstance(op,ast.LtE):
                return '<='
            elif isinstance(op,ast.Gt):
                return '>'
            elif isinstance(op,ast.GtE):
                return '>='
            elif isinstance(op,ast.Eq):
                return '='
            else:
                raise ValueError('Unknown comparator',op.__class__)
            
        return r'%s%s'%(self.visit(n.left),''.join(['%s%s'%(visit_Op(n.ops[i]),
                self.visit(n.comparators[i])) for i in range(len(n.comparators))]))

    def prec_Compare(self, n):
        return 300 # arbitrary ?

    # Default
    def generic_visit(self, n):
        if isinstance(n, ast.AST):
            return r'' % (n.__class__.__name__, ', '.join(map(self.visit, [getattr(n, f) for f in n._fields])))
        else:
            return str(n)

    def generic_prec(self, n):
        return 0

    # LaTeX blocs
    def group(self,expr):
        return r'{{{0}}}'.format(expr)

    def parenthesis(self,expr):
        return r'\left({0}\right)'.format(expr)

    def power(self,expr,power):
        return r'{0}^{1}'.format(expr, self.group(power))

    def division(self,up,down):
        return r'\frac{0}{1}'.format(self.group(up), self.group(down))

    def sqrt(self,args):
         return r'\sqrt{0}'.format(self.group(args))

    def operator(self,func,args=None):
        if args is None:
            return r'\operatorname{{{0}}}'.format(func)
        else:
            return r'\operatorname{{{0}}}\left({1}\right)'.format(func, args)

class WordVisitor(LatexVisitor):
    ''' A variant of the LatexVisitor to create Word readable equations '''

    # Word-readable blocks
    def group(self,expr):
        'Word will convert unnecessary parenthesis in equivalent LaTeX {} groups'
        return self.parenthesis(expr)

    def parenthesis(self,expr):
        'No spacing'
        return '({0})'.format(expr)
    
    def power(self,expr,power):
        'no { }'
        return r'{0}^{1}'.format(expr, power)

    def division(self,up,down):
        'no frac' 
        return r'({0}/{1})'.format(up, down)

    def visit_Mult(self,n):
        'No spacing'
        return r''
    
    def sqrt(self,args):
        return r'\sqrt({0})'.format(args)

    def operator(self,func,args=None):
        if args is None:
            return r'{0}'.format(func)
        else:
            return r'{0}({1})'.format(func, args)

def clean(expr):
    ''' Removes unnessary calls to libraries'''
    
    for m in clear_modules:
        expr = expr.replace(m+'.','')
    
    return expr

def py2tex(expr,print_latex=True,print_formula=True,dummy_var='u',output='tex',
           upperscript='ˆ',lowerscript='_',verbose=False):
    ''' Return the LaTeX expression of a Python formula 
    Note. Will return '\\' instead of '\' because we don't want those to be 
    interpreted as regular expressions. Use print(result) to get the correct
    LaTex formula. 

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
    
    Output
    ----------    
    - returns the latex expression in raw text, to be used in your reports or 
    to display in an IPython notebook
    '''

    try:
        assert(isinstance(expr, str))
    except AssertionError:
        raise ValueError('Input must be a string')
    
    expr=clean(expr) # removes module calls, etc.

    # Parse 
    pt = ast.parse(expr)
    if output == 'tex':
        Visitor = LatexVisitor(dummy_var=dummy_var,upperscript=upperscript,
                               lowerscript=lowerscript,verbose=verbose)
    elif output == 'word':
        Visitor = WordVisitor(dummy_var=dummy_var,upperscript=upperscript,
                              lowerscript=lowerscript,verbose=verbose)
    if isinstance(pt.body[0],ast.Expr): 
        # To deal with cases such as 'x=something' 
        # TODO : one single command to start the visit?
        s = Visitor.visit(pt.body[0].value)
    else: # For Compare / Assign expressions
        s = Visitor.visit(pt.body[0])        
        
    if output == 'tex':
        s = '$$'+s+'$$'    
    
    # Output
    if print_latex and output=='tex': 
        try:
            IPython.display.display(IPython.display.Latex(s))
        except:
            pass
    
    if print_formula:
        uprint(s)
    return s
    
def uprint(*expr, sep=' ', end='\n', file=sys.stdout):
    ''' Deals with encoding problems '''
    
    try:
        print(*expr, sep=sep, end=end, file=file)
    except UnicodeEncodeError:
        f = lambda expr: expr.encode(sys.stdout.encoding, errors='replace')
        print(*map(f, expr), sep=sep, end=end, file=file)

def _test(verbose=True,**kwargs):
    ''' 
    Note : for debugging use 
        pt = ast.parse(expr)
        print(ast.dump(pt))
    ''' 
    
    expr_py = [r'Re_x=(rho*v*x)/mu',
                r'2*sqrt(2*pi*k*T_e/m_e)*(DeltaE/(k*T_e))**2*a_0**2',
                r'f(x**2/y**3)',
                r'arctanh(x/sqrt(x))',
                r'quad(f,0,np.inf)',
                r'2*4',
                r'1<2<a<=5',
                r'np.std([f(i) for i in range(20)])',
                r'np.sum([i**2 for i in range(1,100)])==328350',
                r'k_i__1_i__2ˆj__1ˆj__2',
                ]
    expr_tex = [r'$$Re_{x}=\frac{\rho\,v\,x}{\mu}$$',
                r"$$2\,\sqrt{\frac{2\,\pi\,k\,T_{e}}{m_{e}}}\,\left(\frac{\Delta E}{k\,T_{e}}\right)^{2}\,a_{0}^{2}$$",
                r"$$f{\left(\frac{x^{2}}{y^{3}}\right)}$$",
                r"$$\tanh^{-1}(\frac{x}{\sqrt{x}})$$",
                r"$$\int_{0}^{\infty} f(u) du$$",
                r'$$2\times4$$',
                r'$$1<2<a<=5$$',
                r'$$\operatorname{std}\left(f{\left(i\right)}, i=0..20\right)$$',
                r'$$\sum_{i=1}^{100} i^{2}=328350$$',
                r'$$k_{i_{1},i_{2}}^{j_{1},j_{2}}$$',
                ]

    
    btest = True
    for i,expr in enumerate(expr_py):
        if verbose: 
            uprint('')
            uprint(u'ˆ')
            uprint(u'Python formula to convert: {0}'.format(expr))
            s = py2tex(expr)
            uprint('Got:')
            b = (expr_tex[i]==s)
#            print(s)
            uprint('.. correct =',b)
            if not b: 
                uprint('Expected:\n',expr_tex[i])
                uprint('\n'*3)
        else:
            s = py2tex(expr,print_latex=False,print_formula=False)
            b = (expr_tex[i]==s)
        btest *= b         
    
    return btest
    
if __name__ == '__main__':
    uprint('Test =',bool(_test(True)))