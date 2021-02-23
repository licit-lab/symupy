"""
Abstract Subject 
=================
This module implements a general metaclass of the subject/publisher of information.
"""
# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import abc
from .observer import AbsObserver

# ============================================================================
#  CLASS AND DEFINITIONS
# ============================================================================


class AbsSubject(metaclass=abc.ABCMeta):
    _channels = {}

    @abc.abstractclassmethod
    def attach(self, observer, channel, callback):
        """ Attach a new observer 
        """
        pass

    @abc.abstractclassmethod
    def detach(self, observer, channel):
        """ Detach an existing observer 
        """
        pass

    @abc.abstractclassmethod
    def dispatch(self, channel):
        """ Notify all observers by calling update method
        """
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._channels.clear()
