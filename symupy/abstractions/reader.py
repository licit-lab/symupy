from abc import ABC, abstractmethod


class AbstractNetworkReader(ABC):
    """ Abstraction of Network Reader"""
    _ext = None

    def __init__(self):
        assert (
            self._ext != None
        ), "Reader must define the extension associate to the file via _ext class attribute"

    @abstractmethod
    def get_network(self):
        pass


class AbstractTrafficDataReader(ABC):
    """Abstraction of Traffic Data Reader.

    In order to be able to read trip and OD in VisuNet,
    you must declare the methods:

    get_path(self, id) -> Path
    get_OD(self, *args, **kwargs) -> list[Path]

    Attributes
    ----------
    _ext : type
        Description of attribute `_ext`.

    """

    _ext = None

    def __init__(self):
        assert (
            self._ext != None
        ), "Reader must define the extension associate to the file via _ext class attribute"
