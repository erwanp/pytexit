from setuptools import setup
import os

long_description = 'Convert a Python expression in a LaTeX formula'
if os.path.exists('README.txt'):
    long_description = open('README.txt').read()
    
setup(name='pytexit',
      version='0.1.0',
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