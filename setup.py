#! -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import sys

install_requires = []

try:
    import MeCab
    mecabObj = MeCab.Tagger('-Ochasen')
    text = u'本日は晴天なり'.encode('utf-8')
    node = mecabObj.parseToNode(text)
    node = node.next
    while node.next is not None:
        word_surface = node.surface.decode('utf-8')
        node = node.next
except Exception as e:
    print e
    sys.exit("Mecab and Mecab-python is not ready to use. Please setup first")


setup(
    author='Kensuke Mitsuzawa',
    name = 'JapaneseTokenizer',
    version='0.1',
    test_suite='test_all.suite',
    install_requires = install_requires,
    packages=find_packages(),
    )

