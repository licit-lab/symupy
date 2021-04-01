# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import pandas as pd
import os

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from symupy.tsc.journey import Path, State, Trip
from symupy.utils.exceptions import SymupyWarning
from symupy.abstractions.reader import AbstractTrafficDataReader

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================



class SymuMasterTrafficDataReader(AbstractTrafficDataReader):
    def __init__(self, ppaths, final_ppaths, distribution):
        self._file_ppaths = ppaths
        self._file_final_ppaths = final_ppaths
        self._file_distribution = distribution

        self.ppaths = None
        self.final_ppaths = None
        self.distribution = None

    def load_ppaths(self):
        self.ppaths = pd.read_csv(self._file_ppaths, sep=';', index_col=False, header=None, engine='python')

    def load_final_ppaths(self):
        self.final_ppaths = pd.read_csv(self._file_final_ppaths, sep=';', index_col=False, engine='python')

    def load_distribution(self):
        self.distribution = pd.read_csv(self._file_distribution, sep=';', index_col=False, engine='python')

    def clean(self):
        del self.ppaths
        del self.final_ppaths
        del self.distribution

        self.ppaths = None
        self.final_ppaths = None
        self.distribution = None

    def get_trip(self, vehid): #final_ppath
        #No States
        pass

    def get_OD(self, period, OD, loop=None): #Both ppaths and distribution
        pass



if __name__ == '__main__':
    fileppaths = '/Users/florian.gacon/Work/data/LYON63V/default_PPaths.csv'
    filefinal = '/Users/florian.gacon/Work/data/LYON63V/default_final_ppaths.csv'
    filedistrib = '/Users/florian.gacon/Work/data/LYON63V/default_distribution.csv'

    reader = SymuMasterTrafficDataReader(fileppaths, filefinal, filedistrib)
    reader.load_final_ppaths()
    reader.load_ppaths()
    reader.load_distribution()
