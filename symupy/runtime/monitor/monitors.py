import re

import numpy as np

from symupy.runtime.api import Simulator
from symupy.runtime.monitor.manager import ScatterMonitorView, LineMonitorView
from symupy.utils.constants import DEFAULT_PATH_SYMUVIA

_PATTERN_TRAJ = re.compile("<TRAJ\s(.*?)\/>")
_PATTERN_ATTR  = re.compile('(\w+)="(.*?)"')
_PATTERN_TIME = re.compile('val="(.*?)">')


def _get_trajs(string):
    trajs = _PATTERN_TRAJ.findall(string)
    trajs = [{key:val for key, val in _PATTERN_ATTR.findall(t)} for t in trajs]
    return trajs


def launch_simuvia(file):
    sim_instance = Simulator.from_path(file, DEFAULT_PATH_SYMUVIA)
    sim_instance.trace_flow = True
    sim_instance.step_launch_mode = "full"

    with sim_instance as s:
        while s.do_next:
          s.run_step()
          yield sim_instance.simulationstep, sim_instance.request.query.decode("UTF8")


class SymuviaMonitorMFD(ScatterMonitorView):
    def __init__(self):
        super(SymuviaMonitorMFD, self).__init__('MFD', 'Accumulation', 'production')
        self.nbveh_pattern = re.compile('<INST nbVeh="(.*?)"\s')
        self.vit_pattern = re.compile('vit="(.*?)"')

    def update(self, step, instants, ind):
        nbveh = int(self.nbveh_pattern.findall(instants)[0])
        speeds = [float(v) for v in self.vit_pattern.findall(instants)]
        if speeds:
            mean_speed = sum(speeds)/len(speeds)
            return nbveh, mean_speed*nbveh
        else:
            return None, None


class SymuviaMonitorAccumulation(LineMonitorView):
    def __init__(self):
        super(SymuviaMonitorAccumulation, self).__init__('Accumulation', 'Instant', 'VEH number')
        self.nbveh_pattern = re.compile('<INST nbVeh="(.*?)"\s')

    def update(self, step, instants, ind):
        nbveh = int(self.nbveh_pattern.findall(instants)[0])
        return step, nbveh


class SymuviaMonitorVEH(LineMonitorView):
    def __init__(self, ids, indicator):
        self._indicators = {"speed": self._update_speed,
                            "acceleration": self._update_acceleration,
                            "distance": self._update_distance}
        assert indicator in self._indicators
        super(SymuviaMonitorVEH, self).__init__(f'VEH{ids} {indicator}', 'Instant', indicator, nb_plots=len(ids))
        self.ids = ids

        self.indicator = indicator

        self._dst = 0
        self._lastpos = None

        self.line_labels = [str(id) for id in ids]


    def _update_speed(self, traj):
        return float(traj["vit"])

    def _update_acceleration(self, traj):
        return float(traj["acc"])

    def _update_distance(self, trajs):
        curr_pos = np.array([float(trajs["abs"]), float(trajs["ord"])])
        if self._lastpos is None:
            self._lastpos = curr_pos
        else:
            curr_dst = np.linalg.norm(curr_pos-self._lastpos)
            self._dst += curr_dst
            self._lastpos = curr_pos
        return self._dst

    def update(self, step, instants, ind):
        trajs = _get_trajs(instants)
        veh_state = None
        #time = float(_PATTERN_TIME.findall(instants)[0])
        for t in trajs:
            if int(t["id"]) == self.ids[ind]:
                veh_state = t
                break

        if veh_state is not None:
            y = self._indicators[self.indicator](veh_state)
            return step, y
        else:
            return None, None


