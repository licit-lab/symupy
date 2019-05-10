import typing
from typing import TypeVar, Iterable, Tuple, Union

# Local imports
from .road_networks import RoadSideUnit

Veh = TypeVar('Veh')
NetElem = Union(RoadSideUnit, )


class VehicleToInfastructureNetwork(object):
    def __init__(self) -> None:
        self._nodes_elem = []
        self._vehs_elem = []

    def register_element(self, element: NetElem) -> None:
        self._nodes_elem.append(element)

    def register_veh(self, veh: Veh) -> None:
        self._vehs_elem.append(veh)
