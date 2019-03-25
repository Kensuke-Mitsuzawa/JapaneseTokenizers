#! -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import sys
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
        import sys
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'kytea'])
        import Mykytea
    except Exception as e:
        logger.error('We failed to install mykytea automatically. Try installing kytea manually.')
        logger.error(e)

# --------------------------------------------------------------------------------------------------------
try:
    import neologdn
except ImportError:
    try:
        import sys
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'neologdn'])
        import neologdn
    except Exception as e:
        logger.error('We failed to install neologdn automatically because of some issues in the package. Try installing pyknp manually.')
        logger.error(e)

# --------------------------------------------------------------------------------------------------------

common_packages = ['pypandoc', 'future', 'six', 'jaconv>=0.2', 'pip>=8.1.0', 'pexpect', 'pyknp>=0.4.1']
if python_version >= (3, 0, 0):
    if python_version <= (3, 5, 0):
        common_packages.append('typing')
    elif python_version > (3, 5, 0):
        common_packages.append('mecab-python3')
elif python_version <= (2, 9, 9):
    common_packages.append('typing')
    common_packages.append('mecab-python')
else:
    raise NotImplementedError()

version = '1.6'
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
    keywords=['MeCab', '和布蕪', 'Juman',
                'Japanese morphological analyzer', 'NLP', '形態素解析', '自然言語処理'],
    license="MIT",
    url = "https://github.com/Kensuke-Mitsuzawa/JapaneseTokenizers",
    test_suite='test.test_all.suite',
    install_requires=common_packages,
    tests_require=common_packages,
    packages=find_packages()
)
