import typing
from typing import TypeVar, Iterable, Tuple, Union

# Local imports
from .road_networks import RoadSideUnit
from symupy.components.vehicles import Vehicle


class V2XNetwork(object):
    def __init__(self) -> None:
        self._nodes_elem = []
        self._veh_elem = []

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        tp = tuple(veh.vehid for veh in self._veh_elem)
        return f"Vehicle registered: {tp}\n Elements registered: {tp}"

    def register_vehicle(self, veh: Vehicle) -> None:
        self._veh_elem.append(veh)


class V2INetwork(V2XNetwork):
    def __init__(self) -> None:
        super().__init__()

    def register_element(self, element: RoadSideUnit) -> None:
        self._nodes_elem.append(element)


class V2VNetwork(V2XNetwork):
    def __init__(self) -> None:
        super().__init__()
