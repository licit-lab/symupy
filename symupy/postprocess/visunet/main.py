import sys
import logging


from PyQt5.QtWidgets import (
    QHBoxLayout,
    QGroupBox,
    QDesktopWidget,
    QMainWindow,
    QApplication,
    QMenu,
    QAction,
    QFileDialog,
    QSplitter,
    QActionGroup,
    QDialog,
)
from PyQt5.QtCore import Qt

from symupy.postprocess.visunet import logger
from symupy.postprocess.visunet.network import NetworkWidget
from symupy.postprocess.visunet.qtutils import TripSelector, ODSelector
from symupy.postprocess.visunet.right_panel import RightPanelWidget
from symupy.plugins.reader import add_dir_to_plugin
from symupy.postprocess.visunet.routes import RoutesHandler

logger.setLevel(logging.INFO)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(QDesktopWidget().availableGeometry(self).size() * 0.7)

        self.layout = QSplitter(Qt.Horizontal)
        self.setCentralWidget(self.layout)

        self.setWindowTitle("VisuNet")

        self.netWidget = NetworkWidget(parent=self)
        self.layout.addWidget(self.netWidget)
        self.panel = RightPanelWidget(parent=self)
        self.layout.addWidget(self.panel)

        self.routes = RoutesHandler()

        self.initMenu()

    def initMenu(self):
        self.menubar = self.menuBar()
        if sys.platform == "darwin":
            self.menubar.setNativeMenuBar(False)

        self.fileMenu = QMenu("&Network", self)
        self.menubar.addMenu(self.fileMenu)
        self.openNetAction = QAction("&Open...", self)
        self.fileMenu.addAction(self.openNetAction)
        self.openNetAction.triggered.connect(self.open_network)
        self.openNetAction.setShortcut("Ctrl+N")

        self.routeMenu = QMenu("&Routes", self)
        self.menubar.addMenu(self.routeMenu)
        self.openTrajAction = QAction("&Open...", self)
        self.openTrajAction.triggered.connect(self.open_traffic_data)
        self.routeMenu.addAction(self.openTrajAction)
        self.openTrajAction.setShortcut("Ctrl+T")
        self.renderPathAction = QAction("&Render Path...", self)
        self.renderPathAction.setDisabled(True)
        self.renderPathAction.triggered.connect(self.select_path)
        self.routeMenu.addAction(self.renderPathAction)
        self.renderODAction = QAction("&Render OD...", self)
        self.routeMenu.addAction(self.renderODAction)
        self.renderODAction.triggered.connect(self.selectOD)
        self.renderODAction.setDisabled(True)
        self.renderTripAction = QAction("&Render Trip...", self)
        self.renderTripAction.setDisabled(True)
        self.renderTripAction.triggered.connect(self.select_trip)
        self.routeMenu.addAction(self.renderTripAction)

        self.exportAction = QAction("&Export...", self)
        self.routeMenu.addAction(self.exportAction)
        self.exportAction.triggered.connect(self.routes.export_csv)

        self.clearAction = QAction("&Clear", self)
        self.routeMenu.addAction(self.clearAction)
        self.clearAction.triggered.connect(self.netWidget.clear)

        self.pluginMenu = QMenu("&Plugins", self)
        self.menubar.addMenu(self.pluginMenu)
        self.submenuReader = self.pluginMenu.addMenu("&Reader")
        self.addFolderAction = QAction("&Add folder...", self)
        self.submenuReader.addAction(self.addFolderAction)
        self.addFolderAction.triggered.connect(self.add_plugins)

        self.logMenu = QMenu("&Log", self)
        self.menubar.addMenu(self.logMenu)
        self.submenuLogger = self.logMenu.addMenu("&Level")
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

    def open_network(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "Load Network", options=QFileDialog.DontUseNativeDialog
        )

        if file != "":
            self.netWidget.choose_reader(file)
            self.panel.update_label_network(file.split("/")[-1])

    def open_traffic_data(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "Load Traffic Data", options=QFileDialog.DontUseNativeDialog
        )
        self.routes.clear()
        self.routes.addRenderer(self.netWidget.renderer)
        if file != "":
            self.routes.choose_reader(file)
            self.panel.update_label_traffic_data(file.split("/")[-1])
            reader = self.routes.reader
            if hasattr(reader, "get_path") and callable(getattr(reader, "get_path")):
                self.renderPathAction.setDisabled(False)
            else:
                self.renderPathAction.setDisabled(True)
            if hasattr(reader, "get_OD") and callable(getattr(reader, "get_OD")):
                self.renderODAction.setDisabled(False)
            else:
                self.renderODAction.setDisabled(True)
            if hasattr(reader, "get_trip") and callable(getattr(reader, "get_trip")):
                self.renderTripAction.setDisabled(False)
            else:
                self.renderTripAction.setDisabled(True)

    def select_path(self):
        trip_selector = TripSelector()
        if trip_selector.exec_() == QDialog.Accepted:
            vehid = trip_selector.vehid.value()
            if vehid != "":
                logger.info(f"Looking for path {vehid} and plotting it ...")
                self.routes.addPath(vehid)

    def select_trip(self):
        trip_selector = TripSelector()
        if trip_selector.exec_() == QDialog.Accepted:
            vehid = trip_selector.vehid.value()
            if vehid != "":
                logger.info(f"Looking for trip {vehid} and plotting it ...")
                self.routes.addTrip(vehid)

    def selectOD(self):
        OD_selector = ODSelector(self.routes.reader.get_OD)
        if OD_selector.exec_() == QDialog.Accepted:
            args = [None if arg == "None" else arg for arg in OD_selector.values]
            self.routes.addOD(args)

    def add_plugins(self):
        options = QFileDialog.Options(
            QFileDialog.Options(QFileDialog.DontUseNativeDialog)
        )
        folder = str(
            QFileDialog.getExistingDirectory(self, "Load Plugins", "", options=options)
        )
        if folder != "":
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


def launch_app(file=None):
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    if file is not None:
        w.data.file_network = file
        w.panel.panel_netw.plot_network()

    app.exec_()


if __name__ == "__main__":
    launch_app()
