# TODO: Finish the implementation

from dataclasses import dataclass, field
from collections import deque
from typing import List

from symupy.components import Vehicle, VehicleList
from symupy.utils import constants as ct


def _dfl_lst():
    return deque([0] * ct.BUFFER_CONTROL)

@dataclass
class VehicleControl:
    """ Controls a single vehicle"""

    # Local state
    vehicle: Vehicle = field(default_factory=Vehicle)

    # Internals
    timestep: float = field(default=ct.TIME_STEP, repr=False, metadata={"unit": "s"})
    traveldist: float = field(default=0, repr=False, metadata={"unit": "m"})

    # Environment state

    # Historical data
    posithistory: deque = field(default_factory=_dfl_lst, repr=False, metadata={"unit": "m"})
    speedhistory: deque = field(default_factory=_dfl_lst, repr=False, metadata={"unit": "m/s"})
    accelhistory: deque = field(default_factory=_dfl_lst, repr=False, metadata={"unit": "m/s^2"})

    def set_controlpolicy(self, control: float, control_type: str = "accceleration") -> None:
        self.set_controlpolicy(control, control_type)
        return {
            "acceleration": self.udate_queue("speedhistory", control),
            "speed": self.udate_queue("accelhistory", control),
        }.get(control_type, None)

    def update_vehicle_state(self, vehicledata: Vehicle) -> None:
        self.__dict__ = vehicledata.__dict__

    def update_deque(self, attrval: str, control: float):
        getattr(self, attrval).append(control)
        getattr(self, attrval).popleft()


@dataclass
class VehicleGroupControl:
    """ Control of group of vehicles of the same class"""

    controls: List[VehicleControl] = field(default_factory=list)

    def __str__(self):
        if not self.controls:
            return "No vehicles registered for control"
        return "\n".join(
            ", ".join(f"{k}:{v}" for k, v in ctr.vehicles.__dict__.items()) for ctr in self.controls
        )

    def __repr__(self):
        if not self.controls:
            return "No vehicles registered for control"
        return "\n".join(
            ", ".join(f"{k}:{v}" for k, v in ctr.vehicles.__dict__.items()) for ctr in self.controls
        )

