__author__ = 'kensuke-mi'
import sys
import pip
python_version = sys.version_info
with open("requirement.txt") as f:
    for line in f: 
        if 'mecab' in line:
            if python_version < (3, 0, 0): pip.main(['install', line])
            else: pip.main(['install', 'mecab-python3'])
        else:
            pip.main(['install', line.strip()])