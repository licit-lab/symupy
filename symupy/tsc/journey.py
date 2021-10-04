from dataclasses import dataclass, field
from typing import Any, Union
from symupy.tsc.network import Zone, Node, Link
from symupy.tsc.vehicles import Vehicle


@dataclass
class Path:
    links: list = field(default_factory=list)
    length: float = -1

    def __getitem__(self, attr):
        return self.__dict__[attr]

    def __setitem__(self, attr, value):
        self.__dict__[attr] = value

    def __repr__(self):
        return f"Path({len(self.links)} links, length={self.length})"


@dataclass
class State:
    time: str = None
    speed: float = 0
    acceleration: float = 0
    curvilinear_abscissa: float = 0
    absolute_position: list = field(default_factory=list)
    link: str = None
    lane: int = None

    def __getitem__(self, attr):
        return self.__dict__[attr]

    def __setitem__(self, attr, value):
        self.__dict__[attr] = value


@dataclass
class Trip:
    states: list = field(default_factory=list)
    vehicle: Vehicle = None
    mode: str = None
    path: Path = None
    departure_time: str = None
    arrival_time: str = None
    origin: Union[Node, Link, Zone] = None
    destination: Union[Node, Link, Zone] = None

    def __getitem__(self, attr):
        return self.__dict__[attr]

    def __setitem__(self, attr, value):
        self.__dict__[attr] = value

    def __repr__(self):
        return f"Trip(veh={self.vehicle}, origin={self.origin.__repr__()}, destination={self.destination.__repr__()}, {len(self.states)} states)"


@dataclass
class Journey:
    trips: list = field(default_factory=list)
    origin: Union[Node, Link, Zone] = None
    destination: Union[Node, Link, Zone] = None

    def __getitem__(self, attr):
        return self.__dict__[attr]

    def __setitem__(self, attr, value):
        self.__dict__[attr] = value

    def __repr__(self):
        return f"Sensor(id={self.id.__repr__()}, {len(self.links)} links)"
