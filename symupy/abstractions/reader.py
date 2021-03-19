from abc import ABC, abstractmethod

class AbstractNetworkReader(ABC):
    _ext = ''

    def __init__(self, ext):
        self._ext = ext

    @abstractmethod
    def get_network(self):
        pass
