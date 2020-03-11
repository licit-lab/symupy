import typing

import warnings


class SymupyError(Exception):
    def __init__(self, error_message: str, target_dir: str = "") -> None:
        super().__init__(error_message)
        self._target_dir = target_dir

    @property
    def target_dir(self) -> str:
        return self._target_dir

    @property
    def get_messsage(self) -> str:
        (mess,) = self.args
        return mess


class SymupyWarning(Exception):
    # TODO: Raise a warning all the times
    def __init__(self, warning_message: str) -> None:
        warnings.warn(warning_message)


class SymupyFileLoadError(SymupyError):
    def __init__(self, error_message: str, target_dir: str = "") -> None:
        super().__init__(error_message, target_dir)

    def __str__(self) -> str:
        return f"{self.get_messsage}, at: {self._target_dir}"

    def __repr__(self) -> str:
        return f"SymupyFileLoadError({self.get_messsage},{self._target_dir})"


class SymupyLoadLibraryError(SymupyError):
    def __init__(self, error_message: str, target_dir: str = "") -> None:
        super().__init__(error_message, target_dir)

    def __str__(self) -> str:
        return f"{self.get_messsage}, at: {self._target_dir}"

    def __repr__(self) -> str:
        return f"SymupyLoadLibraryError({self.get_messsage},{self._target_dir})"


class SymupyVehicleCreationError(SymupyError):
    def __init__(self, error_message: str, target_dir: str = "") -> None:
        super().__init__(error_message, target_dir)

    def __str__(self) -> str:
        return f"{self.get_messsage}, at: {self._target_dir}"

    def __repr__(self) -> str:
        return f"SymupyVehicleCreationError({self.get_messsage},{self._target_dir})"


class SymupyDriveVehicleError(SymupyError):
    def __init__(self, error_message: str, target_dir: str = "") -> None:
        super().__init__(error_message, target_dir)

    def __str__(self) -> str:
        return f"{self.get_messsage}, at: {self._target_dir}"

    def __repr__(self) -> str:
        return f"SymupyDriveVehicleError({self.get_messsage},{self._target_dir})"
