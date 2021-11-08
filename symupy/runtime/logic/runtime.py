"""
    This module describes classes and objects to perform a runtime of a single scenario
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

from itertools import chain
import click

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from .states import (
    Compliance,
    Connect,
    Initialize,
    PreRoutine,
    Query,
    Control,
    Push,
    PostRoutine,
    Terminate,
)

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================

start_seq = ["compliance", "connect", "initialize"]
runtime_seq = ["preroutine", "query", "control", "push", "postroutine"]
end_seq = [
    "terminate",
]


class RuntimeDevice:
    """
    This class defines the runtime device describing a series of cyclic states required to be run

    :return: Runtime Device for controlling states of the simulation runtime
    :rtype: RuntimeDevice
    """

    def __init__(self) -> None:
        click.echo("Runtime: Initialization")
        self.state = Compliance()  # Initial state

    def __logic(self, boolContinue: bool = True) -> dict:
        """
        Logic for state machine, transitions

        * ``Compliance`` -> ``Connect``
        * ``Connect`` -> ``Initialize``
        * ``Initialize`` -> ``PreRoutine``
        * ``PreRoutine`` -> ``Query``
        * ``Query`` -> ``Control``
        * ``Control`` -> ``Push``
        * ``Push`` -> ``PostRoutine``
        * ``PostRoutine`` -> ``PreRoutine`` when ``boolContinue`` = True
        * ``PostRoutine`` -> ``Terminate`` when ``boolContinue`` = False
        * ``Terminate`` -> ``Terminate``

        :param boolContinue: Flag to determine continue looping, defaults to True
        :type boolContinue: bool, optional
        :return: State
        :rtype: State
        """
        dct = {
            ("Compliance", True): self.state.on_event("Connect"),
            ("Connect", True): self.state.on_event("Initialize"),
            ("Initialize", True): self.state.on_event("PreRoutine"),
            ("PreRoutine", True): self.state.on_event("Query"),
            ("Query", True): self.state.on_event("Control"),
            ("Control", True): self.state.on_event("Push"),
            ("Push", True): self.state.on_event("PostRoutine"),
            ("PostRoutine", True): self.state.on_event("PreRoutine"),
            ("PostRoutine", False): self.state.on_event("Terminate"),
            ("Terminate", True): self.state.on_event("Terminate"),
            ("Terminate", False): self.state.on_event("Terminate"),
        }
        return dct.get((self.state.__class__.__name__, boolContinue), self.state)

    def reset_state(self) -> None:
        """
        Reset to initial state in case required
        """
        self.state = Compliance()

    def next_state(self, cycle: bool = True) -> None:
        """
        Updates the state according to the state machine logic, possible states

        * ``Compliance``
        * ``Connect``
        * ``Initialize``
        * ``PreRoutine``
        * ``Query``
        * ``Control``
        * ``Push``
        * ``PostRoutine``
        * ``Terminate``

        :param cycle: Cycle parameter to return to PreRoutine state, defaults to True
        :type cycle: bool, optional
        """
        self.state = self.__logic(cycle)
