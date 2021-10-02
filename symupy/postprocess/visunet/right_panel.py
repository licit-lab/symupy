import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QTextEdit, QLabel, QGroupBox

# from .trajectory import TrajectoryWidget
from symupy.postprocess.visunet.qtutils import ConsoleWindowLogHandler

from symupy.postprocess.visunet import logger


class RightPanelWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

        self.labels = QGroupBox()
        self.labels.layout = QVBoxLayout()
        self.labels.setLayout(self.labels.layout)
        self.label_file_netw = QLabel("Network:")
        self.label_file_traj = QLabel("TrafficData:")
        self.label_file_netw.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.label_file_traj.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.labels.layout.addWidget(self.label_file_netw)
        self.labels.layout.addWidget(self.label_file_traj)
        self.layout.addWidget(self.labels)

        self.logger_widget = QTextEdit()
        self.logger_widget.setReadOnly(True)
        self.layout.addWidget(self.logger_widget)

        consoleHandler = ConsoleWindowLogHandler()
        consoleHandler.sigLog.connect(self.logger_widget.append)
        logger.addHandler(consoleHandler)

        # self.panel_traj = TrajectoryWidget(self.data)
        # self.layout.addWidget(self.panel_traj)

    def update_label_network(self, filename):
        self.label_file_netw.setText("Network: " + filename)

    def update_label_traffic_data(self, filename):
        self.label_file_traj.setText("TrafficData: " + filename)
