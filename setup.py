from __future__ import absolute_import
from setuptools import setup, find_packages
import os
import io
import codecs
from os.path import join, dirname, abspath, exists
from setuptips import yield_sphinx_only_markup

# Build description from README (PyPi compatible)
# (note: README.rst has been converted to README.md by register.py, and cleaned afterwards )
readme_path = join(abspath(dirname(__file__)), 'README.md')
if not exists(readme_path):
    long_description = description
else:
    with io.open(readme_path, encoding='utf-8') as f:
        long_description = f.read()
    
# Read version number from file
with open(join(dirname(__file__),'pytexit', '__version__.txt')) as version_file:
    __version__ = version_file.read().strip()

setup(name='pytexit',
      version=__version__,
      description='Convert a Python expression to a LaTeX formula',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='http://pytexit.readthedocs.io/',
      author='Erwan Pannier',
      author_email='erwan.pannier@gmail.com',
      license='CeCILL-2.1',
      packages=find_packages(),
      platforms="any",
      keywords=["latex", "py2tex"],
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)',
        'Topic :: Scientific/Engineering',
        'Topic :: Text Processing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        "Operating System :: OS Independent"],
      install_requires=[
                 'six',  # python 2-3 compatibility],
                 ],
      scripts=[
          'scripts/py2tex'],
      include_package_data=True,
      zip_safe=False)
