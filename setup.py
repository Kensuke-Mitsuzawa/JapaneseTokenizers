#! -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import JapaneseTokenizer.mecab_wrapper.mecab_wrapper as mecab_wrapper
import sys
from JapaneseTokenizer import __version__
import install_python_dependencies

python_version = sys.version_info


install_requires = ['mecab-python']

try:
    import MeCab
    mecabObj = MeCab.Tagger('-Ochasen')
    if python_version >= (3, 0, 0):
        text = '本日は晴天なり'
    else:
        text = u'本日は晴天なり'.encode('utf-8')
    node = mecabObj.parseToNode(text)
    node = node.next
    while node.next is not None:
        if python_version >= (3, 0, 0):
            word_surface = node.surface
        else:
            word_surface = node.surface.decode('utf-8')
        node = node.next
except Exception as e:
    print(e)
    sys.exit("Mecab and Mecab-python is not ready to use. Please setup first")


setup(
    author='Kensuke Mitsuzawa',
    name = 'JapaneseTokenizer',
    version=__version__,
    test_suite='JapaneseTokenizer.test.test_all.suite',
    install_requires = install_requires,
    packages=find_packages(),
    )

