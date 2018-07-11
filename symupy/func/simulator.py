"""
    Simulator class is capable of:

    - Loading the symuvia library 
    - Loading the XML file 
    - Launching a simulation for the corresponding XML file
"""

from lxml import etree
from ctypes import cdll

class Simulator():
    """
        Simulator class can launch a simulation. 
    """
    def __init__(self, fullSymPath):
        """
            Class constructor
            :param string fullSymPath: string containing the library path to Simuvia 
        """
        self.sfullSymPath = fullSymPath
        self.olibSymuVia = self.load_SymuViaLib()

    def load_SymuViaLib(self):
        """
            Library loader 
        """
        try:
            oSimulator = cdll.LoadLibrary(self.sfullSymPath)
        except:
            print('Symuvia Library could not be loaded')
        
        return oSimulator

class Simulation(Simulator):
    """
        Simulation parses an XML data for a paricular case. When created a simulator is asociated
    """

    def __init__(self, fileName, fullSymPath):
        """
            Class constructor
            
            :param string fileName: string containing the library path to a Simulation 

            :param string fullSymPath: string containing the library path to Simuvia 
        """

        super().__init__(fullSymPath)
        print(f'Simulator created at: {fileName}')
        self.sfileName = fileName
        self.oSimulation = self.load_SymuviaXML()

    def load_SymuviaXML(self):
        """
            XML loader

            Load XML Simulation file in order to perform simulation 
        """
        try: 
            oSimulator = self.olibSymuVia
            sfileNameEnc = self.sfileName.encode('UTF8')
            oSimulation = oSimulator.SymLoadNetworkEx(sfileNameEnc)
            print('Symuvia Library succesfully loaded')            
        except:
            print('Symuvia Library could not be loaded')
        return oSimulation

    
    def run_Simulation(self):
        """ Launches a full-time simulation """        
        return self.olibSymuVia.SymRunEx(self.encoded_FileName())


    def encoded_FileName(self):
        """ Returns the file name encoded for the simulator """
        return self.sfileName.encode('UTF8')