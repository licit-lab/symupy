import time

import numpy as np
from matplotlib import pyplot as plt

from symupy.postprocess.visunet import logger

from PyQt5.QtWidgets import QDialog, QFileDialog

from symupy.postprocess.visunet.qtutils import Worker
from symupy.postprocess.visunet.reader import Reader
from symupy.renderer.trip import render_trip


class RoutesHandler(object):
    def __init__(self):
        self.dict = dict()
        self.reader_widget = Reader("output")
        self.reader = None
        self.renderer = None

    def append(self, tr_dict):
        self.dict.update(tr_dict)
        if self.renderer is not None:
            self.renderer.draw_paths(tr_dict)

    def addRenderer(self, renderer):
        self.renderer = renderer

    def clear(self):
        self.dict.clear()

    def addPath(self, vehid):
        self.process = Worker(self._process_path, [vehid])
        self.process.start()

    def addOD(self, args):
        self.process = Worker(self._process_OD, [args])
        self.process.start()

    def addTrip(self, vehid):
        trip = self.reader.get_trip(vehid)
        if trip is not None:
            self.append({vehid: trip.path.links})
            plt.draw()
            figtrip = plt.figure()
            render_trip(figtrip, trip)
            figtrip.show()

    def choose_reader(self, file):
        self.reader_widget.set_file(file)
        if self.reader_widget.exec_() == QDialog.Accepted:
            logger.debug(f"Choose reader {self.reader_widget.choosen_reader}")
            logger.info(f"Loading file {file.split('/')[-1]} ...")
            start = time.time()
            self.reader = self.reader_widget.choosen_reader(file)
            end = time.time()
            logger.info(f"Done [{end - start:.4f} s]")

    def _process_path(self, vehid):
        logger.info(f"Looking for path {vehid} and plotting it ...")
        start = time.time()
        path = self.reader.get_path(vehid)
        if path is not None:
            self.append({vehid: path.links})
        end = time.time()
        logger.info(f"Done [{end - start:.4f} s]")

    def _process_OD(self, args):
        logger.info(f"Looking for ODs withs args: {args}")
        start = time.time()
        od_list = self.reader.get_OD(*args)
        od_list = list(dict.fromkeys([tuple(path.links) for path in od_list]))
        logger.info(f"Found {len(od_list)} unique ODs ...")
        self.append({ind: path for ind, path in enumerate(od_list)})
        end = time.time()
        logger.info(f"Done [{end - start:.4f} s]")

    def export_csv(self):
        name = QFileDialog.getSaveFileName(
            parent=None, caption="Export Routes to csv", filter="csv files (*.csv)"
        )
        if name[0] != "":
            logger.info(f"Exporting routes in file: {name[0]}")
            with open(name[0], "w") as f:
                for ind, links in self.dict.items():
                    f.write(str(ind) + ";" + "/".join(links) + "\n")


def compute_length_path(network, path):
    length = 0
    for lid in path.links:
        link = network.links[lid]
        if len(link.internal_points) > 0:
            length += np.linalg.norm(link["upstream_coords"] - link.internal_points[0])
            length += sum(
                [
                    np.linalg.norm(
                        link.internal_points[i] - link.internal_points[i + 1]
                    )
                    for i in range(1, len(link.internal_points) - 1)
                ]
            )
            length += np.linalg.norm(
                link.internal_points[-1] - link["downstream_coords"]
            )
        else:
            length += np.linalg.norm(
                link["upstream_coords"] - link["downstream_coords"]
            )
    return length
