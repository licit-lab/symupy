"""
   This module contains information related to a Simulation.
   It is capable of:

    - Loading the symuvia library 
    - Loading the XML file 
    - Launching a simulation for the corresponding XML file
"""

from datetime import datetime
from lxml import etree
from ctypes import cdll, create_string_buffer, c_int, byref, c_bool, c_double 

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
        self.iBufferString = 10000

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
        self.oSimulation = self.load_Simulation()

    def load_Simulation(self):
        """ Load XML Simulation file in order to perform simulation """
        try: 
            oSimulator = self.olibSymuVia
            sfileNameEnc = self.sfileName.encode('UTF8')
            oSimulation = oSimulator.SymLoadNetworkEx(sfileNameEnc)
            print('Symuvia Library succesfully loaded')            
        except:
            print('Symuvia Library could not be loaded')
        return oSimulation

    def encoded_FileName(self):
        """ Returns the file name encoded for the simulator """
        return self.sfileName.encode('UTF8')
    
    def run_Simulation(self):
        """ Launches a full-time simulation """        
        return self.olibSymuVia.SymRunEx(self.encoded_FileName())

    def init_Simulation(self):
        """ Initializes conditions for a step by step simulation"""
        # Pointers
        self.sRequest = create_string_buffer(self.iBufferString)
        self.bEnd = c_int()
        self.bSecond = c_bool(True)
        self.bForce = c_int(1)

    def set_NumberIterations(self, numIt):
        """ Find the number of iterations within for a Simulation"""
        self.load_XML()
        sPathTime = 'SIMULATIONS/SIMULATION'
        oElement = self.oXMLTree.xpath(sPathTime)[0].attrib
        sTimeStep = oElement['pasdetemps']
        sTimeStart = oElement['debut']
        sTimeEnd = oElement['fin']
        sDate = oElement['date']
        sDateSt = sDate + ' ' + sTimeStart
        sDateEd = sDate + ' ' + sTimeEnd
        sDateFormat = '%Y-%m-%d %H:%M:%S'
        oTimeSt = datetime.strptime(sDateSt, sDateFormat)
        oTimeEd = datetime.strptime(sDateEd, sDateFormat)
        fDeltaT = oTimeEd - oTimeSt
        fDeltaT = fDeltaT.total_seconds()
        nIterations = fDeltaT/float(sTimeStep)
        return nIterations

    def load_XML(self):
        """ Creates XML object within Python"""
        oTree = etree.parse(self.sfileName)
        root = oTree.getroot()
        self.oXMLTree = root

    def run_SimulatonbyStep(self):
        """ Run a full simulation step by step"""
        while self.bSuccess>0:
            self.run_Step()

    def run_Step(self):
        """ Launches a single step fo simulation """
        self.bSuccess =  self.olibSymuVia.SymRunNextStepEx(self.sRequest, True, byref(self.bEnd))
