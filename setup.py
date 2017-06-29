#! -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import sys
import pip
import logging
import codecs
logger = logging.getLogger(__file__)

python_version = sys.version_info

# --------------------------------------------------------------------------------------------------------
# try to install kytea automatically because it usually causes to error during installing
try:
    import Mykytea
except ImportError:
    try:
        pip.main(['install', 'kytea'])
    except:
        logger.error('We failed to install mykytea automatically. Try installing kytea manually.')

    try:
        import Mykytea
    except ImportError:
        logger.error('We failed to install mykytea automatically. Try installing kytea manually.')

# --------------------------------------------------------------------------------------------------------
# try to install pyknp automatically because it usually causes to error during installing
try:
    import pyknp
except ImportError:
    try:
        pip.main(['install', 'http://nlp.ist.i.kyoto-u.ac.jp/DLcounter/lime.cgi?down=http://lotus.kuee.kyoto-u.ac.jp/nl-resource/pyknp/pyknp-0.3.tar.gz&name=pyknp-0.3.tar.gz'])
    except:
        logger.error('We failed to install pyknp automatically. Try installing pyknp manually.')

    try:
        import pyknp
    except ImportError:
        logger.error('We failed to install pyknp automatically. Try installing pyknp manually.')
# --------------------------------------------------------------------------------------------------------

if python_version >= (3, 0, 0):
    logger.info(msg='python={}'.format(python_version))
    install_requires = ['pypandoc', 'future', 'six', 'mecab-python3', 'jaconv>=0.2', 'pip>=8.1.0', 'typing', 'neologdn', 'pexpect']
else:
    logger.info(msg='python={}'.format(python_version))
    install_requires = ['pypandoc', 'future', 'six', 'mecab-python', 'jaconv>=0.2', 'pip>=8.1.0', 'typing', 'neologdn', 'pexpect']

version = '1.3.1'
name = 'JapaneseTokenizer'
short_description = '`JapaneseTokenizer` is a package for easy Japanese Tokenization'

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = codecs.open('README.md', 'r', 'utf-8').read()

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
    author_email='kensuke.mit@gmail.com',
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
    packages=find_packages()
)
