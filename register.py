# -*- coding: utf-8 -*-
'''Automatically generate a README.rst for Pypi from my README.md

Requirement
------------
    pandoc
    
'''

import os


if os.path.exists('README.rst'):
    os.remove('README.rst')

os.system('pandoc -s README.md --from markdown --to rst -s -o README.rst')

if os.path.exists('README.rst'):
    print('Readme generated')
    os.system("setup.py register sdist upload")
    os.remove('README.rst')
