from dataclasses import dataclass, field
from typing import Any
from collections import OrderedDict
import numpy as np


@dataclass
class NetworkElement:
    id: Any = None


@dataclass
class Node(NetworkElement):
    links: list = field(default_factory=list)
    pos: np.ndarray = None

    def __getitem__(self, attr):
        return self.__dict__[attr]

    def __setitem__(self, attr, value):
        self.__dict__[attr] = value

@dataclass
class Link(NetworkElement):
    downstream_node: Node = None
    upstream_node: Node = None
    nb_lanes: int = 1
    authorized_mode: str = "all"
    internal_points: list = field(default_factory=list)

    def __getitem__(self, attr):
        return self.__dict__[attr]

    def __setitem__(self, attr, value):
        self.__dict__[attr] = value

@dataclass
class Zone(NetworkElement):
    links: list = field(default_factory=list)


@dataclass
class Sensor:
    id: Any = None
    links: list = field(default_factory=list)
    mesure: list = field(default_factory=list)

    def __getitem__(self, attr):
        return self.__dict__[attr]

    def __setitem__(self, attr, value):
        self.__dict__[attr] = value

    def __repr__(self):
        return f"Sensor(id={self.id.__repr__()}, {len(self.links)} links)"

@dataclass
class TerminationZone:
    id: Any = None
    links: list = field(default_factory=list)

    def __getitem__(self, attr):
        return self.__dict__[attr]

    def __setitem__(self, attr, value):
        self.__dict__[attr] = value

    def __repr__(self):
        return f"TerminationZone(id={self.id.__repr__()}, {len(self.links)} links)"


class Network(NetworkElement):
    __slots__ = ['sensors', 'termination_zone', 'links', 'nodes', 'adj']

    def __init__(self, id, links=list(), nodes=list(), sensors=list()):
        super().__init__(id)
        self.links = OrderedDict()
        self.nodes = OrderedDict()
        self.sensors = dict()
        self.termination_zone = dict()
        self.networks = dict()

    def add_node(self, id, coords=None):
        self.nodes[id] = Node(id, pos=coords)

    def add_link(self, id, upstream_node, downstream_node, nb_lanes=1, authorized_mode="all"):
        assert id not in self.links.keys(), f"{id} is already in Network"
        if upstream_node not in self.nodes.keys():
            self.add_node(upstream_node)
        if downstream_node not in self.nodes.keys():
            self.add_node(downstream_node)

        l = Link(id=id,
                 upstream_node=upstream_node,
                 downstream_node=downstream_node,
                 nb_lanes=nb_lanes,
                 authorized_mode=authorized_mode)

        self.links[id] = l
        self.nodes[upstream_node]['links'].append(id)
        self.nodes[downstream_node]['links'].append(id)

    def add_sensor(self, id, links):
        for l in links:
            assert l in self.links.keys(), f"{l} is not in Network"
        self.sensors[id] = Sensor(id, links)

    def add_termination_zone(self, id, links):
        for l in links:
            assert l in self.links.keys(), f"{l} is not in Network"
        self.termination_zone[id] = TerminationZone(id, links)

    def add_network(self, id, network):
        self.networks[id] = network

    def get_nodes_attributes(self, attr):
        return {k:n[attr] for k,n in self.nodes.items()}

    def get_links_attributes(self, attr):
        return {k:l[attr] for k,l in self.links.items()}

    def get_borders(self, id):
        return [self.nodes[self.links[id]['upstream_node']],
                self.nodes[self.links[id]['downstream_node']]]

    def get_regions(self, id):
        return [self.links[l] for l in self.nodes[id]['links']]

    def __repr__(self):
        return f"Network(id={self.id.__repr__()}, {len(self.links)} links, {len(self.nodes)} nodes)"
