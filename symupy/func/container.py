"""
    This module manages data parsing for the simulator
"""

from xmltodict import parse

class Container():
    """ 
        Class 
    """
    
    def __init__(self):
        self.sDict  = {}
    
    def fill_Container(self, sQuery):
        """ Fills container with data extracted from the query"""
        try: 
            self.sQuery = sQuery
            self.sDict = parse(self.sQuery)
        except: 
            print('Not managed')

    def get_CurrentTime(self):
        """ Get travel time""" 
        return self.sDict['INST']['@val']