import sys

from PyQt5.QtWidgets import (QHBoxLayout, QGroupBox, QDesktopWidget, QMainWindow,
                             QApplication, QMenu, QAction, QFileDialog)
# from PyQt5.QtCore import QApplication
# from PyQt5.QtGui import *

from symupy.postprocess.visunet.figure import MplWidget
from symupy.postprocess.visunet.panel import RightPanelWidget
from symupy.plugins.reader import add_dir_to_plugin


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

        self.menubar = self.menuBar()
        if sys.platform == "darwin":
            self.menubar.setNativeMenuBar(False)

        self.fileMenu = QMenu("&File", self)
        self.menubar.addMenu(self.fileMenu)
        self.openAction = QAction("&Open...", self)
        self.fileMenu.addAction(self.openAction)
        self.openAction.triggered.connect(self.panel.panel_netw.load_network)
        self.openAction.setShortcut("Ctrl+O")

        self.pluginMenu = QMenu("&Plugins", self)
        self.menubar.addMenu(self.pluginMenu)
        self.addFolderAction = QAction("&Add folder...", self)
        self.pluginMenu.addAction(self.addFolderAction)
        self.addFolderAction.triggered.connect(self.add_plugins)


    def add_plugins(self):
        options = QFileDialog.Options(QFileDialog.Options(QFileDialog.DontUseNativeDialog))
        folder = str(QFileDialog.getExistingDirectory(self, "Load Plugins", "", options=options))
        print(folder)
        add_dir_to_plugin(folder)




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

if __name__ == '__main__':
    launch_app()
