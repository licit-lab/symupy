import time

import matplotlib.pyplot as plt
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QDialog,
    QGridLayout,
    QLabel,
    QVBoxLayout,
    QPushButton,
)

from symupy.postprocess.visunet import logger
from symupy.postprocess.visunet.mplfigure import MPLWidget
from symupy.postprocess.visunet.qtutils import Worker
from symupy.postprocess.visunet.reader import Reader
from symupy.renderer.network import NetworkRenderer


class NetworkWidget(QWidget):
    def __init__(self, parent=None):
        super(NetworkWidget, self).__init__(parent=parent)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.mpl_widget = MPLWidget()
        self.layout.addWidget(self.mpl_widget)

        self.reader = Reader("input")
        self.renderer = None
        self.network = None

    def choose_reader(self, file):
        self.reader.set_file(file)
        if self.reader.exec_() == QDialog.Accepted:
            self.mpl_widget.figure.clf()
            logger.debug(f"Choose reader {self.reader.choosen_reader}")
            self.process = Worker(self._process_network, [file])
            self.plot = Worker(self._plot_network, [])
            self.process.finished.connect(self.plot.start)
            self.process.start()

    def _process_network(self, file):
        logger.info(f"Creating Network object ...")
        start = time.time()
        reader = self.reader.choosen_reader(file)
        self.network = reader.get_network()
        end = time.time()
        logger.info(f"Done [{end - start:.4f} s]")

    def _plot_network(self):
        self.renderer = NetworkRenderer(
            self.network, self.mpl_widget.figure, callbackpicking=self._showlink
        )
        logger.info(f"Rendering Network object ...")
        start = time.time()
        self.mpl_widget.figure.clf()
        self.renderer.draw_network()
        plt.axis("off")
        plt.axis("tight")
        self.mpl_widget.figure.gca().set_aspect("equal")
        end = time.time()
        logger.info(f"Done [{end - start:.4f} s]")

    def _showlink(self, link):
        infowidget = LinkInfo(link, parent=self.parent().parent())
        infowidget.show()
        # if widget.exec_() == QDialog.Accepted:
        #     pass

    def clear(self):
        if self.renderer is not None:
            logger.info("Clearing Renderer routes")
            self.renderer.clear()


class LinkInfo(QDialog):
    def __init__(self, link, parent=None):
        super().__init__(parent)
        nameLabel = QLabel(f"Id: {link.id}")

        # self.layout = QVBoxLayout()
        # self.layout.addWidget(nameLabel)

        self.layout = QGridLayout()
        labid = QLabel(link.id)
        labid.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.layout.addWidget(QLabel("Id:"), 0, 0)
        self.layout.addWidget(labid, 0, 1)
        self.layout.addWidget(QLabel("Upstream Node:"), 1, 0)
        labun = QLabel(link.upstream_node)
        labun.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.layout.addWidget(labun, 1, 1)
        self.layout.addWidget(QLabel("Downstream Node:"), 2, 0)
        labdn = QLabel(link.downstream_node)
        labdn.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.layout.addWidget(labdn, 2, 1)
        self.layout.addWidget(QLabel("Nb Lane:"), 3, 0)
        self.layout.addWidget(QLabel(str(link.nb_lanes)), 3, 1)
        self.layout.addWidget(QLabel("Speed limit:"), 4, 0)
        self.layout.addWidget(QLabel(str(link.speed_limit)), 4, 1)

        self.setLayout(self.layout)
        # self.setGeometry(300, 300, 250, 150)
        self.sizeHint()
        self.setWindowTitle("Link Info")
