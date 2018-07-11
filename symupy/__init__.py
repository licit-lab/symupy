"""
    SymuPy: Symuvia Traffic Simulator - Python API 

    This main file imports the modules required to interact with SymuVia

    Four main submodules are considered:

    - io: Input/Output interaction with Symuvia
    - func: Implement parameter/config functions within the module
    - control: Control / manipulation of traffic conditions in simulation
    - util: Other tools 
"""

__author__ = "Andres Ladino"
__copyright__ = "SymuPy Project"
__credits__ = ["Cecile Becarie"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Andres Ladino"
__email__ = "andres.ladino@ifsttar.fr"
__status__ = "Prototype"


__all__ = ['io',
           'control',
           'func',
           'util',
           ]

print('Importing the Simupy package')

from .io import *
from .func import *
# from control import *
# from util import *