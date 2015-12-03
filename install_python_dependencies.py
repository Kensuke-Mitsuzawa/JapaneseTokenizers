__author__ = 'kensuke-mi'


import pip
with open("requirement.txt") as f:
    for line in f: pip.main(['install', line])