import linecache
from collections import OrderedDict, defaultdict

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.lines import Line2D
from PyQt5.QtCore import Qt, pyqtSlot, QThread, pyqtSignal
from PyQt5.QtWidgets import (QFileDialog, QGroupBox, QLabel, QPushButton,
                             QRadioButton, QVBoxLayout, QProgressBar, QDesktopWidget,
                             QWidget, QComboBox, QDialog)
from PyQt5.Qt import QRect

from symupy.postprocess.visunet.qtutils import waitcursor
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


        # self.button_load_network = QPushButton('Render')
        # self.button_load_network.clicked.connect(self.load_network)
        # self.layout.addWidget(self.button_load_network)

        # self.show_public_transport = QRadioButton('Show public transport')
        # self.show_public_transport.setChecked(False)
        # self.layout.addWidget(self.show_public_transport)
        # self.show_public_transport.toggled.connect(self.update_show_public)


        self.label_file_netw = QLabel('File:')
        self.label_file_netw.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.layout.addWidget(self.label_file_netw)
        self.label_tr = QLabel('Troncons:')
        self.label_tr.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.layout.addWidget(self.label_tr)

        self.network = None
        self.renderer = None

    def update_label(self):
        file = self.data.file_network.split('/')[-1]
        self.label_file_netw.setText('File: '+file)
        tr = len(self.network.links)
        self.label_tr.setText('Troncons: '+str(tr))

    def choose_reader(self):
        self.reader = Reader(self.data.file_network)
        if self.reader.exec_() == QDialog.Accepted:
            reader = self.reader.choosen_reader
            self.process_network(reader)
            self.plot_network()
        # geom = QRect(0, 0, 200, 400)
        # centerPoint = QDesktopWidget().availableGeometry().center()
        # geom.moveCenter(centerPoint)
        # self.reader.setGeometry(geom)


    def load_network(self):
        options = QFileDialog.Options(QFileDialog.Options(QFileDialog.DontUseNativeDialog))
        file, _ = QFileDialog.getOpenFileName(self,"Load Network", "","Network file (*)", options=options)



        if file != '':
            self.data.file_network = file
            self.choose_reader()
            # self.process_network()
            # self.plot_network()

    @waitcursor
    def process_network(self, reader):
        reader = reader(self.data.file_network)
        self.network = reader.get_network()
        self.update_label()
        self.renderer = NetworkRenderer(self.network, self.data.figure)


    def plot_network(self):
        self.data.figure.clf()
        self.renderer.draw()
        plt.axis('off')
        plt.axis('tight')
        self.data.figure.gca().set_aspect('equal')
        self.data.canvas.draw()
        print('Done')


class Reader(QDialog):
    def __init__(self, file, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Available Reader')

        self.readers = load_plugins('input')

        ext_plugins = defaultdict(list)
        for name, cls in self.readers.items():
            ext_plugins[cls._ext].append(name)

        self.reader_widget = QComboBox()
        if file.split('.')[-1] in ext_plugins.keys():
            for r in ext_plugins[file.split('.')[-1]]:
                self.reader_widget.addItem(r)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

        self.layout.addWidget(self.reader_widget)
        self.button_select = QPushButton('Select')
        self.layout.addWidget(self.button_select)
        self.button_select.clicked.connect(self.choose)

        # self.show()

    def choose(self):
        self.choosen_reader = self.readers[self.reader_widget.currentText()]
        self.accept()
