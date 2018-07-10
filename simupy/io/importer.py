"""
    Input parser 
"""

import os 
from ctypes import cdll


class SymuViaImporter():
    """
        Class to parse input files to SymuVia
    """

    def __init__(self, sdirFile = None, sdirSim = None):
        """
            Initialize a class with 

            :param string sdirFile: Absolute path XML input file 

            :param string sdirSim: Absolute path for libraries symuvia libraries  
        """
        self.fileName = sdirFile
        self.fullSymPath = sdirSim

    def load_SymuViaLib(self):
        """
            Load SymuVia library 
        """
        if self.fullSymPath:
            try:                 
                self.olibSymuVia = cdll.LoadLibrary(self.fullSymPath)
                print('Library successfully loaded') 
            except: 
                print('Library could not loaded')
                self.olibSymuVia = None
        else:
            scurrDir = os.getcwd()
            # MacDefault
            slibPathName = ('symupy',
                            'symuvia',
                            'Contents',
                            'Frameworks',
                            'libSymuVia.dylib') 
            self.fullSymPath = os.path.join(scurrDir, *slibPathName)
            self.load_SymuViaLib()

    def load_xml_file(self, fileName):
        """
            Load xml input file for SymuVia
        """
        if self.fileName:
            try:                 
                self.olibSymuVia = cdll.LoadLibrary(self.fullSymPath)
                print('File successfully loaded') 
                print('File directory:\n')
                print('{}'.format(self.fileName)) 
            except: 
                print('File could not be loaded')
                self.olibSymuVia = None
            