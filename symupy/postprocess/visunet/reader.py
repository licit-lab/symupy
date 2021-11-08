from collections import defaultdict

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox, QVBoxLayout, QPushButton, QDialog

from symupy.plugins.reader import load_plugins


class Reader(QDialog):
    def __init__(self, type, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Available Reader")

        self.readers = load_plugins(type)
        self.reader_widget = QComboBox()

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

        self.layout.addWidget(self.reader_widget)
        self.button_select = QPushButton("Select")
        self.layout.addWidget(self.button_select)
        self.button_select.clicked.connect(self.choose)

    def set_file(self, file):
        self.reader_widget.clear()
        ext_plugins = defaultdict(list)
        for name, cls in self.readers.items():
            ext_plugins[cls._ext].append(name)
        if file.split(".")[-1] in ext_plugins.keys():
            for r in ext_plugins[file.split(".")[-1]]:
                self.reader_widget.addItem(r)

    def choose(self, file):
        self.choosen_reader = self.readers[self.reader_widget.currentText()]
        self.accept()
