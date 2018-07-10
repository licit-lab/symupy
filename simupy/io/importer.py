"""
    Input parser 
"""

import os 
import platform 
from ctypes import cdll

# Directory path where simuvia can be found
_MACPTH = ('simupy', 'symuvia', 'Contents', 'Frameworks')
_LINPTH = () # TODO: Assign default path in Linux
_WINPTH = () # TODO: Assign default path in Windows
_MACLYB = ('libSymuVia.dylib',)
_LINLYB = () # TODO: Assign default library in Linux
_WINLIB = () # TODO: Assign default library in Windows

def get_default_lyb_path():
    """
        Determine the platform in use and import defa
    """
    os_type = platform.system()
    dlibPathOS = {'Darwin': _MACPTH,
                  'Linux': _LINPTH,
                  'Windows': _WINPTH,}
    dlibNameOS = {'Darwin': _MACLYB,
                  'Linux': _LINLYB,
                  'Windows': _WINLIB}
    slibPathName = dlibPathOS[os_type]+dlibNameOS[os_type]
    return slibPathName

def build_full_path(tlibPathName):
    """
        :param tuple tlibPathName: Relative path for the library

    """
    scurrDir = os.getcwd()            
    slibPathName = os.path.join(scurrDir, *tlibPathName)

    return slibPathName


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
            except:                 
                self.olibSymuVia = None
            finally: 
                self.print_LoadStatus()
        else:
            tlibPathName = get_default_lyb_path()
            self.fullSymPath = build_full_path(tlibPathName)
            print(f'Defining a default path for the library at: {self.fullSymPath}')
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
            
    def print_LoadStatus(self):
        """
            Status printer
        """
        tlibPathName = get_default_lyb_path()
        sdefPathLib = build_full_path(tlibPathName)

        try:
            if self.olibSymuVia:
                if sdefPathLib == self.fullSymPath:
                    print('Default path library loaded.')    
                else:
                    print('External path library loaded.')
        except AttributeError:
            print(f'Library could not loaded. Try providing defining a new path') 
        finally: 
            print(f'The path: {self.fullSymPath} was used')
