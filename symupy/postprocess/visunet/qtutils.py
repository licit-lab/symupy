import functools
import logging
from inspect import signature, _empty

from PyQt5.QtCore import QThread, Qt, QObject, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QHBoxLayout,
    QSlider,
    QLabel,
    QComboBox,
    QLineEdit,
    QDialog,
    QFormLayout,
    QPushButton,
    QVBoxLayout,
)
from PyQt5.QtGui import QIntValidator


def waitcursor(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        value = func(*args, **kwargs)
        QApplication.restoreOverrideCursor()
        return value

    return wrapper


class ConsoleWindowLogHandler(logging.Handler, QObject):
    sigLog = pyqtSignal(str)

    def __init__(self):
        logging.Handler.__init__(self)
        QObject.__init__(self)
        self.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))

    def emit(self, logRecord):
        logRecord = self.format(logRecord)
        # message = str(logRecord.getMessage())
        self.sigLog.emit(logRecord)


class Slider(QWidget):
    def __init__(self, name=" ", parent=None):
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

        self.line_edit = QLineEdit("", self)
        self.line_edit.setFixedWidth(40)
        self.line_edit.setValidator(QIntValidator())
        self.line_edit.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.line_edit.editingFinished.connect(self.updateSlider)
        # self.line_edit.setMinimumWidth(80)

        # self.layout.addSpacing(5)
        self.layout.addWidget(self.line_edit)

        self.valueChanged = self.slider.valueChanged

    def updateLabel(self, value):
        self.line_edit.setText(str(value))

    def updateSlider(self):
        self.slider.setValue(int(self.line_edit.text()))

    def value(self):
        return self.slider.value()

    def setRange(self, min, max):
        self.slider.setRange(min, max)
        self.updateLabel(self.value())

    def setName(self, name):
        self.name.setText(name)


class LabelComboBox(QWidget):
    def __init__(self, name=" ", parent=None):
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


class LabelLineEdit(QWidget):
    def __init__(self, name=" ", parent=None):
        super().__init__(parent)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.name = QLabel(name, self)
        self.layout.addWidget(self.name)

        self.widget = QLineEdit()
        self.layout.addWidget(self.widget)

        self.name.setAlignment(Qt.AlignLeft)

    def value(self):
        return self.widget.text()


class Worker(QThread):
    def __init__(self, func, args):
        super(Worker, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.func(*self.args)


class TripSelector(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Choose Trip")

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

        self.vehid = LabelLineEdit("VEH id")
        self.layout.addWidget(self.vehid)
        self.button_select = QPushButton("Select")
        self.layout.addWidget(self.button_select)
        self.button_select.clicked.connect(self.select)

    def select(self):
        self.accept()


class ODSelector(QDialog):
    def __init__(self, func, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Choose OD")

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

        self.button_select = QPushButton("Select")
        self.layout.addWidget(self.button_select)
        self.button_select.clicked.connect(self.select)

        self.values = list()

    def select(self):
        for line_edit in self.widgets:
            self.values.append(line_edit.text())
        self.accept()
