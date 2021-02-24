"""
Abstract Command 
=================
This module implements a general metaclass for a command.
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import abc

# ============================================================================
#  CLASS AND DEFINITIONS
# ============================================================================


class AbsCommand(metaclass=abc.ABCMeta):
    """Abstract command class"""

    @abc.abstractmethod
    def execute(self):
        """Standard launcher"""

    @abc.abstractproperty
    def names(self):
        """Command name"""

    @abc.abstractproperty
    def description(self):
        """Command brief description"""
