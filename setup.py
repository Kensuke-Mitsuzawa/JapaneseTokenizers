#! -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import sys
import install_python_dependencies
import pypandoc
python_version = sys.version_info


if python_version >= (3, 0, 0):
    install_requires = ['mecab-python3', 'jctconv']
else:
    install_requires = ['mecab-python', 'jctconv']

version = '0.6a1'
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
    keywords = ['MeCab', '和布蕪', 'Japanese morphological analyzer', 'NLP', '形態素解析', '自然言語処理'],
    license = "MIT",
    url = "https://github.com/Kensuke-Mitsuzawa/JapaneseTokenizers",
    test_suite='JapaneseTokenizer.test.test_all.suite',
    install_requires = install_requires,
    packages=find_packages(),
    )

