# pytexit

*Erwan Pannier - Non Eq. Plasma Group - EM2C Laboratory, CentraleSupélec / CNRS UPR 288*

## Description

Convert a Python expression in a LaTeX formula

[Project Github page](https://github.com/rainwear/pytexit)

Based on a code sample from Geoff Reedy on [StackOverflow](http://stackoverflow.com/questions/3867028/converting-a-python-numeric-expression-to-latex
)

You may also be interested in the similar development from [BekeJ](
https://github.com/BekeJ/py2tex) that was built
on top of the same sample. 
BekeJ's code is designed to be used exclusively in an iPython console using 
%magic commands to perform unit aware calculations and return result in a nice
LaTeX format. 

This module isn't unit aware and isn't designed to perform calculations. It is 
a mere translator from Python expressions into LaTeX syntax. The idea behind it
was I wanted my Python formula to be the same objects as the LaTeX formula I 
write in my reports / papers. It allows me to:

- gain time: 
    I can write my LaTeX formulas directly from the Python expression
    
- check my Python formulas are correct:
    once printed LaTeX is much more readable that a multiline Python expression

## Install

```
pip install pytexit
```
    
## Use

```
from pytexit import py2tex
py2tex('x = 2*sqrt(2*pi*k*T_e/m_e)*(DeltaE/(k*T_e))**2*a_0**2')
```

Will display the following equation:

![https://github.com/rainwear/pytexit/blob/master/docs/output.png](docs/output.png)

And the corresponding LaTeX formula:
```
$$x=2\,\sqrt{\frac{2\,\pi\,k\,T_{e}}{m_{e}}}\,\left(\frac{\Delta E}{k\,T_{e}}\right)^{2}\,a_{0}^{2}$$
```

You may also use it directly from the console:

```
py2tex 'x = 2*sqrt(2*pi*k*T_e/m_e)*(DeltaE/(k*T_e))**2*a_0**2'
```

## Current Features

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

```
\alpha --> [Tab] --> α
```
    
- pytexit will recognize those unicode characters and convert them again in 
latex expressions

- there is a mode to output Python expressions in Word syntax. From version 2007
Word converts most LaTeX expressions in its own graphical representation. The 
Word mode here was just about replacing those LaTeX {} with Word ().

```    
py2tex('sqrt(5/3)',output='word')
```

## Upperscript formalism

Python3 allows you to use almost every unicode character as a valid identifier
for a variable. For instance all the following characters are valid: 
`αβχδεφγψιθκλνηοπϕστωξℂΔΦΓΨΛΣℚℝΞ`

Also, `ˆ` [chr(710)] is a valid Python3 identifier (`^` isn't). Although I 
wouldn't call it recommanded, I find it convenient to name some of my variables 
with `ˆ`, such as α_iˆj (mostly because I want a direct Python -> LaTeX 
translation). The py2tex code below is aware of this and will perform the 
following conversion:

```
Python -> Real

k_i_j  -> k_i,j
k_i__j -> k_(i_j) 
k_iˆj -> k_i^j
k_iˆˆj -> k_(i^j)
k_i__1_i__2ˆj__1ˆˆj__2 -> k_(i_1,i_2)^(j_1,j_2)
```
    
etc. k_i__j___1 is still a valid expression, although it quickly starts to be 
unreadable.


## Test

I haven't deeply tested this module. Please let me know if anything goes wrong.
From version 0.1.4 Python 2.7 should also work, even if some encoding problems
may happen in the console mode, and special unicode characters cannot be used
as valid identifiers. 


## Changes

- 0.1.4 : partial Python 2 support


## Still WIP

Todo:

- make it fully Python 2 compatible

- allow syntax "a*b = c" (not a valid Python expression, but convenient to type
    some LaTeX formula)
    
- code for numbered equations

- export all the conversions on an external text file 
    