import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.lines import Line2D
from itertools import cycle
import numpy as np


class NetworkRenderer(object):
    def __init__(self, network, fig=None):
        self._network = network
        if fig is None:
            self._fig = plt.figure()
        else:
            self._fig = fig

        self._colors = cycle(mcolors.TABLEAU_COLORS.values())

        self._network_coords = []
        self._network_keys = list(self._network.links.keys())

        self._ids_to_delete = set()
        self._sensor_plot = dict()
        self._termination_zone_plot = dict()
        self._path_plot = dict()

        for id, link in self._network.links.items():
            self._network_coords.append(
                [link["upstream_coords"].tolist()]
                + [arr.tolist() for arr in link["internal_points"]]
                + [link["downstream_coords"].tolist()]
            )

    def add_termination_zones(self, termination_zones:list):
        for key in termination_zones:
            troncons = self._network.termination_zone[key]["links"]
            troncons_id = [self._network_keys.index(id) for id in troncons]
            self._termination_zone_plot[key] = troncons_id

    def remove_termination_zones(self, termination_zones:list):
        for key in termination_zones:
            if key in self._termination_zone_plot.keys():
                del self._termination_zone_plot[key]

    def add_sensors(self, sensors:list):
        for key in sensors:
            troncons = self._network.sensors[key]["links"]
            troncons_id = [self._network_keys.index(id) for id in troncons]
            self._sensor_plot[key] = troncons_id

    def remove_sensors(self, sensors:list):
        for key in sensors:
            if key in self._sensor_plot.keys():
                del self._sensor_plot[key]

    def add_paths(self, paths:dict):
        for key, troncons in paths.items():
            troncons_id = [self._network_keys.index(id) for id in troncons]
            self._path_plot[key] = troncons_id

    def remove_paths(self, paths:list):
        for key in paths:
            if key in self._path_plot.keys():
                del self._path_plot[key]


    def draw(self):
        for key, tids in self._sensor_plot.items():
            self._ids_to_delete.update(tids)
            coords = np.array(self._network_coords, dtype=object)[tids]
            coords = np.row_stack([arr + [[None, None]] for arr in coords])
            self._fig.gca().plot(coords[:, 0], coords[:, 1], next(self._colors), label=key, linewidth=3)

        for key, tids in self._termination_zone_plot.items():
            self._ids_to_delete.update(tids)
            coords = np.array(self._network_coords, dtype=object)[tids]
            coords = np.row_stack([arr + [[None, None]] for arr in coords])
            self._fig.gca().plot(coords[:, 0], coords[:, 1], next(self._colors), label=key, linewidth=3)

        for key, tids in self._path_plot.items():
            self._ids_to_delete.update(tids)
            coords = np.array(self._network_coords, dtype=object)[tids]
            coords = np.row_stack([arr for arr in coords])
            self._fig.gca().plot(coords[:, 0], coords[:, 1], next(self._colors), label=key, linewidth=3)
            self._fig.gca().plot(coords[0,0], coords[0,1], 'k+')
            self._fig.gca().annotate("O",(coords[0,0], coords[0,1]))
            self._fig.gca().plot(coords[-1,0], coords[-1,1], 'k+')
            self._fig.gca().annotate("D",(coords[-1,0], coords[-1,1]))

        if self._ids_to_delete:
            network_coords = np.delete(
                np.array(self._network_coords, dtype=object), list(self._ids_to_delete), axis=0)
        else:
            network_coords = self._network_coords

        network_coords = np.row_stack([arr + [[None, None]] for arr in network_coords])

        self._fig.gca().plot(
            network_coords[:, 0],
            network_coords[:, 1],
            "k",
            alpha=0.7,
            linewidth=1,
        )

    def reset(self):
        self._fig.clf()
        self._ids_to_delete = set()
        self._sensor_plot = dict()
        self._termination_zone_plot = dict()
        self._path_plot = dict()

    def plot(self):
        plt.title('Network')
        plt.legend(loc="center left", bbox_to_anchor=(1.05, 0.5))
        plt.tight_layout()
        self._fig.gca().set_aspect("equal")
        plt.show()



def draw_network(network, fig=None, termination_zone=[], sensors=[], path={}):
    colors = cycle(mcolors.TABLEAU_COLORS.values())
    network_coords = []
    ids_to_delete = set()
    sensor_plot = dict()
    termination_zone_plot = dict()
    path_plot = dict()
    network_keys = list(network.links.keys())

    if fig is None:
        fig = plt.figure()

    for id, link in network.links.items():
        network_coords.append(
            [link["upstream_coords"].tolist()]
            + [arr.tolist() for arr in link["internal_points"]]
            + [link["downstream_coords"].tolist()]
        )

    for key in sensors:
        troncons = network.sensors[key]["links"]
        troncons_id = [network_keys.index(id) for id in troncons]
        sensor_plot[key] = np.array(network_coords, dtype=object)[troncons_id]
        ids_to_delete.update(troncons_id)

    for key in termination_zone:
        troncons = network.termination_zone[key]["links"]
        troncons_id = [network_keys.index(id) for id in troncons]
        termination_zone_plot[key] = np.array(network_coords, dtype=object)[troncons_id]
        ids_to_delete.update(troncons_id)

    for key, troncons in path.items():
        troncons_id = [network_keys.index(id) for id in troncons]
        ids_to_delete.update(troncons_id)
        path_plot[key] = np.array(network_coords, dtype=object)[troncons_id]

    if ids_to_delete:
        network_coords = np.delete(
            np.array(network_coords, dtype=object), list(ids_to_delete), axis=0)

    network_coords = np.row_stack([arr + [[None, None]] for arr in network_coords])
    fig.gca().plot(
        network_coords[:, 0],
        network_coords[:, 1],
        "k",
        label="Network",
        alpha=0.7,
        linewidth=1,
    )

    for key, coords in sensor_plot.items():
        coords = np.row_stack([arr + [[None, None]] for arr in coords])
        fig.gca().plot(coords[:, 0], coords[:, 1], next(colors), label=key, linewidth=1)

    for key, coords in termination_zone_plot.items():
        coords = np.row_stack([arr + [[None, None]] for arr in coords])
        fig.gca().plot(coords[:, 0], coords[:, 1], next(colors), label=key, linewidth=1)

    for key, coords in path_plot.items():
        coords = np.row_stack([arr + [[None, None]] for arr in coords])
        fig.gca().plot(coords[:, 0], coords[:, 1], next(colors), label=key, linewidth=1)

    plt.legend(loc="center left", bbox_to_anchor=(1.05, 0.5))
    plt.tight_layout()
    fig.gca().set_aspect("equal")

if __name__ == '__main__':
    from symupy.parser.symuvia import SymuviaNetworkReader
    file = "/Users/florian/Work/visunet/data/Lyon63V/L63V.xml"
    reader = SymuviaNetworkReader(file)
    network = reader.get_network()
    renderer = NetworkRenderer(network)
    renderer.add_sensors(['MFD_692660102'])
    renderer.add_termination_zones(["690340602"])
    renderer.remove_termination_zones(["690340602"])
    renderer.draw()
    renderer.plot()
