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

from .states import Compliance, Connect, Initialize, PreRoutine, Query, Control, Push, PostRoutine, Terminate
from symupy.utils import Configurator

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================

start_seq = ["compliance", "connect", "initialize"]
runtime_seq = ["preroutine", "query", "control", "push", "postroutine"]
end_seq = [
    "terminate",
]


class RuntimeDevice(object):
    """ This class defines the runtime device describing a series of cyclic states required to be run 

    :param object: Runtime Device for controlling states of the simulation runtime
    :type object: Class with internal logic
    """

    def __init__(self, configurator: Configurator = Configurator()):
        self.state = Compliance()  # Initial state
        self.configurator = configurator
        self.cycles = configurator.total_steps

    def __enter__(self) -> None:
        """ Implementation of the state machine         
        """
        full_seq = chain(start_seq, self.cycles * runtime_seq, end_seq)

        currentCycle = 0
        for event in full_seq:
            self.on_event(event)
            if isinstance(self.state, PostRoutine):  # Step counted on PreRoutine
                currentCycle = currentCycle + 1
                click.echo(click.style(f"Step: {currentCycle}", fg="cyan", bold=True))
            if isinstance(self.state, Terminate):
                break

        self.on_event(event)  # Run Terminate sequence

        return self

    def __exit__(self, type, value, traceback) -> bool:
        return False

    def on_event(self, event: str):
        """ Action to consider on event:

        * compliance
        * connect
        * initialize
        * preroutine
        * query
        * control
        * push
        * postroutine
        * terminate
        
        :param event: 
        :type event: str 
        :param configurator:
        :type configurator: Configurator
        """
        self.state = self.state.on_event(event, self.configurator)
