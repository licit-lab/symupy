"""
    This module contains a set of exceptions and handlers for such exceptions.

    Example: 
        To use the ``Exceptions`` import the module as::

            >>> from symupy.utils.exceptions import SymupyLoadLibraryError
            >>> from ctypes import cdll
            >>> try: 
            ...     path = 'path/to/library'
            ...     lib = cdll.LoadLibrary(path)
            ... except OSError: 
            ...     raise  SymupyLoadLibraryError("Library not found",path)

"""
# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import warnings

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


class SymupyError(Exception):
    """ 
        General error exception, it can be raised at whatever moment, the class its intends to create a base class that intends to tag error situations dected by this module. 
    
        :return: General ``SymupyError`` exception handler
        :rtype: SymupyError
    """

    def __init__(self, error_message: str, target_dir: str = "") -> None:
        super().__init__(error_message)
        self._target_dir = target_dir

    @property
    def target_dir(self) -> str:
        """ Retreives the path of the target directory
        
        :return: Path to target directory
        :rtype: str
        """
        return self._target_dir

    @property
    def get_messsage(self) -> str:
        """ Retreives custom message to be send to the user 
        
        :return: Custom message
        :rtype: str
        """
        (mess,) = self.args
        return mess


class SymupyWarning(object):
    """
       General warning exception, it can be raised at whatever moment, the class its intends to create a base class that intends to tag warning situations dected by this module. 
    
        :param Exception: General ``SymupyWarning`` exception handler
        :type Exception: SymupyWarning
    """

    def __init__(self, warning_message: str) -> None:
        warnings.warn(warning_message)


class SymupyFileLoadError(SymupyError):
    """
        File Load Error exception handler, created for handling file situations in particular scenario situations
    
        :return: File Load Error 
        :rtype: SymupyFileLoadError
    """

    def __init__(self, error_message: str, target_dir: str = "") -> None:
        super().__init__(error_message, target_dir)

    def __str__(self) -> str:
        return f"{self.get_messsage}, at: {self._target_dir}"

    def __repr__(self) -> str:
        return f"SymupyFileLoadError({self.get_messsage},{self._target_dir})"


class SymupyLoadLibraryError(SymupyError):
    """
        Load Library Error exception handler, created for handling library situations in particular when it is not 
        possible to link the library and python
    
        :return: Library Load Error 
        :rtype: SymupyLoadLibraryError
    """

    def __init__(self, error_message: str, target_dir: str = "") -> None:
        super().__init__(error_message, target_dir)

    def __str__(self) -> str:
        return f"{self.get_messsage}, at: {self._target_dir}"

    def __repr__(self) -> str:
        return f"SymupyLoadLibraryError({self.get_messsage},{self._target_dir})"


class SymupyVehicleCreationError(SymupyError):
    """
        Vehicle Creation Error exception handler, created for handling situations at runtime when the vehicles cannot be created within the network
    
        :return: Vehicle Creation Error 
        :rtype: SymupyVehicleCreationError
    """

    def __init__(self, error_message: str, target_dir: str = "") -> None:
        super().__init__(error_message, target_dir)

    def __str__(self) -> str:
        return f"{self.get_messsage}, at: {self._target_dir}"

    def __repr__(self) -> str:
        return f"SymupyVehicleCreationError({self.get_messsage},{self._target_dir})"


class SymupyDriveVehicleError(SymupyError):
    """
        Vehicle Drive Error exception handler, created for handling situations at runtime when the vehicles cannot be created within the network
    
        :return: Vehicle Creation Error 
        :rtype: SymupyDriveVehicleError
    """

    def __init__(self, error_message: str, target_dir: str = "") -> None:
        super().__init__(error_message, target_dir)

    def __str__(self) -> str:
        return f"{self.get_messsage}, at: {self._target_dir}"

    def __repr__(self) -> str:
        return f"SymupyDriveVehicleError({self.get_messsage},{self._target_dir})"
