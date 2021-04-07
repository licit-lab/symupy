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
from symupy.utils.time import Date
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
        self.final_ppaths = pd.read_csv(self._file_final_ppaths, sep=';', index_col=False, engine='python', header=None)

    def load_distribution(self):
        self.distribution = pd.read_csv(self._file_distribution, sep=';', index_col=False, engine='python', header=None)

    def clean(self):
        del self.ppaths
        del self.final_ppaths
        del self.distribution

        self.ppaths = None
        self.final_ppaths = None
        self.distribution = None

    def get_trip(self, vehid):
        row = self.final_ppaths[self.final_ppaths.iloc[:,3]==float(vehid)]
        path = row[7].to_list()[0].split('\\')
        origin = path[0]
        dest = path[-1]
        departure_time = Date(row[4].to_list()[0])
        if row[5].to_list()[0] == 'Undefined':
            arrival_time = 'Undefined'
        else:
            arrival_time = Date(row[5].to_list()[0])

        return Trip(path=path[1:-1][::2],
                    departure_time=departure_time,
                    arrival_time=arrival_time,
                    origin=origin,
                    destination=dest,
                    vehicle=vehid)

    def get_OD(self, OD, period=None, loop=None, file='distribution'): #Both ppaths and distribution
        if file == 'distribution':
            mask = (self.distribution.iloc[:,4]==OD[0]) & (self.distribution.iloc[:,5]==OD[1]) & (self.distribution.iloc[:,8]!='Sum of user and minimum travel time for the OD')
            if period is not None:
                pass
            if loop is not None:
                pass
            rows = self.distribution[mask]
            print(rows)


if __name__ == '__main__':
    fileppaths = '/Users/florian/Work/visunet/data/Lyon63V/Out_SymuMaster/default_PPaths.csv'
    filefinal = '/Users/florian/Work/visunet/data/Lyon63V/Out_SymuMaster/default_final_PPaths.csv'
    filedistrib = '/Users/florian/Work/visunet/data/Lyon63V/Out_SymuMaster/default_distribution.csv'

    reader = SymuMasterTrafficDataReader(fileppaths, filefinal, filedistrib)
    reader.load_final_ppaths()
    # reader.load_ppaths()
    reader.load_distribution()

    t = reader.get_OD(('690340602', '692660103'))
