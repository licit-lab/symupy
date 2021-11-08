import re

import numpy as np

from symupy.runtime.api import Simulator
from symupy.runtime.monitor.manager import ScatterMonitorView, LineMonitorView
from symupy.utils.constants import DEFAULT_PATH_SYMUFLOW


def launch_simuflow(file) -> tuple:
    sim_instance = Simulator.from_path(file, DEFAULT_PATH_SYMUFLOW)
    sim_instance.trace_flow = True
    sim_instance.step_launch_mode = "full"

    with sim_instance as s:
        while s.do_next:
          s.run_step()
          yield sim_instance.simulationstep, sim_instance.request.datatraj


class SymuFlowMonitorMFD(ScatterMonitorView):
    def __init__(self):
        super(SymuFlowMonitorMFD, self).__init__('MFD', 'Accumulation', 'Production')

    def update(self, step, instants, ind):
        nbveh = instants.nbveh
        if instants.vit:
            mean_speed = np.mean(list(instants.vit.values()))
            return nbveh, mean_speed*nbveh
        else:
            return None, None


class SymuFlowMonitorAccumulation(LineMonitorView):
    def __init__(self):
        super(SymuFlowMonitorAccumulation, self).__init__('Accumulation', 'Instant', 'VEH number')

    def update(self, step, instants, ind):
        return step, instants.nbveh


class SymuFlowMonitorVEH(LineMonitorView):
    def __init__(self, ids, indicator):
        self._indicators = {"speed": self._update_speed,
                            "acceleration": self._update_acceleration,
                            "distance": self._update_distance}
        assert indicator in self._indicators
        super(SymuFlowMonitorVEH, self).__init__(f'VEH {indicator}', 'Instant', indicator, nb_plots=len(ids))
        self.ids = ids

        self.indicator = indicator

        self._dst = [0]*len(ids)
        self._lastpos = [None]*len(ids)
        self.line_labels = [str(id) for id in ids]


    def _update_speed(self, instants, ind):
        return instants.vit[self.ids[ind]]

    def _update_acceleration(self, instants, ind):
        return instants.acc[self.ids[ind]]

    def _update_distance(self, instants, ind):
        curr_pos = np.array([instants.abs[self.ids[ind]], instants.ord[self.ids[ind]]])

        if self._lastpos[ind] is None:
            self._lastpos[ind] = curr_pos
        else:
            curr_dst = np.linalg.norm(curr_pos-self._lastpos[ind])
            self._dst[ind] += curr_dst
            self._lastpos[ind] = curr_pos
        return self._dst[ind]

    def update(self, step, instants, ind):
        veh_ids = instants.id
        veh_state = None
        if self.ids[ind] in veh_ids:
            y = self._indicators[self.indicator](instants, ind)
            return step, y
        else:
            return None, None


class SymuFlowMonitorTTT(LineMonitorView):
    def __init__(self, zone, aggregation_period=1):
        super(SymuFlowMonitorTTT, self).__init__('Total Travel Time', 'Instant', 'Time')
        self.zone = set(zone)
        self.aggregation_period = aggregation_period

        self.vehs= {}
        self.ttt = 0

    def update(self, step, instants, ind):
        if step%self.aggregation_period==0:
            time = instants.inst
            curr_t = set()
            for vehid, tron in instants.tron.items():
                if tron in self.zone and vehid in self.vehs:
                    self.ttt += time - self.vehs[vehid]
                    self.vehs[vehid] = time
                if tron in self.zone:
                    curr_t.add(vehid)
                    self.vehs[vehid] = time

            [self.vehs.pop(t) for t in list(self.vehs.keys()) if t not in curr_t]

            return step, self.ttt
        else:
            return None, None


class SymuFlowMonitorTTD(LineMonitorView):
    def __init__(self, zone, aggregation_period=1):
        super(SymuFlowMonitorTTD, self).__init__('Total Travel Distance', 'Instant', 'Distance')
        self.zone = set(zone)
        self.aggregation_period = aggregation_period

        self.vehs= {}
        self.ttd = 0

    def update(self, step, instants, ind):
        if step%self.aggregation_period==0:
            curr_t = set()
            for vehid, tron, abs, ord in zip(instants.id, instants.tron.values(), instants.abs.values(), instants.ord.values()):
                pos = np.array([abs, ord])
                if tron in self.zone and vehid in self.vehs:
                    self.ttd += np.linalg.norm(pos - self.vehs[vehid])
                    self.vehs[vehid] = pos
                if tron in self.zone:
                    curr_t.add(vehid)
                    self.vehs[vehid] = pos

            [self.vehs.pop(t) for t in list(self.vehs.keys()) if t not in curr_t]

            return step, self.ttd
        else:
            return None, None


class SymuFlowMonitorFlux(LineMonitorView):
    def __init__(self, zone, aggregation_period=1):
        super(SymuFlowMonitorFlux, self).__init__('Flux', 'Instant', 'Number', nb_plots=2, line_labels=["InFlux", "OutFlux"])
        self.zone = set(zone)
        self.aggregation_period = aggregation_period

        self.influx = 0
        self.outflux = 0

        self.invehs = set()

    def update(self, step, instants, ind):
        if ind == 0:
            for vehid, tron in instants.tron.items():
                if vehid not in self.invehs and tron in self.zone:
                    self.influx += 1
                    self.invehs.add(vehid)
            val = self.influx
            if step % self.aggregation_period == 0:
                self.influx= 0
        else:
            curr_vehs = list(instants.tron.keys())
            to_del = set()
            for t in self.invehs:
                if t not in curr_vehs:
                    self.outflux += 1
                    to_del.add(t)
            self.invehs = self.invehs.difference(to_del)
            val = self.outflux
            if step % self.aggregation_period == 0:
                self.outflux= 0

        if step % self.aggregation_period == 0:
            return step, val
        else:
            return None, None


class SymuFlowMonitorFlow(ScatterMonitorView):
    def __init__(self, xrange=None, yrange=None):
        super(SymuFlowMonitorFlow, self).__init__('Flow', 'X', 'Y', stack_value=False, symbol="o", xrange=xrange, yrange=yrange)

    def update(self, step, instants, ind):
        ord = [float(v) for v in instants.ord.values()]
        abs = [float(v) for v in instants.abs.values()]

        if ord:
            return abs, ord
        else:
            return None, None
