from symupy.postprocess.visunet.qtutils import LabelLineEdit

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QDialog, QComboBox, QVBoxLayout, QPushButton)

class TripSelector(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Choose Trip')

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

        self.vehid = LabelLineEdit('VEH id')
        self.layout.addWidget(self.vehid)
        self.button_select = QPushButton('Select')
        self.layout.addWidget(self.button_select)
        self.button_select.clicked.connect(self.select)

    def select(self):
        self.accept()
