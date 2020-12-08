"""
Publisher 
===========
This module dedicates a generic object to generate a publisher pattern implementation responsible of specific methods.
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

from symupy.metaclass import AbsSubject

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


class Publisher(AbsSubject):
    """ This generic class model implements a general publisher pattern to
        broadcast information towards different subscribers. Subscribers are
        intented to be objects such as vehicles or other objects that should be aware of the publisher.

        In particular this creates a subject that can notify to a specific channel where subscribers are registered.
        
        Example:
            Create a DataQuery for 2 type of channels, ``automated`` and  ``regular`` and perform a subscription ::

                >>> channels = ('auto','regular')
                >>> p = Publisher(channels)        
                >>> s = Subscriber(p,'auto')  # Registers a s into p
    """

    def __init__(self, channels=("default",)):
        # maps event names to subscribers
        # str -> dict
        self._channels = {channel: {} for channel in channels}

    def __repr__(self):
        return f"{self.__class__.__name__}({self.channels})"

    @property
    def channels(self):
        return tuple(self._channels.keys())

    def get_subscribers(self, channel):
        """Retreive subscribers in a particular channel"""
        return self._channels[channel]

    def attach(self, observer, channel: str, callback=None):
        """ Attach a new observer to a specific channel,, one can specify 
            a method of the class to be called.

            Args:
                channel(str): channel name
                observer(observer): observer object
                callback(callable): method to be executed when publisher notifies.
        """
        if callback == None:
            callback = getattr(observer, "update")
        self.get_subscribers(channel)[observer] = callback

    def detach(self, observer, channel: str):
        """ Detach observer from the subject 

            Args:
                channel(str): channel name
                observer(observer): observer object
                callback(callable): method to be executed when publisher notifies.
        """
        del self.get_subscribers(channel)[observer]

    def dispatch(self, channel: str = "default"):
        """ Dispatches a message to a specific channel

            Args:
                channel(str): channel name                
        """
        for _, callback in self.get_subscribers(channel).items():
            callback()

    def foo(self):
        """ Demo function"""
        print("Hello world")
