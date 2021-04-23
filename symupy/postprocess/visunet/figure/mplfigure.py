import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import \
    NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QSizePolicy, QVBoxLayout, QWidget

matplotlib.use('Qt5Agg')

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100, fig=None):
        super(MplCanvas, self).__init__(fig)

class MplWidget(QWidget):
    def __init__(self, data, parent=None):
        super().__init__(parent=parent)
        self.data = data

        self.data.figure = plt.figure(0)
        self.data.figure.gca().set_aspect('equal')
        self.data.canvas = MplCanvas(self,fig=self.data.figure, width=5, height=4, dpi=100)
        self.data.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.data.figure.gca().plot()
        self.data.figure.gca().axis('off')

        self.toolbar = NavigationToolbar(self.data.canvas, self)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(self.data.canvas)
        self.layout.addWidget(self.toolbar)
