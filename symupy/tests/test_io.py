"""
    Test file for io module 

    Author: Andres Ladino
"""

import os
import sys
import unittest
import symupy.symupy.io

print(os.getcwd())
stestDir = os.getcwd()
smodulePathDir = ('symupy')
smodulePathName = os.path.join(stestDir, smodulePathDir)
print(smodulePathName)


class Testio(unittest.TestCase):
    """
        Tests for the io submodule
    """

    # Submodule directory
    stestDir = os.getcwd()
    smodulePathDir = ('symupy')
    smodulePathName = os.path.join(stestDir, smodulePathDir)
    sys.path.append(smodulePathName)

    def test_load_SymuViaLib(self):
        """
            Test library load
        """
        # Constructors
        # objIo = symupy.io.SymuViaImporter()


if __name__ == "__main__":
    pass