class SymuviaMonitorTTT(LineMonitorView):
    def __init__(self, zone, aggregation_period=1):
        super(SymuviaMonitorTTT, self).__init__('Total Travel Time', 'Instant', 'Time')
        self.zone = set(zone)
        self.aggregation_period = aggregation_period

        self.vehs= {}
        self.ttt = 0

    def update(self, step, instants, ind):
        if step%self.aggregation_period==0:
            time = float(_PATTERN_TIME.findall(instants)[0])
            trajs = _get_trajs(instants)
            curr_t = set()
            for t in trajs:
                if t["tron"] in self.zone and t["id"] in self.vehs:
                    self.ttt += time - self.vehs[t["id"]]
                    self.vehs[t["id"]] = time
                if t["tron"] in self.zone:
                    curr_t.add(t["id"])
                    self.vehs[t["id"]] = time

            [self.vehs.pop(t) for t in list(self.vehs.keys()) if t not in curr_t]

            return step, self.ttt
        else:
            return None, None


class SymuviaMonitorTTD(LineMonitorView):
    def __init__(self, zone, aggregation_period=1):
        super(SymuviaMonitorTTD, self).__init__('Total Travel Distance', 'Instant', 'Distance')
        self.zone = set(zone)
        self.aggregation_period = aggregation_period

        self.vehs= {}
        self.ttd = 0

    def update(self, step, instants, ind):
        if step%self.aggregation_period==0:
            trajs = _get_trajs(instants)
            curr_t = set()
            for t in trajs:
                pos = np.array([float(t["abs"]), float(t["ord"])])
                if t["tron"] in self.zone and t["id"] in self.vehs:
                    self.ttd += np.linalg.norm(pos - self.vehs[t["id"]])
                    self.vehs[t["id"]] = pos
                if t["tron"] in self.zone:
                    curr_t.add(t["id"])
                    self.vehs[t["id"]] = pos

            [self.vehs.pop(t) for t in list(self.vehs.keys()) if t not in curr_t]

            return step, self.ttd
        else:
            return None, None


class SymuviaMonitorFlux(LineMonitorView):
    def __init__(self, zone, aggregation_period=1):
        super(SymuviaMonitorFlux, self).__init__('Flux', 'Instant', 'Number', nb_plots=2, line_labels=["InFlux", "OutFlux"])
        self.zone = set(zone)
        self.aggregation_period = aggregation_period

        self.influx = 0
        self.outflux = 0

        self.invehs = set()

    def update(self, step, instants, ind):
        trajs = _get_trajs(instants)

        if ind == 0:
            for t in trajs:
                if t["id"] not in self.invehs and t["tron"] in self.zone:
                    self.influx += 1
                    self.invehs.add(t["id"])
            val = self.influx
            print("in", val)
            if step % self.aggregation_period == 0:
                self.influx= 0
        else:
            curr_vehs = [t["id"] for t in trajs]
            to_del = set()
            for t in self.invehs:
                if t not in curr_vehs:
                    self.outflux += 1
                    to_del.add(t)
            print(to_del, self.outflux)
            self.invehs = self.invehs.difference(to_del)
            val = self.outflux
            print("out",val)
            if step % self.aggregation_period == 0:
                self.outflux= 0

        if step % self.aggregation_period == 0:
            return step, val
        else:
            return None, None


if __name__ == "__main__":
    from symupy.runtime.monitor.manager import MonitorApp

    manager = MonitorApp()
    manager.add_monitor(SymuviaMonitorMFD(), 0, 0)
    manager.add_monitor(SymuviaMonitorAccumulation(), 0, 1)
    manager.add_monitor(SymuviaMonitorVEH([3,58], "speed"), 1, 0)
    manager.add_monitor(SymuviaMonitorTTT(["L_0"], aggregation_period=1), 1, 1)
    manager.add_monitor(SymuviaMonitorTTD(["L_0"], aggregation_period=1), 0, 2, rowspan=2)
    manager.add_monitor(SymuviaMonitorFlux(["L_0"], aggregation_period=10), 2, 0, colspan=3)
    manager.set_feeder(launch_simuvia("/Users/florian/Work/visunet/data/SingleLink_symuvia_withcapacityrestriction.xml"))
    manager.launch_app()