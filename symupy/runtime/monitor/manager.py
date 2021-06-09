import sys
import types

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pyqtgraph as pg

from symupy.postprocess.visunet.qtutils import Worker


class LineMonitorView():
    def __init__(self, title, x_label, y_label, nb_plots=1, colors=['w', 'g', 'b', 'c', 'm', 'y', 'r'], line_labels=None, aggregation_period=1):
        self.plots = [None for _ in range(nb_plots)]
        self.title = title
        self.labels = (x_label, y_label)

        self.x = [[] for _ in range(nb_plots)]
        self.y = [[] for _ in range(nb_plots)]

        self._plot_kwargs = {}

        self.colors = [colors[i] for i in range(nb_plots)]

        if line_labels is None:
            self.line_labels = [None for i in range(nb_plots)]
        else:
            self.line_labels = line_labels

        self.aggregation_period = aggregation_period

    def add_plot(self, plot):
        plot.addLegend()
        for i in range(len(self.plots)):
            self.plots[i] = plot.plot([], [], self._plot_kwargs, name=self.line_labels[i])


    def _update_plot(self, step, string):
        for i, p in enumerate(self.plots):
            x_val, y_val = self.update(step, string, i)
            if (x_val, y_val) != (None, None):
                self.x[i].append(x_val)
                self.y[i].append(y_val)

                kwargs = {"pen":self.colors[i]}
                kwargs.update(self._plot_kwargs)

                p.setData(self.x[i], self.y[i], **kwargs, name="test")

    def update(self, step, string, ind):
        raise NotImplementedError


class ScatterMonitorView(LineMonitorView):
    def __init__(self, title, x_label, y_label, symbol="+", nb_plots=1, aggregation_period=1):
        super(ScatterMonitorView, self).__init__(title, x_label, y_label, nb_plots=nb_plots, aggregation_period=aggregation_period)
        self._plot_kwargs = {"pen":None, "symbol":symbol}


class MonitorManager():
    def __init__(self):
        pg.setConfigOptions(antialias=True)
        self.monitors = []
        self.widget = pg.GraphicsLayoutWidget(show=True, title="SymuPy Monitor")

    def add_monitor(self, monitor, row, col, rowspan=1, colspan=1):
        plot = self.widget.addPlot(row, col, rowspan, colspan, title=monitor.title, labels={'left': (monitor.labels[1]), 'bottom': (monitor.labels[0])})
        monitor.add_plot(plot)

        self.monitors.append(monitor)

    def update(self, step, string):
        [monitor._update_plot(step, string) for monitor in self.monitors]


class MonitorApp(QMainWindow):
    _app = QApplication(sys.argv)

    def __init__(self, *args, **kwargs):
        super(MonitorApp, self).__init__(*args, **kwargs)

        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        self.run = QPushButton("Run")
        self.stop = QPushButton("Stop")
        self.run.clicked.connect(self.launch_simulation)
        self.stop.clicked.connect(self.set_stop)
        self.layout.addWidget(self.run)
        self.layout.addWidget(self.stop)

        self.monitor_manager = MonitorManager()
        self.layout.addWidget(self.monitor_manager.widget)

        self.stop_flag = False

        self.feeder = None

    def add_monitor(self, monitor, row, col, rowspan=1, colspan=1):
        self.monitor_manager.add_monitor(monitor, row, col, rowspan=rowspan, colspan=colspan)

    def run_simulation(self):
        self.stop_flag = False
        self.process = Worker(self.launch_simulation, [])
        self.process.start()

    def set_stop(self):
        self.stop_flag = True

    def set_feeder(self, feeder):
        assert isinstance(feeder, types.GeneratorType)
        self.feeder = feeder

    def launch_simulation(self):
        self.stop_flag = False
        for step, res in self.feeder:
            if not self.stop_flag:
                self.monitor_manager.update(step, res)
                pg.QtGui.QApplication.processEvents()
            else:
                break

    def launch_app(self):
        self.show()
        sys.exit(MonitorApp._app.exec_())