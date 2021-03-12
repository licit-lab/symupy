import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDesktopWidget, QHBoxLayout, QWidget

from symupy.postprocess.visunet.figure import MplWidget
from symupy.postprocess.visunet.panel import RightPanelWidget


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.resize(QDesktopWidget().availableGeometry(self).size() * 0.7)

        self.data = DataContainer()

        self.layout = QHBoxLayout()
        self.widget = QWidget(self)
        self.widget.setLayout(self.layout)
        self.setWindowTitle('VisuNet')

        self.widget_mpl = MplWidget(self.data)
        self.layout.addWidget(self.widget_mpl)

        self.panel = RightPanelWidget(self.data)
        self.layout.addWidget(self.panel)


        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        self.show()

class DataContainer(object):
    def __init__(self):
        self.figure = None
        self.canvas = None
        self.file_network = None
        self.tree_network = None
        self.file_traj = None
        self.struct_traj = None
        self.traj_plot = list()
        self.troncons_coords = dict()
        self.legend_network = None
        self.public_transport = None


def launch_app():
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    app.exec_()
