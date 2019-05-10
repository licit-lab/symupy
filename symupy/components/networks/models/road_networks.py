import typing

# Module imports
from symupy.utils import constants as ct


class RoadNetwork(object):
    pass


class RoadSideUnit(object):

    def __init__(self, link: str, position: float, radious: int = ct.RADIOUS_ANT):
        self._link = link
        self._pos = position
        self._radious = radious

    def get_abs_pos(self):
        raise NotImplementedError
