import functools

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QHBoxLayout, QSlider, QLabel,
                            QComboBox)


def waitcursor(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        value = func(*args, **kwargs)
        QApplication.restoreOverrideCursor()
        return value
    return wrapper

class Slider(QWidget):
    def __init__(self, name=' ', parent=None):
        super().__init__(parent)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.name = QLabel(name, self)
        self.layout.addWidget(self.name)

        self.slider = QSlider(Qt.Horizontal)
        # self.slider.setRange(min, max)
        self.slider.setFocusPolicy(Qt.NoFocus)
        self.slider.setPageStep(5)

        self.layout.addWidget(self.slider)

        self.slider.valueChanged.connect(self.updateLabel)

        self.label = QLabel('', self)
        self.label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        # self.label.setMinimumWidth(80)


        # self.layout.addSpacing(5)
        self.layout.addWidget(self.label)

        self.valueChanged = self.slider.valueChanged

    def updateLabel(self, value):
        self.label.setText(str(value))

    def value(self):
        return self.slider.value()

    def setRange(self, min, max):
        self.slider.setRange(min, max)
        self.updateLabel(self.value())

    def setName(self, name):
        self.name.setText(name)


class LabelComboBox(QWidget):
    def __init__(self, name=' ', parent=None):
        super().__init__(parent)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.name = QLabel(name, self)
        self.layout.addWidget(self.name)

        self.widget = QComboBox()
        self.layout.addWidget(self.widget)

        self.name.setAlignment(Qt.AlignLeft)

        self.currentIndexChanged = self.widget.currentIndexChanged

    def setItems(self, items):
        self.widget.clear()
        [self.widget.addItem(str(it)) for it in items]

    def setName(self, name):
        self.name.setText(name)

    def value(self):
        return self.widget.currentText()
