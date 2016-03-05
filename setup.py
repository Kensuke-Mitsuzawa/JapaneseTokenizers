#! -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import sys
import install_python_dependencies
python_version = sys.version_info


if python_version >= (3, 0, 0):
    install_requires = ['mecab-python3', 'jctconv']
else:
    install_requires = ['mecab-python', 'jctconv']

setup(
    author='Kensuke Mitsuzawa',
    name = 'JapaneseTokenizer',
    version='0.6',
    license = "MIT",
    url = "https://github.com/Kensuke-Mitsuzawa/JapaneseTokenizers",
    test_suite='JapaneseTokenizer.test.test_all.suite',
    install_requires = install_requires,
    packages=find_packages(),
    )

