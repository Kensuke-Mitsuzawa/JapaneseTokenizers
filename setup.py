#! -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import sys

python_version = sys.version_info


# check required libraries
try:
    import jctconv
    import pypandoc
    import pyknp
except:
    # install them if any of them is not installed
    import install_python_dependencies

if python_version >= (3, 0, 0):
    install_requires = ['future', 'six', 'mecab-python3', 'jctconv==0.1.2', 'pyknp']
    dependency_links = []
else:
    install_requires = ['future', 'six', 'mecab-python', 'jctconv==0.1.2', 'pyknp']
    dependency_links = ['https://mecab.googlecode.com/files/mecab-python-0.996.tar.gz']

version = '1.0'
name = 'JapaneseTokenizer'
short_description = '`JapaneseTokenizer` is a package for easy Japanese Tokenization'

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

classifiers = [
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Natural Language :: Japanese",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5"
        ]

setup(
    author='Kensuke Mitsuzawa',
    name = name,
    version=version,
    short_description=short_description,
    long_description=long_description,
    keywords = ['MeCab', '和布蕪', 'Juman',
                'Japanese morphological analyzer', 'NLP', '形態素解析', '自然言語処理'],
    license = "MIT",
    url = "https://github.com/Kensuke-Mitsuzawa/JapaneseTokenizers",
    test_suite='test.test_all.suite',
    install_requires = install_requires,
    dependency_links=dependency_links,
    packages=find_packages(),
    )

