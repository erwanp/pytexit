# -*- coding: utf-8 -*-
'''Automatically generate a README.rst for Pypi from my README.md, and publish
the latest version

Use
------------
    python register.py

Requirement
------------
    pandoc
    
'''

from __future__ import print_function, absolute_import
import os
import shutil

package_name = 'pytexit'

# All the rest below is standard:
os.system('python setup.py sdist')
os.system('python setup.py bdist_wheel --universal')
os.system("twine upload dist/*")
# Clean
shutil.rmtree('dist')

print('All done')
