import linecache
from collections import OrderedDict

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.lines import Line2D
from PyQt5.QtCore import Qt, pyqtSlot, QThread, pyqtSignal
from PyQt5.QtWidgets import (QFileDialog, QGroupBox, QLabel, QPushButton,
                             QRadioButton, QVBoxLayout, QProgressBar)

from symupy.postprocess.visunet.qtutils import waitcursor
from symupy.parser.xmlparser import XMLParser

class NetworkWidget(QGroupBox):
    def __init__(self, data, name='Network', parent=None):
        super().__init__(name, parent)
        self.data = data

        self.file_network = None
        self.tree_network = None

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)


        self.button_load_network = QPushButton('Load Network')
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

        self.data.legend_network = None

    def update_label(self):
        file = self.data.file_network.split('/')[-1]
        self.label_file_netw.setText('File: '+file)
        tr = len(self.data.troncons_coords)
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
            print(file)
            self.data.file_network = file
            self.plot_network()

    def process_network(self):
        parser = XMLParser(self.data.file_network)
        root = parser.get_root()
        if root.tag == "OUT":
            troncons_elem = parser.xpath("OUT/IN/RESEAU/TRONCONS")
        elif root.tag == "ROOT_SYMUBRUIT":
            troncons_elem = parser.xpath("ROOT_SYMUBRUIT/RESEAUX/RESEAU/TRONCONS")

        troncons_coords = list()
        self.data.troncons_coords = OrderedDict()
        for elem in troncons_elem.iterchildrens():
            amont = np.fromstring(elem.attr['extremite_amont'], sep=' ')
            aval = np.fromstring(elem.attr['extremite_aval'], sep=' ')
            internal_points = elem.find_children_tag('POINTS_INTERNES')
            if internal_points is not None:
                coords = [np.fromstring(ip.attr['coordonnees'], sep=' ') for ip in internal_points.iterchildrens()]
                coords = [amont]+coords+[aval]

            else:
                coords = [amont]+[aval]
            self.data.troncons_coords[elem.attr['id']] = coords
        self.update_label()


    @waitcursor
    def plot_network(self):
        self.data.figure.clf()
        self.process_network()
        troncons_coords = np.row_stack([arr + [[None, None]] for arr in self.data.troncons_coords.values()])
        self.data.figure.gca().plot(
            troncons_coords[:, 0],
            troncons_coords[:, 1],
            "k",
            label="Network",
            alpha=0.7,
            linewidth=1,
        )

        plt.axis('tight')
        self.data.figure.gca().set_aspect('equal')
        self.data.canvas.draw()
        print('Done')
