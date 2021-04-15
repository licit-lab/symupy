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

        self._sensor_plot = list()
        self._termination_zone_plot = list()
        self._path_plot = list()
        self._legends = list()
        self._legend = None

        for id, link in self._network.links.items():
            self._network_coords.append(
                [link["upstream_coords"].tolist()]
                + [arr.tolist() for arr in link["internal_points"]]
                + [link["downstream_coords"].tolist()]
            )

    @property
    def color(self):
        return next(self._colors)


    def draw_network(self):
        network_coords = np.row_stack([arr + [[None, None]] for arr in self._network_coords])
        self._network_plot = self._fig.gca().plot(
            network_coords[:, 0],
            network_coords[:, 1],
            "k",
            alpha=0.7,
            linewidth=1,
        )
        plt.draw()

    def draw_paths(self, paths:dict):
        for key, troncons in paths.items():
            troncons_id = [self._network_keys.index(id) for id in troncons]
            coords = np.array(self._network_coords, dtype=object)[troncons_id]
            coords = np.row_stack([arr for arr in coords])
            c = self.color
            self._path_plot.append(self._fig.gca().plot(coords[:, 0], coords[:, 1], c, linewidth=2)[0])
            self._path_plot.append(self._fig.gca().plot(coords[0,0], coords[0,1], 'k+')[0])
            self._path_plot.append(self._fig.gca().annotate("O",(coords[0,0], coords[0,1])))
            self._path_plot.append(self._fig.gca().plot(coords[-1,0], coords[-1,1], 'k+')[0])
            self._path_plot.append(self._fig.gca().annotate("D",(coords[-1,0], coords[-1,1])))
            self._path_plot.append(self._fig.gca().annotate("D",(coords[-1,0], coords[-1,1])))
            self._legends.append([Line2D([0], [0], color=c, lw=2), str(key)])

        self._show_legend()
        plt.draw()


    def draw_termination_zones(self, termination_zone:list):
        for key in termination_zone:
            troncons = self._network.termination_zone[key]["links"]
            troncons_id = [self._network_keys.index(id) for id in troncons]
            coords = np.array(self._network_coords, dtype=object)[troncons_id]
            coords = np.row_stack([arr + [[None, None]] for arr in coords])
            c = self.color
            self._termination_zone_plot.append(self._fig.gca().plot(coords[:, 0], coords[:, 1], c, linewidth=2)[0])
            self._legends.append([Line2D([0], [0], color=c, lw=2), str(key)])
        self._show_legend()
        plt.draw()

    def draw_sensors(self, sensors:list):
        for key in sensors:
            troncons = self._network.sensors[key]["links"]
            troncons_id = [self._network_keys.index(id) for id in troncons]
            coords = np.array(self._network_coords, dtype=object)[troncons_id]
            coords = np.row_stack([arr + [[None, None]] for arr in coords])
            c = self.color
            self._sensor_plot.append(self._fig.gca().plot(coords[:, 0], coords[:, 1], c, linewidth=2)[0])
            self._legends.append([Line2D([0], [0], color=c, lw=2), str(key)])
        self._show_legend()
        plt.draw()

    def _show_legend(self):
        leg = [i[0] for i in self._legends]
        lab = [i[1] for i in self._legends]
        self._legend = self._fig.gca().legend(leg, lab)



    def clear(self):
        for plot in [self._path_plot, self._termination_zone_plot, self._sensor_plot]:
            for line in plot:
                line.remove()
            plot.clear()
        self._legends.clear()
        self._legend.remove()
        plt.draw()

    def plot(self):
        plt.title('Network')
        plt.legend(loc="center left", bbox_to_anchor=(1.05, 0.5))
        plt.tight_layout()
        self._fig.gca().set_aspect("equal")
        self._fig.show()



if __name__ == '__main__':
    from symupy.plugins.reader.symuvia import SymuviaNetworkReader
    file = "/Users/florian/Work/visunet/data/Lyon63V/L63V.xml"
    reader = SymuviaNetworkReader(file)
    network = reader.get_network()
    renderer = NetworkRenderer(network)
    # renderer.add_sensors(['MFD_692660102'])
    # renderer.add_termination_zones(["690340602"])
    # renderer.remove_termination_zones(["690340602"])
    # renderer.draw_network()
    # renderer.draw_path({1:['Rue_Crequi_SN_1', 'Cr_Lafayette_OE_6', 'Cr_Lafayette_OE_7']})
    #
    # renderer.plot()
