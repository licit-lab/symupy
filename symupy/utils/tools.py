"""This module contains a series of decorators in order to add logging functionalities to some of the class methods. The decorators are regularly purposed for logging, printing, neutering funcitons. etc. 

"""

from functools import wraps
from typing import Callable

from .screen import log_in_terminal, log_success

# Decorators


def logger_func(orig_func: Callable):
    """Logs execution of a function/method and arguments into a file called with the function name

    Args:
        orig_func (Callable): A function/method to be logged

    Returns:
        (Callable): Wrapped method after log
    """
    import logging

    logging.basicConfig(
        filename="{}.log".format(orig_func.__name__), level=logging.INFO
    )

    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        logging.info("Ran with args: {}, and kwargs: {}".format(args, kwargs))
        return orig_func(*args, **kwargs)

    return wrapper


def timer_func(orig_func: Callable) -> Callable:
    """Prints in terminal the execution time of a code

    Args:
        orig_func (Callable): A function/method to be temporized

    Returns:
        Callable: Wrapped method after timming execution time
    """
    import time

    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = orig_func(*args, **kwargs)
        t2 = time.time() - t1
        log_success("{} ran in: {} sec".format(orig_func.__name__, t2))
        return result

    return wrapper


def printer_time(orig_func: Callable) -> Callable:
    """Prints in terminal the current time step of a simulation.

    Args:
        orig_func (Callable): Connector class containing the `simulationstep` status via an attribute. Decorated method is `run_step`

    Returns:
        Callable: Wrapped step execution
    """
    # This is useful in the case of chaining decorators.
    # See: https://youtu.be/FsAPt_9Bf3U?t=1343
    # @wraps(orig_func)
    def wrapper(*args, **kwargs):
        log_in_terminal(f"Step: {args[0].simulationstep}")
        return orig_func(*args, **kwargs)

    return wrapper


def conditional(cond: bool, warning: str = "") -> Callable:
    """Disables the execution of the decorated method/function

    Args:
        cond (bool): Flag to execute
        warning (str, optional): Warning to login. Defaults to "".

    Returns:
        Callable: Wrapped method
    """
    # Top decorator for disabling a function execution:
    # See: https://stackoverflow.com/questions/17946024/deactivate-function-with-decorator
    def noop_decorator(func):
        return func  # pass through

    def neutered_function(func):
        def neutered(*args, **kw):
            if warning != "":
                log.warn(warning)
            return

        return neutered

    return noop_decorator if cond else neutered_function
