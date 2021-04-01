from PyQt5.QtWidgets import QVBoxLayout, QWidget

from .network import NetworkWidget
from .trajectory import TrajectoryWidget


class RightPanelWidget(QWidget):
    def __init__(self, data, parent=None):
        super().__init__(parent=parent)
        self.data = data

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.panel_netw = NetworkWidget(self.data)
        self.layout.addWidget(self.panel_netw)

        # self.panel_traj = TrajectoryWidget(self.data)
        # self.layout.addWidget(self.panel_traj)
