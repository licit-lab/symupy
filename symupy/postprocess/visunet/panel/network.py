import linecache
from collections import OrderedDict, defaultdict
import time
from inspect import signature

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.lines import Line2D
from PyQt5.QtCore import Qt, pyqtSlot, QThread, pyqtSignal
from PyQt5.QtWidgets import (QFileDialog, QGroupBox, QLabel, QPushButton,
                             QRadioButton, QVBoxLayout, QProgressBar, QDesktopWidget,
                             QWidget, QComboBox, QDialog)
from PyQt5.Qt import QRect

from symupy.postprocess.visunet.qtutils import waitcursor
from symupy.postprocess.visunet import logger
from symupy.postprocess.visunet.qtutils import Worker
from symupy.renderer.trip import render_trip
from symupy.renderer.network import NetworkRenderer
from symupy.plugins.reader import load_plugins

from .trajectory import TripSelector, ODSelector

class NetworkWidget(QGroupBox):
    def __init__(self, data, name=None, parent=None):
        super().__init__(name, parent)
        self.data = data

        self.file_network = None
        self.tree_network = None

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)


        self.label_file_netw = QLabel('Network:')
        self.label_file_traj = QLabel('Trajectories:')
        self.label_file_netw.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.layout.addWidget(self.label_file_netw)
        self.label_tr = QLabel('Troncons:')
        self.label_tr.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.layout.addWidget(self.label_tr)
        self.layout.addWidget(self.label_file_traj)

        self.network = None
        self.renderer = None
        self.input_reader_widget = Reader('input')
        self.output_reader_widget = Reader('output')

        self._input_reader = None
        self._output_reader = None


    def update_label(self):
        file = self.data.file_network.split('/')[-1]
        self.label_file_netw.setText('File: '+file)
        tr = len(self.network.links)
        self.label_tr.setText('Troncons: '+str(tr))

    def choose_input_reader_widget(self):
        self.input_reader_widget.set_file(self.data.file_network)
        if self.input_reader_widget.exec_() == QDialog.Accepted:
            logger.debug(f'Choose reader {self.input_reader_widget.choosen_reader}')
            self._input_reader = self.input_reader_widget.choosen_reader
            self.workerProcessNet = Worker(process_network, [self])
            self.workerPlotNet = Worker(plot_network, [self])
            self.workerProcessNet.finished.connect(self.workerPlotNet.start)
            self.workerProcessNet.start()

    def load_network(self):
        options = QFileDialog.Options(QFileDialog.Options(QFileDialog.DontUseNativeDialog))
        file, _ = QFileDialog.getOpenFileName(self,"Load Network", "","Network file (*)", options=options)

        if file != '':
            self.data.file_network = file
            self.choose_input_reader_widget()
            # self.process_network()
            # self.plot_network()

    def load_traffic_data(self):
        options = QFileDialog.Options(QFileDialog.Options(QFileDialog.DontUseNativeDialog))
        file, _ = QFileDialog.getOpenFileName(self,"Load Traffic Data", "","Traffic Data file (*)", options=options)

        if file != '':
            self.data.file_traj = file
            file = file.split('/')[-1]
            self.label_file_traj.setText('Trajectories: '+file)
            self.choose_output_reader_widget()

    def choose_output_reader_widget(self):
        self.output_reader_widget.set_file(self.data.file_traj)
        if self.output_reader_widget.exec_() == QDialog.Accepted:
            logger.debug(f'Choose reader {self.output_reader_widget.choosen_reader}')
            self._output_reader = self.output_reader_widget.choosen_reader(self.data.file_traj)

    def select_trip(self):
        trip_selector = TripSelector()
        if trip_selector.exec_() == QDialog.Accepted:
            vehid = trip_selector.vehid.value()
            if vehid != '':
                logger.info(f'Looking for trip {vehid} and plotting it ...')
                start = time.time()
                process_trip(self, vehid)
                end = time.time()
                logger.info(f'Done [{end-start:.4f} s]')

    def select_path(self):
        trip_selector = TripSelector()
        if trip_selector.exec_() == QDialog.Accepted:
            vehid = trip_selector.vehid.value()
            if vehid != '':
                self.workerProcessPath = Worker(process_path, [self, vehid])
                self.workerProcessPath.start()

    def selectOD(self):
        OD_selector = ODSelector(self._output_reader.get_OD)
        if OD_selector.exec_() == QDialog.Accepted:
            for arg in OD_selector.values:
                if arg=='None':
                    arg = None
            args = [None if arg=='None' else arg for arg in OD_selector.values]
            self.workerProcessTrip = Worker(process_ODs, [self, args])
            self.workerProcessTrip.start()

    def clear(self):
        if self.renderer is not None:
            logger.info('Clearing Renderer trajectories')
            self.renderer.clear()

