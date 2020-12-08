"""
Subscriber
==========
This module dedicates a generic object to generate an observer pattern implementation responsible of subscribing to a publisher
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

from itertools import count

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from symupy.metaclass import AbsSubject, AbsObserver

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


class Subscriber(AbsObserver):
    """ This general dataquery model implements a general publisher pattern to
        broadcast information towards different subscribers. Subscribers are
        intented to be objects such as vehicles, front/rear gap coordinators.

        This creates an subject that can notify to a specific channel where subscribers are registered or 
        
        Example:
            Create a DataQuery for 2 type of channels, ``automated`` and  ``regular`` vehicles::

                >>> channels = ('auto','regular')
                >>> query = DataQuery(channels)        
    """

    def __init__(self, publisher, channel="default"):
        self._counter = count(0)
        self._call = next(self._counter)
        self._publisher = publisher
        self._channel = channel
        publisher.attach(self, channel)

    def update(self):
        self._call = next(self._counter)

    def __exit__(self, exc_type, exc_value, traceback):
        self._publisher.detach(self, self._channel)
