from functools import wraps

# Decorators


def logger_func(orig_func):
    import logging

    logging.basicConfig(filename="{}.log".format(orig_func.__name__), level=logging.INFO)

    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        logging.info("Ran with args: {}, and kwargs: {}".format(args, kwargs))
        return orig_func(*args, **kwargs)

    return wrapper


def timer_func(orig_func):
    import time

    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = orig_func(*args, **kwargs)
        t2 = time.time() - t1
        print("{} ran in: {} sec".format(orig_func.__name__, t2))
        return result

    return wrapper


def printer_time(orig_func):
    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        print(f"Step: {args[0].simulationstep}")
        return orig_func(*args, **kwargs)

    return wrapper