@waitcursor
def process_network(networkwidget):
    logger.info(f'Creating Network object ...')
    start = time.time()
    networkwidget._input_reader = networkwidget._input_reader(networkwidget.data.file_network)
    networkwidget.network = networkwidget._input_reader.get_network()
    end = time.time()
    logger.info(f'Done [{end-start:.4f} s]')
    networkwidget.update_label()
    networkwidget.renderer = NetworkRenderer(networkwidget.network, networkwidget.data.figure)

@waitcursor
def process_path(networkwidget, vehid):
    logger.info(f'Looking for path {vehid} and plotting it ...')
    start = time.time()
    path = networkwidget._output_reader.get_path(vehid)
    length = compute_length_path(networkwidget.network, path)
    logger.info(f'Length of path: {length:.4f}')
    networkwidget.renderer.draw_paths({vehid:path.links})
    end = time.time()
    logger.info(f'Done [{end-start:.4f} s]')


@waitcursor
def process_trip(networkwidget, vehid):
    trip = networkwidget._output_reader.get_trip(vehid)
    networkwidget.renderer.draw_paths({vehid:trip.path.links})
    figtrip = plt.figure()
    render_trip(figtrip, trip)
    figtrip.show()


@waitcursor
def process_ODs(networkwidget, args_OD):
    try:
        logger.info(f'Looking for paths and plotting it ...')
        start = time.time()
        od_list = networkwidget._output_reader.get_OD(*args_OD)
        logger.info(f'Found {len(od_list)} ODs ...')
        pathes = {ind:path.links for ind, path in enumerate(od_list)}
        length_pathes = [compute_length_path(networkwidget.network, p) for p in od_list]
        logger.info(f'Length info:')
        logger.info(f'Mean: {sum(length_pathes)/len(length_pathes):.4f}')
        logger.info(f'Max: {max(length_pathes):.4f}')
        logger.info(f'Min: {min(length_pathes):.4f}')
        networkwidget.renderer.draw_paths(pathes)
        end = time.time()
        logger.info(f'Done [{end-start:.4f} s]')
    except:
        end = time.time()
        logger.info(f'Found nothing for args:{args_OD}')
        logger.info(f'Done [{end-start:.4f} s]')


def plot_network(networkwidget):
    logger.info(f'Rendering Network object ...')
    start = time.time()
    networkwidget.data.figure.clf()
    networkwidget.renderer.draw_network()
    plt.axis('off')
    plt.axis('tight')
    networkwidget.data.figure.gca().set_aspect('equal')
    end = time.time()
    logger.info(f'Done [{end-start:.4f} s]')


def compute_length_path(network, path):
    length = 0
    for lid in path.links:
        link = network.links[lid]
        if len(link.internal_points)>0:
            length += np.linalg.norm(link['upstream_coords']-link.internal_points[0])
            length += sum([np.linalg.norm(link.internal_points[i] - link.internal_points[i+1]) for i in range(1, len(link.internal_points)-1) ])
            length += np.linalg.norm(link.internal_points[-1]-link['downstream_coords'])
        else:
            length += np.linalg.norm(link['upstream_coords']-link['downstream_coords'])
    return length


class Reader(QDialog):
    def __init__(self, type, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Available Reader')

        self.readers = load_plugins(type)

        self.reader_widget = QComboBox()


        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

        self.layout.addWidget(self.reader_widget)
        self.button_select = QPushButton('Select')
        self.layout.addWidget(self.button_select)
        self.button_select.clicked.connect(self.choose)

    def set_file(self, file):
        self.reader_widget.clear()
        ext_plugins = defaultdict(list)
        for name, cls in self.readers.items():
            ext_plugins[cls._ext].append(name)
        if file.split('.')[-1] in ext_plugins.keys():
            for r in ext_plugins[file.split('.')[-1]]:
                self.reader_widget.addItem(r)

    def choose(self, file):
        self.choosen_reader = self.readers[self.reader_widget.currentText()]
        self.accept()
