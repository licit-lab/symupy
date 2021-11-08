import typing
import numpy as np
from symupy.utils import constants as CT

PAR = {"time_step": CT.DCT_SIMULATION_INFO, "engine_tau": CT.ENGINE_CONSTANT}


def dynamic_3rd_ego(state: np.array, control: np.array, parameters=PAR) -> np.array:
    """Update vehicle state in 3rd order dynamics"""
    K_a = parameters["time_step"] / parameters["engine_tau"]
    A = np.array(
        [
            [1, parameters["time_step"], 0],
            [0, 1, parameters["time_step"]],
            [0, 0, (1 - K_a)],
        ]
    )
    B = np.array([[0], [0], [K_a]])
    return A @ state[:3] + B @ control[:1]


def dynamic_2nd_ego(state: np.array, control: np.array, parameters=PAR) -> np.array:
    """Update vehicle state in 2nd order dynamics"""
    A = np.array([[1, parameters["time_step"]], [0, 1]])
    B = np.array([[0], [parameters["time_Step"]]])
    return A @ state[:2] + B @ control[:1]


class VehicleDynamic(object):
    def __init__(self, time_step=CT.TIME_STEP, veh_dyn=dynamic_2nd_ego) -> None:
        self.time_step = time_step
        self.veh_dyn = veh_dyn
        self.prev_state = np.array([])

    def __call__(self, *args, **kwargs):

        vehicle, control, parameters = args
        DCT_DIRECTIVES = {
            "dynamic_3rd_ego": {
                "args": (vehicle.state, control, parameters),
                "kwargs": kwargs,
            },
            "dynamic_2nd_ego": {"args": (vehicle.state, control), "kwargs": kwargs},
        }

        dynamic_name = self.veh_dyn.__name__
        args = DCT_DIRECTIVES.get(dynamic_name).get("args")
        kwargs = DCT_DIRECTIVES.get(dynamic_name).get("kwargs")
        return self.veh_dyn(*args, **kwargs)

    def __repr__(self):
        return f"{self.__class__.__name__}(time_step = {self.time_step}, veh_dyn ={self.veh_dyn.__name__})"

    def __str__(self):
        return f"{self.__class__.__name__}(time_step = {self.time_step}, veh_dyn ={self.veh_dyn.__name__})"
