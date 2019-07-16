import typing
import numpy as np
from symupy.utils import constants as ct

PAR = {"time_step": ct.DCT_SIMULATION_INFO, "engine_tau": ct.ENGINE_CONSTANT}


def dynamic_3rd_ego(state: np.array, control: np.array, parameters=PAR) -> np.array:
    """Update vehicle state in 3rd order dynamics"""
    K_a = parameters["time_step"] / parameters["engine_tau"]
    A = np.array(
        [[1, parameters["time_step"], 0], [0, 1, parameters["time_step"]], [0, 0, (1 - K_a)]]
    )
    B = np.array([[0], [0], [K_a]])
    return A @ state[:3] + B @ control[:1]


def dynamic_2nd_ego(state: np.array, control: np.array, parameters=PAR) -> np.array:
    """Update vehicle state in 2nd order dynamics"""
    A = np.array([[1, parameters["time_step"]], [0, 1]])
    B = np.array([[0], [parameters["time_Step"]]])
    return A @ state[:2] + B @ control[:1]
