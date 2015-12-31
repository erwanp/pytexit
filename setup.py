from setuptools import setup
import os
import codecs

long_description = 'Convert a Python expression in a LaTeX formula'
if os.path.exists('README.rst'):
    long_description = codecs.open('README.rst').read()
    
setup(name='pytexit',
      version='0.1.3',
      description='Convert a Python expression in a LaTeX formula',
	long_description=long_description,
      url='https://github.com/rainwear/pytexit',
      author='Erwan Pannier',
      author_email='erwan.pannier@gmail.com',
      license='BSD-3',
      packages=['pytexit'],
      install_requires=[],
      scripts=[
          'scripts/py2tex'],
	include_package_data=True,
      zip_safe=False)