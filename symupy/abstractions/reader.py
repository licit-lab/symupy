from abc import ABC, abstractmethod

class AbstractNetworkReader(ABC):
    _ext = None

    def __init__(self):
        assert self._ext != None, "Reader must define the extension associate to the file via _ext class attribute"

    @abstractmethod
    def get_network(self):
        pass


class AbstractTrafficDataReader(ABC):
    _ext = None

    def __init__(self):
        assert self._ext != None, "Reader must define the extension associate to the file via _ext class attribute"

    @abstractmethod
    def get_OD(self, period, OD, loop=None):
        pass

    @abstractmethod
    def get_trip(self, vehid):
        pass

    @abstractmethod
    def get_path(self, vehid):
        pass
