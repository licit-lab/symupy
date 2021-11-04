"""This module contains a ``Configurator`` object.
    The configurator is an object that stores *parameters* that can be
    relevant to make the evolution of a simulation. The objective is to
    introduce flexibility when configuring the the simulator platform
    and the runtime execution possibilities offered by exposed functions
    from the c library of SymuFlow
"""
# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

from ctypes import create_string_buffer, c_bool, c_char
from dataclasses import dataclass
import click
from symupy.utils.screen import log_verify

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from symupy.utils.constants import (
    BUFFER_STRING,
    WRITE_XML,
    TRACE_FLOW,
    DEFAULT_PATH_SYMUFLOW,
    TOTAL_SIMULATION_STEPS,
    LAUNCH_MODE,
)

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


@dataclass
class Configurator:
    """Configurator class for containing specific simulator parameters
    Example:
        To use the ``Simulator`` declare in a string the ``path`` to the
        simulator ::

            >>> path = "path/to/libSymuyVia.dylib"
            >>> simulator = Configurator(library_path = path)

    Args:
        library_path (str):
            Absolute path towards the simulator library

        bufferSize (int):
            Size of the buffer for message for data received from simulator

        write_xml (bool):
            Flag to turn on writting the XML output

        trace_flow (bool):
            Flag to determine tracing or not the flow / trajectories

        total_steps (int):
            Define the number of iterations of a simulation

        step_launch_mode (str):
            Determine to way to launch the ``RunStepEx``. Options ``lite``/``full``

    :return: Configurator object with simulation parameters
    :rtype: Configurator
    """

    buffer_string: c_char = create_string_buffer(BUFFER_STRING)
    write_xml: c_bool = c_bool(WRITE_XML)
    trace_flow: bool = TRACE_FLOW
    library_path: str = DEFAULT_PATH_SYMUFLOW
    total_steps: int = TOTAL_SIMULATION_STEPS
    step_launch_mode: str = LAUNCH_MODE

    def __init__(self, **kwargs) -> None:
        """Configurator class for containing specific simulator parameter

        Args:
            library_path (str):
                Absolute path towards the simulator library

            bufferSize (int):
                Size of the buffer for message for data received from simulator

            write_xml (bool):
                Flag to turn on writting the XML output

            trace_flow (bool):
                Flag to determine tracing or not the flow / trajectories

            total_steps (int):
                Define the number of iterations of a simulation

            step_launch_mode (str):
                Determine to way to launch the ``RunStepEx``. Options ``lite``/``full``
        """
        click.echo("Configurator: Initialization")
        for key, value in kwargs.items():
            setattr(self, key, value)
        try:
            if kwargs["library_path"] != DEFAULT_PATH_SYMUFLOW:
                log_verify("Using user defined library path: ", kwargs["library_path"],)
        except KeyError:
            log_verify("Using default defined library path")
        finally:
            return

    def __repr__(self):
        data_dct = ", ".join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({data_dct})"

    def __str__(self):
        data_dct = "Configuration status:\n " + "\n ".join(
            f"{k}:  {v}" for k, v in self.__dict__.items()
        )
        return f"{data_dct}"
