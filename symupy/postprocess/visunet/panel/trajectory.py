from inspect import signature, _empty

from symupy.postprocess.visunet.qtutils import LabelLineEdit

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QDialog, QLineEdit, QLabel, QPushButton, QFormLayout, QVBoxLayout)

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


class ODSelector(QDialog):
    def __init__(self, func, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Choose OD')

        self.layout = QFormLayout()
        self.setLayout(self.layout)

        sig = signature(func)
        self.widgets = list()
        maxsize = max([len(item) for item in sig.parameters.keys()])
        for name, param in sig.parameters.items():
            label = QLabel(name)
            edit = QLineEdit()
            self.widgets.append(edit)
            self.layout.addRow(label, edit)
            if param.default != _empty:
                edit.setText(str(param.default))

        self.button_select = QPushButton('Select')
        self.layout.addWidget(self.button_select)
        self.button_select.clicked.connect(self.select)

        self.values = list()

    def select(self):
        for line_edit in self.widgets:
            self.values.append(line_edit.text())
        self.accept()
