import logging

from PyQt5.QtWidgets import QVBoxLayout, QWidget, QTextEdit

from .network import NetworkWidget
from .trajectory import TrajectoryWidget
from symupy.postprocess.visunet.qtutils import ConsoleWindowLogHandler

from symupy.postprocess.visunet import logger

class RightPanelWidget(QWidget):
    def __init__(self, data, parent=None):
        super().__init__(parent=parent)
        self.data = data

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.panel_netw = NetworkWidget(self.data)
        self.layout.addWidget(self.panel_netw)

        self.logger_widget = QTextEdit()
        self.logger_widget.setReadOnly(True)
        self.layout.addWidget(self.logger_widget)

        consoleHandler = ConsoleWindowLogHandler()
        consoleHandler.sigLog.connect(self.logger_widget.append)
        logger.addHandler(consoleHandler)

        # self.panel_traj = TrajectoryWidget(self.data)
        # self.layout.addWidget(self.panel_traj)
