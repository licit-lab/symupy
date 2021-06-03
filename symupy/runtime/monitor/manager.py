import time

import numpy as np
import matplotlib.pyplot as plt


class Monitor(object):
    def __init__(self, x_label, y_label, title, use_grid=True, style='-k', alpha=0.8):
        self.ax = None

        self.use_grid = use_grid
        self.x_label = x_label
        self.y_label = y_label
        self.title = title
        self.style = style
        self.alpha = alpha

        self.line = None
        self.x = []
        self.y = []

        self.simulator = None

    def set_axe(self, axe):
        self.ax = axe
        self.ax.set_xlabel(self.x_label)
        self.ax.set_ylabel(self.y_label)
        self.ax.set_title(self.title)

        if self.use_grid:
            self.ax.grid(True)

    def start(self):
        #print("Starting Monitor", self.__class__.__name__)
        self.line = self.ax.plot([], [], self.style, alpha=self.alpha)[0]

    def _update_graph(self, step, string):
        #print("Update Graph", self.__class__.__name__)

        x_val, y_val = self.update(step, string)

        #print(x_val, y_val)
        if (x_val, y_val) != (None, None):
            start = time.time()
            self.x.append(x_val)
            self.y.append(y_val)


            self.line.set_ydata(self.y)
            self.line.set_xdata(self.x)


            if np.min(self.y) <= self.line.axes.get_ylim()[0] or np.max(self.y) >= self.line.axes.get_ylim()[1]:
                self.line.axes.set_ylim([np.min(self.y) - np.std(self.y), np.max(self.y) + np.std(self.y)])

            if np.max(self.x) >= self.line.axes.get_xlim()[1]:
                self.line.axes.set_xlim([np.min(self.x) - 1, np.max(self.x) + 1])
            print(f"  Time update {self.__class__.__name__}:", time.time() - start)



    def end(self):
        plt.ioff()

    def update(self, step, string):
        raise NotImplementedError


class MonitorManager(object):
    def __init__(self, figsize=(16, 9)):
        self.fig = plt.figure(figsize=figsize)
        self.monitors = []

    def add_monitor(self, monitor, pos):
        ax = self.fig.add_subplot(pos)
        monitor.set_axe(ax)
        self.monitors.append(monitor)

    def update(self, step, string):
        #print("Manager update", step, string)
        self.fig.suptitle(f"Step {step}", fontsize=16)
        start = time.time()
        [monitor._update_graph(step, string) for monitor in self.monitors]
        plt.pause(1e-5)
        print(" Total time update:", time.time() - start)

    def end(self):
        plt.show()

    def start(self, simulator):
        plt.tight_layout()
        plt.show(block=False)

        def deco_step(method):
            def wrap(*args, **kwargs):
                # start = time.time()
                method(*args, **kwargs)
                step = simulator.simulationstep
                string = simulator.request.query
                self.update(step, string.decode("UTF8"))

                # print("Time", time.time() - start)
            return wrap

        setattr(simulator, "run_step", deco_step(simulator.run_step))

        [monitor.start() for monitor in self.monitors]


