""" 
    This module defines the basic states required to execute and launch a simulation. 

    The states are defined as: 

    * **Compliance**: This state is defined to check availability of files and candidates.
    * **Connect**: This state is defined to process 
    * **Initialize**: This state perform initialization tasks. In example, loading the file scenarios into the simulator. Declaring initial conditions for the platoon, etc. 
    * **Preroutine**: Tasks to be done before the querying information from the simulator
    * **Query**: Tasks of parsing data and querying information from the simulator
    * **Control**: Perform decision tasks for the platoon 
    * **Push**: Push updated information to the simulator for platoon vehicles 
    * **Postroutine**: Performs tasks after the information has been pushed. 
"""

from .base import State


# Start of our states
class Compliance(State):
    """
    The state which declares an status to check file compliance .
    """

    def on_event(self, event: str) -> None:
        if event == "Connect":
            return Connect()

        return self


class Connect(State):
    """
    The state which declares the creation of a connection with the simulator
    """

    def on_event(self, event: str):
        if event == "Initialize":
            return Initialize()

        return self


class Initialize(State):
    """
    The state which initializes values for the scenario simulation
    """

    def on_event(self, event: str):
        if event == "PreRoutine":
            return PreRoutine()

        return self


class PreRoutine(State):
    """
    The state which performs task previous to the interaction with the simulator
    """

    def on_event(self, event: str):
        if event == "Query":
            return Query()

        return self


class Query(State):
    """
    The state which retrieves information from the simulator
    """

    def on_event(self, event: str):
        if event == "Control":
            return Control()

        return self


class Control(State):
    """
    The state which computes the control decision
    """

    def on_event(self, event: str):
        if event == "Push":
            return Push()

        return self


class Push(State):
    """
    The state which pushes data back to the simulator
    """

    def on_event(self, event: str):
        if event == "PostRoutine":
            return PostRoutine()

        return self


class PostRoutine(State):
    """
    The state which logs information or compute step indicators
    """

    def on_event(self, event: str):
        if event == "PreRoutine":
            return PreRoutine()
        elif event == "Terminate":
            return Terminate()

        return self


class Terminate(State):
    """
    The state which declares the end of a simulation
    """

    def on_event(self, event: str):
        return self


# End of our states.
