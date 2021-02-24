"""
Screen log
==========
This module serves as a printer for main class messages like log, warnings, errors, check messages.
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import click
from functools import partial
from click.termui import style

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


def log_in_terminal(message: str, *args, **kwargs) -> None:
    """This function logs in the terminal a message with a specific color

    Args:
        message (str): Message to log on the console
        foreground(str): Foreground color see click.style for options

    """
    if args:
        message = message + "\n" + "\n".join(args)
    click.echo(style(message, **kwargs))


def log_error(message, *args, **kwargs) -> None:
    """Logs an error message in red"""
    f = partial(log_in_terminal, fg="red", **kwargs)
    f(message, *args)


def log_verify(message, *args, **kwargs) -> None:
    """Logs an verification message in blue"""
    f = partial(log_in_terminal, fg="blue", **kwargs)
    f(message, *args)


def log_warning(message, *args, **kwargs) -> None:
    """Logs a warning message in yellow"""
    f = partial(log_in_terminal, fg="yellow", **kwargs)
    f(message, *args)


def log_success(message, *args, **kwargs) -> None:
    """Logs a success message in green"""
    f = partial(log_in_terminal, fg="green", **kwargs)
    f(message, *args)


if __name__ == "__main__":
    log_error("Error", "message")
    log_verify("Verification", "message")
    log_warning("Warning", "multiple", "lines")
    log_success("Success", "message", "for", "testing")
