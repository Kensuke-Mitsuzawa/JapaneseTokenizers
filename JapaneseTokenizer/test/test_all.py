__author__ = 'kensuke-mi'

import unittest
from test_mecab_wrapper import TestMecabWrapper

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestMecabWrapper))

    return suite