import linecache
from collections import OrderedDict

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.lines import Line2D
from PyQt5.QtCore import Qt, pyqtSlot, QThread, pyqtSignal
from PyQt5.QtWidgets import (QFileDialog, QGroupBox, QLabel, QPushButton,
                             QRadioButton, QVBoxLayout, QProgressBar)

from symupy.postprocess.visunet.qtutils import waitcursor
from symupy.parser.symuvia import SymuviaNetworkReader
from symupy.renderer.network import draw_network, NetworkRenderer

class NetworkWidget(QGroupBox):
    def __init__(self, data, name=None, parent=None):
        super().__init__(name, parent)
        self.data = data

        self.file_network = None
        self.tree_network = None

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)


        self.button_load_network = QPushButton('Render')
        self.button_load_network.clicked.connect(self.load_network)
        self.layout.addWidget(self.button_load_network)

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

    # def update_show_public(self):
    #     self.data.public_transport = self.show_public_transport.isChecked()
    #
    # @waitcursor
    # def process_network(self):
    #     if self.data.file_network:
    #         self.data.tree_network = etree.parse(self.data.file_network)
    #         self.update_label()
    #
    #         comments = self.data.tree_network.xpath('//comment()')
    #         for c in comments:
    #             p = c.getparent()
    #             p.remove(c)
    #         self.data.troncons_coords = OrderedDict()
    #         troncons = self.data.tree_network.find('//RESEAU/TRONCONS')
    #         for tr in troncons.iterchildren():
    #             try:
    #                 amont = np.fromstring(tr.attrib['extremite_amont'], sep=' ')
    #             except KeyError:
    #                 print(type(tr))
    #             if tr.getchildren():
    #                 elt = tr.getchildren()[0].getchildren()
    #                 amont = np.row_stack([amont]+[np.fromstring(e.attrib['coordonnees'], sep=' ') for e in elt if 'coordonnees' in e.keys()])
    #             aval = np.fromstring(tr.attrib['extremite_aval'], sep=' ')
    #             arr = np.row_stack((amont, aval))
    #             self.data.troncons_coords[tr.attrib['id']] = arr
    #
    #         print(f"loaded network: {self.data.file_network.split('/')[-1]}")
    #         self.plot_network()


    def load_network(self):
        options = QFileDialog.Options(QFileDialog.Options(QFileDialog.DontUseNativeDialog))
        file, _ = QFileDialog.getOpenFileName(self,"Load Network", "","Network file (*.xml)", options=options)

        if file != '':
            self.data.file_network = file
            self.process_network()
            self.plot_network()

    @waitcursor
    def process_network(self):
        reader = SymuviaNetworkReader(self.data.file_network)
        self.network = reader.get_network()
        self.update_label()
        self.renderer = NetworkRenderer(self.network, self.data.figure)


    def plot_network(self):
        self.data.figure.clf()
        self.renderer.draw()
        plt.axis('tight')
        self.data.figure.gca().set_aspect('equal')
        self.data.canvas.draw()
        print('Done')
