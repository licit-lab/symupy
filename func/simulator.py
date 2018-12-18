"""
   This module contains information related to a Simulation.
   It is capable of:

    - Loading the symuvia library 
    - Loading the XML file 
    - Launching a simulation for the corresponding XML file
"""

# ---------------------------IMPORTS------------------------------------------

# Utilities
import os

# C imports
from ctypes import cdll, create_string_buffer, c_int, byref, c_bool, c_double

# Internals
from symupy.func.container import Container

# Supplementary tools
from lxml import etree
from datetime import datetime

# ---------------------------CONSTANTS----------------------------------------


MAXSTEPS = 86400  # Max simulation steps


def find_simulator_lib():
    "Returns absolute path libSymuVia.dylib"
    for root, dirs, files in os.walk(os.getcwd()):
        for name in files:
            if name == 'libSymuVia.dylib':
                return os.path.join(root, name)


DEFAULT_LBR = find_simulator_lib()

# ---------------------------CLASSES-------------------------------------------


class Simulator(object):
    """
    Loader: 'libSymuvia.dylib'

    Provide the absolute path:
    /Users/myuser/myproject/libSymuVia.dylib

    Default relative path: 
    symupy/symuvia/Contents/Frameworks/libSymuVia.dylib

    """

    def __init__(self, fullSymPath: str = DEFAULT_LBR)-> None:
        """
        Class constructor
        """
        self.sfullSymPath = fullSymPath
        self.olibSymuVia = self.load_SymuViaLib()
        self.iBufferString = 10000

    def load_SymuViaLib(self)->cdll:
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

    def __init__(self, fileName, fullSymPath: str = DEFAULT_LBR):
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
            oSimulation = oSimulator.SymLoadNetworkEx(self.encoded_FileName())
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
        self.bSuccess = 1
        self.oContainer = Container()

    def set_NumberIterations(self, numIt=MAXSTEPS):
        """ Find the number of iterations within for a Simulation

            :param int numIt: Integer indicating the maximum number of iterations
        """
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
        nIterations = int(fDeltaT/float(sTimeStep))
        return min(nIterations, numIt)

    def load_XML(self):
        """ Creates XML object within Python"""
        oTree = etree.parse(self.sfileName)
        root = oTree.getroot()
        self.oXMLTree = root

    def run_SimulationByStep(self, numIt=MAXSTEPS):
        """ Run a full simulation step by step"""
        self.load_Simulation()
        self.init_Simulation()

        iIterations = self.set_NumberIterations(numIt)
        step = iter(range(iIterations))
        while self.bSuccess > 0:
            try:
                iIt = next(step)
                print(f'Iteration: {iIt+1}')
                self.run_Step()
                self.oContainer.fill_Container(self.query_DataStep())
            except StopIteration:
                print('Stop by iteration')
                self.bSuccess = 0
            except:
                self.bSuccess = self.run_Step()
                sRequest = self.query_DataStep()
                print('Return from Symuvia Empty: {}'.format(sRequest))
                self.bSuccess = 0

    def run_Step(self):
        """ Launches a single step fo simulation """
        self.bSuccess = self.olibSymuVia.SymRunNextStepEx(
            self.sRequest, True, byref(self.bEnd))

    def query_DataStep(self):
        """ Query data from a step"""
        return self.sRequest.value.decode('UTF8')
