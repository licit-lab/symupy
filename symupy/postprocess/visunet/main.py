import sys
import logging


from PyQt5.QtWidgets import (QHBoxLayout, QGroupBox, QDesktopWidget, QMainWindow,
                             QApplication, QMenu, QAction, QFileDialog, QSplitter,
                             QActionGroup)
from PyQt5.QtCore import Qt
# from PyQt5.QtGui import *

from symupy.postprocess.visunet import logger
from symupy.postprocess.visunet.figure import MplWidget
from symupy.postprocess.visunet.panel import RightPanelWidget
from symupy.plugins.reader import add_dir_to_plugin

logger.setLevel(logging.INFO)

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(QDesktopWidget().availableGeometry(self).size() * 0.7)

        self.data = DataContainer()

        # self.layout = QHBoxLayout()
        self.widget = QSplitter(Qt.Horizontal)
        # self.widget.setLayout(self.layout)
        self.setWindowTitle('VisuNet')

        self.widget_mpl = MplWidget(self.data)
        self.widget.addWidget(self.widget_mpl)

        self.panel = RightPanelWidget(self.data)
        self.widget.addWidget(self.panel)


        # self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        self.menubar = self.menuBar()
        if sys.platform == "darwin":
            self.menubar.setNativeMenuBar(False)

        self.fileMenu = QMenu("&Network", self)
        self.menubar.addMenu(self.fileMenu)
        self.openNetAction = QAction("&Open...", self)
        self.fileMenu.addAction(self.openNetAction)
        self.openNetAction.triggered.connect(self.panel.panel_netw.load_network)
        self.openNetAction.setShortcut("Ctrl+N")

        self.trajMenu = QMenu("&Trajectories", self)
        self.menubar.addMenu(self.trajMenu)
        self.openTrajAction = QAction("&Open...", self)
        self.trajMenu.addAction(self.openTrajAction)
        self.openTrajAction.setShortcut("Ctrl+T")
        self.renderTripAction = QAction("&Render Trip...", self)
        self.trajMenu.addAction(self.renderTripAction)
        self.renderODAction = QAction("&Render OD...", self)
        self.trajMenu.addAction(self.renderODAction)
        self.clearAction = QAction("&Clear", self)
        self.trajMenu.addAction(self.clearAction)

        self.pluginMenu = QMenu("&Plugins", self)
        self.menubar.addMenu(self.pluginMenu)
        self.submenuReader = self.pluginMenu.addMenu('&Reader')
        self.addFolderAction = QAction("&Add folder...", self)
        self.submenuReader.addAction(self.addFolderAction)
        self.addFolderAction.triggered.connect(self.add_plugins)

        self.logMenu = QMenu("&Log", self)
        self.menubar.addMenu(self.logMenu)
        self.submenuLogger = self.logMenu.addMenu('&Level')
        self.levelGroup = QActionGroup(self)
        self.levelDBGAction = QAction("&Debug", self)
        self.levelINFAction = QAction("&Info", self)
        self.levelWRNAction = QAction("&Warning", self)
        self.levelERRAction = QAction("&Error", self)
        self.levelDBGAction.setCheckable(True)
        self.levelINFAction.setCheckable(True)
        self.levelWRNAction.setCheckable(True)
        self.levelERRAction.setCheckable(True)
        self.submenuLogger.addAction(self.levelDBGAction)
        self.submenuLogger.addAction(self.levelINFAction)
        self.submenuLogger.addAction(self.levelWRNAction)
        self.submenuLogger.addAction(self.levelERRAction)
        self.levelGroup.addAction(self.levelDBGAction)
        self.levelGroup.addAction(self.levelINFAction)
        self.levelGroup.addAction(self.levelWRNAction)
        self.levelGroup.addAction(self.levelERRAction)
        self.levelDBGAction.triggered.connect(self.setLoggerLevelDBG)
        self.levelINFAction.triggered.connect(self.setLoggerLevelINF)
        self.levelWRNAction.triggered.connect(self.setLoggerLevelWRN)
        self.levelERRAction.triggered.connect(self.setLoggerLevelERR)
        self.levelINFAction.setChecked(True)
        self.clearLogAction = QAction("&Clear", self)
        self.logMenu.addAction(self.clearLogAction)
        self.clearLogAction.triggered.connect(self.clearLog)


    def add_plugins(self):
        options = QFileDialog.Options(QFileDialog.Options(QFileDialog.DontUseNativeDialog))
        folder = str(QFileDialog.getExistingDirectory(self, "Load Plugins", "", options=options))
        if folder!='':
            add_dir_to_plugin(folder)

    def setLoggerLevelDBG(self):
        logger.setLevel(logging.DEBUG)

    def setLoggerLevelINF(self):
        logger.setLevel(logging.INFO)

    def setLoggerLevelWRN(self):
        logger.setLevel(logging.WARNING)

    def setLoggerLevelERR(self):
        logger.setLevel(logging.ERROR)

    def clearLog(self):
        self.panel.logger_widget.clear()

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
