import logging
from PyQt5.QtWidgets import QDialog, QPlainTextEdit, QVBoxLayout

from symupy.postprocess.visunet import logger
from symupy.postprocess.visunet.log import QTextEditLogger

class LoggerWidget(QDialog, QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.logTextBox = QTextEditLogger(self)
        # You can format what is printed to text box
        self.logTextBox.setFormatter(logging.Formatter('%(levelname)s: %(message)s', datefmt='%H:%M:%S'))
        logger.addHandler(self.logTextBox)
        # You can control the logging level
        logger.setLevel(logging.INFO)

        layout = QVBoxLayout()
        # Add the new logging box widget to the layout
        layout.addWidget(self.logTextBox.widget)
        self.setLayout(layout)

    def clearLog(self):
        self.logTextBox.widget.clear()

    def setLevelDebug(self):
        logger.setLevel(logging.DEBUG)

    def setLevelInfo(self):
        logger.setLevel(logging.INFO)

    def setLevelWarning(self):
        logger.setLevel(logging.WARNING)

    def setLevelError(self):
        logger.setLevel(logging.ERROR)
