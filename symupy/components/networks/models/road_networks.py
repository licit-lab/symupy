import typing

# Module imports
from symupy.utils import constants as ct


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
