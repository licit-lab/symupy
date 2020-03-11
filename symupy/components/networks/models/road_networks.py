""" 
    Road Networks - Submodule

    This submodule contains the networks that can be created at infrastructure level. Networks can be of different types and at different layers. E.g. Road network where cars drive is physical one. 

    LICIT-LAB 
    Author: Andres Ladino
"""
import typing

# Module imports
from symupy.utils import constants as ct

import networkx as nx


class RoadNetwork(object):
    pass


class RoadSideUnit(object):

    rsuid = 0

    def __init__(self, link: str, position: float, radious: int = ct.RADIOUS_ANT):
        self.__class__.rsuid += 1
        self._link = link
        self._pos = position
        self._radious = radious

    def get_abs_pos(self):
        raise NotImplementedError
