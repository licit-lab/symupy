"""
    This module contains a ``Configurator`` object. The configurator is an object that stores *parameters* that can be relevant to make the evolution of a simulation. The objective is to introduce flexibility when configuring the the simulator platform and the runtime execution possibilities offered by exposed functions from the c library of SymuVia
"""
# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

from ctypes import cdll, create_string_buffer, c_int, byref, c_bool, c_double
import click
import platform

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

import symupy.utils.constants as CT

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


class Configurator:
    """ Configurator class for containing specific simulator parameters
    
        Example:
            To use the ``Simulator`` declare in a string the ``path`` to the simulator ::

                >>> path = "path/to/libSymuyVia.dylib"
                >>> simulator = Configurator(libraryPath = path) 

        Args:
            libraryPath (str): 
                Absolute path towards the simulator library

            bufferSize (int): 
                Size of the buffer for message for data received from simulator

            writeXML (bool): 
                Flag to turn on writting the XML output

            traceFlow (bool):
                Flag to determine tracing or not the flow / trajectories

            totalSteps (int):
                Define the number of iterations of a simulation 

            stepLaunchMode (str):
                Determine to way to launch the ``RunStepEx``. Options ``lite``/``full``

        :return: Configurator object with simulation parameters
        :rtype: Configurator
    """

    def __init__(
        self,
        bufferSize: int = CT.BUFFER_STRING,
        writeXML: bool = CT.WRITE_XML,
        traceFlow: bool = CT.TRACE_FLOW,
        libraryPath: str = CT.DCT_DEFAULT_PATHS[("symuvia", platform.system())],
        totalSteps: int = CT.TOTAL_SIMULATION_STEPS,
        stepLaunchMode: str = CT.LAUNCH_MODE,
    ) -> None:
        """ Configurator class for containing specific simulator parameter

            Args:

            bufferSize (int): 
                Size of the buffer for message for data received from simulator

            writeXML (bool): 
                Flag to turn on writting the XML output

            traceFlow (bool):
                Flag to determine tracing or not the flow / trajectories

            libraryPath (str): 
                Absolute path towards the simulator library

            totalSteps (int):
                Define the number of iterations of a simulation 

            stepLaunchMode (str):
                Determine to way to launch the ``RunStepEx``. Options ``lite``/``full``
        """
        click.echo("Configurator: Initialization")
        self.bufferString = create_string_buffer(bufferSize)
        self.writeXML = c_bool(writeXML)
        self.traceFlow = traceFlow
        self.libraryPath = libraryPath
        self.totalSteps = totalSteps
        self.stepLaunchMode = stepLaunchMode
        super(Configurator, self).__init__()

    def __repr__(self):
        data_dct = ", ".join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({data_dct})"

    def __str__(self):
        data_dct = "Configuration status:\n " + "\n ".join(f"{k}:  {v}" for k, v in self.__dict__.items())
        return f"{data_dct}"
