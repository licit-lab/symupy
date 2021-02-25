"""
    A class to take control over vehicles 
"""

from dataclasses import dataclass, field
from collections import deque
from typing import List

from symupy.tsc.vehicles import Vehicle, VehicleList
from symupy.utils import constants as ct

import numpy as np


class VehicleControl:
    """ Controls a single vehicle"""

    def __init__(
        self, vehicle: Vehicle, mode: str = "manual", time: float = ct.TIME_STEP
    ):
        self.mode = mode
        self.time = time
        self.vehicle = vehicle
        self.__pos = vehicle.distance
        self.__spd = vehicle.speed
        self.__acc = vehicle.acceleration

    def __repr__(self):
        return f"{self.__class__.__name__}(vehicle= {self.vehicle.__str__()},mode = {self.mode}, time= {self.time})"

    def __str__(self):
        return f"{self.__class__.__name__}(vehicle= {self.vehicle.__str__()},mode = {self.mode}, time= {self.time})"

    def compute_control(self):
        """Compute automatic control"""
        raise NotImplementedError

    def set_manual_control(self, value, controlvar="acceleration"):
        self.control = {"variable": controlvar, "value": value}

    @property
    def control(self):
        return self.__u

    @control.setter
    def control(self, value):
        """ Setter for manual """
        if self.mode == "manual":
            self.__u = value
            return
        self.__u = self.compute_control()


@dataclass
class VehicleGroupControl:
    """ Control of group of vehicles of the same class"""

    controls: List[VehicleControl] = field(default_factory=list)

    def __str__(self):
        if not self.controls:
            return "No vehicles registered for control"
        return "\n".join(
            ", ".join(f"{k}:{v}" for k, v in ctr.vehicles.__dict__.items())
            for ctr in self.controls
        )

    def __repr__(self):
        if not self.controls:
            return "No vehicles registered for control"
        return "\n".join(
            ", ".join(f"{k}:{v}" for k, v in ctr.vehicles.__dict__.items())
            for ctr in self.controls
        )
