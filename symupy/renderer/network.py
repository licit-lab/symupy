import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.lines import Line2D
from itertools import cycle
import numpy as np


def render(network, fig=None, termination_zone=[], sensors=[], path={}):
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
    print(np.array(network_coords).shape)
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

    network_coords = np.delete(
        np.array(network_coords, dtype=object), list(ids_to_delete), axis=0
    )
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
    plt.show()
