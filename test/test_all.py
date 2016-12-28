__author__ = 'kensuke-mi'

import sys
import unittest
python_version = sys.version_info


def suite():
    suite = unittest.TestSuite()
    if python_version >= (3, 0, 0):
        from .test_mecab_wrapper_python3 import TestMecabWrapperPython3
        from .test_kytea_wrapper_python3 import TestKyteaWrapperPython3
        from .test_juman_wrapper_python3 import TestJumanWrapperPython3
        from .test_jumanpp_wrapper_python3 import TestJumanppWrapperPython3
        suite.addTest(unittest.makeSuite(TestKyteaWrapperPython3))
        suite.addTest(unittest.makeSuite(TestMecabWrapperPython3))
        suite.addTest(unittest.makeSuite(TestJumanWrapperPython3))
        suite.addTest(unittest.makeSuite(TestJumanppWrapperPython3))
    else:
        from .test_mecab_wrapper_python2 import TestMecabWrapperPython2
        from .test_juman_wrapper_python2 import TestJumanWrapperPython2
        from .test_kytea_wrapper_python2 import TestKyteaWrapperPython2
        from .test_jumanpp_wrapper_python2 import TestJumanppWrapperPython2
        suite.addTest(unittest.makeSuite(TestKyteaWrapperPython2))
        suite.addTest(unittest.makeSuite(TestMecabWrapperPython2))
        suite.addTest(unittest.makeSuite(TestJumanWrapperPython2))
        suite.addTest(unittest.makeSuite(TestJumanppWrapperPython2))


    return suite