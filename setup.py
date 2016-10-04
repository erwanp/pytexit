from setuptools import setup
import os
import codecs

long_description = 'Convert a Python expression in a LaTeX formula'
if os.path.exists('README.rst'):
    long_description = codecs.open('README.rst', encoding="utf-8").read()

setup(name='pytexit',
      version='0.1.8',
      description='Convert a Python expression in a LaTeX formula',
      long_description=long_description,
      url='https://github.com/erwanp/pytexit',
      author='Erwan Pannier',
      author_email='erwan.pannier@gmail.com',
      license='CeCILL-2.1',
      packages=['pytexit'],
      platforms="any",
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
      install_requires=[],
      scripts=[
          'scripts/py2tex'],
      include_package_data=True,
      zip_safe=False)
