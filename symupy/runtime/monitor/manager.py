import time

import numpy as np

from symupy.runtime.api import Simulation, Simulator
from symupy.utils.constants import DEFAULT_PATH_SYMUVIA

import matplotlib.pyplot as plt
import re

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
        print("Starting Monitor", self.__class__.__name__)
        self.line = self.ax.plot([], [], self.style, alpha=self.alpha)[0]

    def _update_graph(self, step, string):
        print("Update Graph", self.__class__.__name__)
        x_val, y_val = self.update(step, string)
        print(x_val, y_val)
        if (x_val, y_val) != (None, None):
            self.x.append(x_val)
            self.y.append(y_val)

            self.line.set_ydata(self.y)
            self.line.set_xdata(self.x)

            if np.min(self.y) <= self.line.axes.get_ylim()[0] or np.max(self.y) >= self.line.axes.get_ylim()[1]:
                self.line.axes.set_ylim([np.min(self.y) - np.std(self.y), np.max(self.y) + np.std(self.y)])

            if np.max(self.x) >= self.line.axes.get_xlim()[1]:
                self.line.axes.set_xlim([np.min(self.x) - 1, np.max(self.x) + 1])

            plt.pause(1e-5)

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
        print("Manager update", step, string)
        [monitor._update_graph(step, string) for monitor in self.monitors]

    def start(self):
        plt.ion()
        [monitor.start() for monitor in self.monitors]

    def __call__(self, simulator):
        def deco_reset(method):
            def wrap(*args, **kwargs):
                self.start()
                return method(*args, **kwargs)
            return wrap

        setattr(simulator, "reset_state", deco_reset(simulator.reset_state))

        def deco_step(method):
            def wrap(*args, **kwargs):
                # start = time.time()
                method(*args, **kwargs)
                step = simulator.simulationstep
                string = simulator.request.query
                self.update(step, string)

                # print("Time", time.time() - start)
            return wrap

        setattr(simulator, "run_step", deco_step(simulator.run_step))

        return simulator


class SymuviaMonitorAccumulation(Monitor):
    def __init__(self):
        super(SymuviaMonitorAccumulation, self).__init__( 'Instant', 'VEH number', 'Accumulation')
        self.nbveh_pattern = re.compile('<INST nbVeh="(.*?)"\s')

    def update(self, step, instants):
        print("SymuviaMonitorAccumulation Update")
        instants = instants.decode("UTF8")
        nbveh = int(self.nbveh_pattern.findall(instants)[0])
        return step, nbveh

class SymuviaMonitorMFD(Monitor):
    def __init__(self):
        super(SymuviaMonitorMFD, self).__init__('Accumulation', '||v|| x accumulation', 'MFD', style='+k')
        self.nbveh_pattern = re.compile('<INST nbVeh="(.*?)"\s')
        self.vit_pattern = re.compile('vit="(.*?)"')

    def update(self, step, instants):
        print("SymuviaMonitorMFD Update")
        instants = instants.decode("UTF8")
        nbveh = int(self.nbveh_pattern.findall(instants)[0])
        speeds = [float(v) for v in self.vit_pattern.findall(instants)]
        if speeds:
            mean_speed = sum(speeds)/len(speeds)
            return nbveh, mean_speed*nbveh
        else:
            return None, None



if __name__ == "__main__":
    sim_instance = Simulator.from_path("/Users/florian/Work/visunet/data/SingleLink_symuvia_withcapacityrestriction.xml", DEFAULT_PATH_SYMUVIA)
    sim_instance.trace_flow = True
    sim_instance.step_launch_mode = "full"

    mm = MonitorManager()
    mm.add_monitor(SymuviaMonitorMFD(), 121)
    mm.add_monitor(SymuviaMonitorAccumulation(), 122)

    sim_instance = mm(sim_instance)

    with sim_instance as s:
        while s.do_next:
            s.run_step()
