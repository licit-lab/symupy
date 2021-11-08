import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QSizePolicy, QVBoxLayout, QWidget, QFileDialog

matplotlib.use("Qt5Agg")


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100, fig=None):
        super(MplCanvas, self).__init__(fig)


class MPLWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.figure = plt.figure()
        self.figure.gca().set_aspect("equal")
        self.canvas = MplCanvas(self, fig=self.figure, width=5, height=4, dpi=100)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.figure.gca().plot()
        self.figure.gca().axis("off")

        self.toolbar = NavigationToolbar(self.canvas, self)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.toolbar)
