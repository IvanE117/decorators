import time
from functools import wraps


def retry(times=3, exceptions=(Exception,), delay=0):
    if times < 1: raise ValueError("times должно быть >= 1")
    exceptions = tuple(exceptions)
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            i = 0
            while i < times:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if i == times - 1:
                        raise
                    time.sleep(delay)
                finally:
                    i += 1
        return wrapper
    return decorator


# Пример
@retry(times=3, exceptions=(ZeroDivisionError,), delay=0.1)
def f(x):
    return 10 // x


print(f(0))
