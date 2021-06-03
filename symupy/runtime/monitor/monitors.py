import re
import time

import numpy as np

from symupy.runtime.monitor.manager import Monitor

_PATTERN_TRAJ = re.compile("<TRAJ\s(.*?)\/>")
_PATTERN_ATTR  = re.compile('(\w+)="(.*?)"')
_PATTERN_TIME = re.compile('val="(.*?)">')

def _get_trajs(string):
    trajs = _PATTERN_TRAJ.findall(string)
    trajs = [{key:val for key, val in _PATTERN_ATTR.findall(t)} for t in trajs]
    return trajs

class SymuviaMonitorAccumulation(Monitor):
    def __init__(self):
        super(SymuviaMonitorAccumulation, self).__init__( 'Instant', 'VEH number', 'Accumulation')
        self.nbveh_pattern = re.compile('<INST nbVeh="(.*?)"\s')

    def update(self, step, instants):
        nbveh = int(self.nbveh_pattern.findall(instants)[0])
        return step, nbveh


class SymuviaMonitorMFD(Monitor):
    def __init__(self):
        super(SymuviaMonitorMFD, self).__init__('Accumulation', '<v> x accumulation', 'MFD', style='k+')
        self.nbveh_pattern = re.compile('<INST nbVeh="(.*?)"\s')
        self.vit_pattern = re.compile('vit="(.*?)"')

    def update(self, step, instants):
        nbveh = int(self.nbveh_pattern.findall(instants)[0])
        speeds = [float(v) for v in self.vit_pattern.findall(instants)]
        if speeds:
            mean_speed = sum(speeds)/len(speeds)
            return nbveh, mean_speed*nbveh
        else:
            return None, None


class SymuviaMonitorVEH(Monitor):
    def __init__(self, id, indicator):
        self._indicators = {"speed": self._update_speed,
                            "acceleration": self._update_acceleration,
                            "distance": self._update_distance}
        assert indicator in self._indicators
        super(SymuviaMonitorVEH, self).__init__('Instant', indicator, f'VEH{id} {indicator}')
        self.id = id

        self.indicator = indicator

        self._dst = 0
        self._lastpos = None


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

    def update(self, step, instants):
        trajs = _get_trajs(instants)
        veh_state = None
        #time = float(_PATTERN_TIME.findall(instants)[0])
        for t in trajs:
            if int(t["id"]) == self.id:
                veh_state = t
                break

        if veh_state is not None:
            y = self._indicators[self.indicator](veh_state)
            return step, y
        else:
            return None, None



if __name__ == "__main__":
    from symupy.runtime.api import Simulator
    from symupy.utils.constants import DEFAULT_PATH_SYMUVIA
    from symupy.runtime.monitor import MonitorManager

    sim_instance = Simulator.from_path("/Users/florian.gacon/Work/data/SingleLink_symuvia_withcapacityrestriction.xml", DEFAULT_PATH_SYMUVIA)
    sim_instance.trace_flow = True
    sim_instance.step_launch_mode = "full"

    mm1 = MonitorManager()
    #mm1.add_monitor(SymuviaMonitorVEH(29, "distance"), 222)
    #mm1.add_monitor(SymuviaMonitorVEH(29, "speed"), 221)
    mm1.add_monitor(SymuviaMonitorMFD(), 121)
    mm1.add_monitor(SymuviaMonitorAccumulation(), 122)

    mm1.start(sim_instance)


    with sim_instance as s:
        #while s.do_next:
         #   s.run_step()

        for _ in range(400):
            start = time.time()
            s.run_step()
            print("Total time step:", time.time() - start)

    mm1.end()

