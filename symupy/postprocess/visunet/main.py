import sys


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from symupy.postprocess.visunet.figure import MplWidget
from symupy.postprocess.visunet.panel import RightPanelWidget


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(QDesktopWidget().availableGeometry(self).size() * 0.7)

        self.data = DataContainer()

        self.layout = QHBoxLayout()
        self.widget = QGroupBox(None, self)
        self.widget.setLayout(self.layout)
        self.setWindowTitle('VisuNet')

        self.widget_mpl = MplWidget(self.data)
        self.layout.addWidget(self.widget_mpl)

        self.panel = RightPanelWidget(self.data)
        self.layout.addWidget(self.panel)


        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        self.menu()

    def menu(self):
        menubar = self.menuBar()
        if sys.platform == "darwin":
            menubar.setNativeMenuBar(False)

        fileMenu = QMenu("&File", self)
        menubar.addMenu(fileMenu)
        openAction = QAction("&Open...", self)
        fileMenu.addAction(openAction)
        openAction.triggered.connect(self.panel.panel_netw.load_network)
        openAction.setShortcut("Ctrl+O")






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


def launch_app(file=None):
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    if file is not None:
        w.data.file_network=file
        w.panel.panel_netw.plot_network()

    app.exec_()
