"""
    A class to take control over vehicles 
"""
from dataclasses import dataclass, field
from collections import deque
from typing import List

from symupy.components import Vehicle, VehicleList
from symupy.utils import constants as ct

import numpy as np


@dataclass
class VehicleControl:
    """ Controls a single vehicle"""

    # Local state
    mode: str = "manual"
    time: int = ct.TIME_STEP
    vehicle: Vehicle = Vehicle()
    __pos: float = field(default=vehicle.totaldistance, repr=False)
    __spd: float = field(default=vehicle.speed, repr=False)
    __acc: float = field(default=vehicle.acceleration, repr=False)

    def compute_control(self):
        """Compute automatic control"""
        raise NotImplementedError

    def set_manual_control(self, value, controlvar="acceleration"):
        self.control = value
        if controlvar == "acceleration":
            self.acc = self.control
        elif controlvar == "speed":
            self.spd = self.control
        elif controlvar == "position":
            self.pos = self.control
        self.update_vehicle_state()

    def update_vehicle_state(self):
        """Update vehicle state"""
        self.vehicle.acceleration = self.acc
        self.vehicle.speed = self.spd
        self.vehicle.distance = self.pos

    @property
    def pos(self):
        return self.__pos

    @pos.setter
    def pos(self, value):
        new_spd = (value - self.pos) / self.time
        self.__acc = (new_spd - self.spd) / self.time
        self.__spd = new_spd
        self.__pos = value

    @property
    def spd(self):
        return self.__spd

    @spd.setter
    def spd(self, value):
        self.__acc = (value - self.spd) / self.time
        self.__spd = value
        self.__pos += self.time * self.spd

    @property
    def acc(self):
        return self.__acc

    @acc.setter
    def acc(self, value):
        self.__acc = value
        self.__spd += self.time * self.acc
        self.__pos += self.time * self.spd + (1 / 2) * self.acc * (self.time ** 2)

    @property
    def vehicle_state(self):
        """ Retrive vehicle vector state"""
        return np.array((self.vehicle.totaldistance, self.vehicle.speed, self.vehicle.acceleration))

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
            ", ".join(f"{k}:{v}" for k, v in ctr.vehicles.__dict__.items()) for ctr in self.controls
        )

    def __repr__(self):
        if not self.controls:
            return "No vehicles registered for control"
        return "\n".join(
            ", ".join(f"{k}:{v}" for k, v in ctr.vehicles.__dict__.items()) for ctr in self.controls
        )

