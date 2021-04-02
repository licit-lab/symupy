import linecache
from collections import OrderedDict, defaultdict
import time

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
# from symupy.parser.symuvia import SymuviaNetworkReader
from symupy.renderer.network import draw_network, NetworkRenderer
from symupy.plugins.reader import load_plugins

class NetworkWidget(QGroupBox):
    def __init__(self, data, name=None, parent=None):
        super().__init__(name, parent)
        self.data = data

        self.file_network = None
        self.tree_network = None

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)


        self.label_file_netw = QLabel('File:')
        self.label_file_netw.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.layout.addWidget(self.label_file_netw)
        self.label_tr = QLabel('Troncons:')
        self.label_tr.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.layout.addWidget(self.label_tr)

        self.network = None
        self.renderer = None
        self.reader = Reader()


    def update_label(self):
        file = self.data.file_network.split('/')[-1]
        self.label_file_netw.setText('File: '+file)
        tr = len(self.network.links)
        self.label_tr.setText('Troncons: '+str(tr))

    def choose_reader(self):
        self.reader.set_file(self.data.file_network)
        if self.reader.exec_() == QDialog.Accepted:
            logger.debug(f'Choose reader {self.reader.choosen_reader}')
            reader = self.reader.choosen_reader
            self.workerProcessNet = Worker(process_network, [self, reader])
            self.workerPlotNet = Worker(plot_network, [self])
            self.workerProcessNet.finished.connect(self.workerPlotNet.start)
            self.workerProcessNet.start()

    def load_network(self):
        options = QFileDialog.Options(QFileDialog.Options(QFileDialog.DontUseNativeDialog))
        file, _ = QFileDialog.getOpenFileName(self,"Load Network", "","Network file (*)", options=options)

        if file != '':
            self.data.file_network = file
            self.choose_reader()
            # self.process_network()
            # self.plot_network()

@waitcursor
def process_network(networkwidget, reader):
    logger.info(f'Creating Network object ...')
    start = time.time()
    reader = reader(networkwidget.data.file_network)
    networkwidget.network = reader.get_network()
    end = time.time()
    logger.info(f'Done [{end-start} s]')
    networkwidget.update_label()
    networkwidget.renderer = NetworkRenderer(networkwidget.network, networkwidget.data.figure)


def plot_network(networkwidget):
    logger.info(f'Rendering Network object ...')
    start = time.time()
    networkwidget.data.figure.clf()
    networkwidget.renderer.draw()
    plt.axis('off')
    plt.axis('tight')
    networkwidget.data.figure.gca().set_aspect('equal')
    networkwidget.data.canvas.draw()
    end = time.time()
    logger.info(f'Done [{end-start} s]')


class Reader(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Available Reader')

        self.readers = load_plugins('input')

        self.reader_widget = QComboBox()


        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

        self.layout.addWidget(self.reader_widget)
        self.button_select = QPushButton('Select')
        self.layout.addWidget(self.button_select)
        self.button_select.clicked.connect(self.choose)

    def set_file(self, file):
        ext_plugins = defaultdict(list)
        for name, cls in self.readers.items():
            ext_plugins[cls._ext].append(name)
        if file.split('.')[-1] in ext_plugins.keys():
            for r in ext_plugins[file.split('.')[-1]]:
                self.reader_widget.addItem(r)

    def choose(self, file):
        self.choosen_reader = self.readers[self.reader_widget.currentText()]
        self.accept()
