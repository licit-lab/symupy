"""
    Input/Output module 
"""

import os 
from ctypes import cdll


from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column, String, Integer, Float 
from sqlalchemy import insert, delete, select, case, and_

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
            
class SymuViaExporter(SymuViaImporter):
    """
        Class to export results from a simulation in SymuVia
    """

    def __init__(self, sdirOutput = None, sfileOutput = None):
        """
            Initialize a class with 

            :param string sdirOutput: Absolute path to store data

            :param string sfileOutput: Output path to store data
        """
        self.bfirstExecution = False 
        self.sdirOutput = sdirOutput

    def create_Exporter(self):
        """
            Parametrize conditions to export data in data bases 
        """
        if not self.sdirOutput: 
            engine_path = ('..',
                           'Output',
                           'SymOut.sqlite')
            engine_name = os.path.join(os.path.sep,*engine_path)
            engine_full_name = os.path.join(dir_path,*engine_path)
            engine_call = 'sqlite://'+engine_name
            engine = create_engine(engine_call)
            metadata = MetaData()

        try: 
            ltbstr = 'Loaded table in: '
            connection = engine.connect()    
            traj = Table('traj', metadata, autoload=True, autoload_with=engine)
            stmt = delete(traj)
            results = connection.execute(stmt)
        except:
            ltbstr = 'Loaded table in: '
            traj = Table('traj', metadata,
                    Column('ti', Float()),
                    Column('id', Integer()),
                    Column('type', String(3)),
                    Column('tron', String(10)),
                    Column('voie', Integer()),
                    Column('dst', Float()),
                    Column('abs', Float()),
                    Column('vit', Float()),
                    Column('ldr', Integer()),
                    Column('spc', Float()),
                    Column('vld', Float()))
            metadata.create_all(engine)
            connection = engine.connect()
        finally: 
            print(ltbstr, engine)


if __name__ == "__main__":
    objIo = SymuViaImporter()
    objIo.load_SymuViaLib()
    x = Simulator()