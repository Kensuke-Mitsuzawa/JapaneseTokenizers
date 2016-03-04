#! -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import install_python_dependencies

install_requires = ['mecab-python']

setup(
    author='Kensuke Mitsuzawa',
    name = 'JapaneseTokenizer',
    version='0.5',
    test_suite='JapaneseTokenizer.test.test_all.suite',
    install_requires = install_requires,
    packages=find_packages(),
    )

