"""
    Test file for func module
"""

import os
import unittest
from symupy.func import Simulator


class Test_func(unittest.TestCase):

    def test_load_SymuViaLib(self):
        """
        Test library load
        """
        tRelLibPath = ('symuvia',
                       'Contents',
                       'Frameworks',
                       'libSymuvia.dylib')
        sLibPath = os.path.join(os.getcwd(), *tRelLibPath)
        print(f'Test dir: {sLibPath}')
        # objSimulator = Simulator(sLibPath)
