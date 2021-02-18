# -*- coding: utf-8 -*-
"""Automatically generate a README.rst for Pypi from my README.md, and publish
the latest version

Use
------------
    python register.py

Requirement
------------
    pandoc
    
"""

from __future__ import absolute_import, print_function

import os
import shutil

package_name = "pytexit"
try:
    # Convert readme to Markdown format
    os.system("pandoc README.rst -o README.md")
    os.system("python setup.py sdist")
    os.system("python setup.py bdist_wheel --universal")
    os.system("twine check dist/*")
    os.system("twine upload dist/*")
finally:
    # Clean
    os.remove("README.md")
    shutil.rmtree("dist")
