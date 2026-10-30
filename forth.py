from functools import wraps
import time
from collections.abc import Iterable
import random


def retry(times=3, delay=0, retry_on=None):
    times = times if isinstance(times, int) and times >= 1 else 1
    if retry_on is None:
        is_bad = lambda res: not res
    elif callable(retry_on):
        is_bad = retry_on
    elif isinstance(retry_on, Iterable):
        is_bad = lambda res: res in retry_on
    else:
        is_bad = lambda res: res == retry_on

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                result = func(*args, **kwargs)
                if is_bad(result) and attempt != times-1:
                    time.sleep(random.random() * 0.1 + delay)
                else:
                    return result
        return wrapper
    return decorator


# Пример
@retry(times=3, delay=0.1, retry_on=None)  # повторять пока результат falsy
def sometimes_none():
    pass


# 1) Повторять, пока результат falsy (по умолчанию retry_on=None)
counter = {"n": 0}
@retry(times=5, delay=0)
def flaky_falsey():
    counter["n"] += 1
    # возвращаем None первые 3 раза, потом "OK"
    if counter["n"] < 4:
        return None
    return "OK"


print(flaky_falsey())  # Ожидается "OK" (4-я попытка), counter["n"] == 4


# 2) Повторять, пока результат равен конкретному значению
ctr = {"n": 0}
@retry(times=4, delay=0, retry_on=False)
def sometimes_false():
    ctr["n"] += 1
    if ctr["n"] < 3:
        return False
    return True


print(sometimes_false())  # True, была повторена дважды


# 3) Повторять, пока результат in {None, 0}
c = {"n": 0}
@retry(times=3, delay=0, retry_on=(None, 0))
def sometimes_none_or_zero():
    c["n"] += 1
    if c["n"] == 1:
        return 0
    if c["n"] == 2:
        return None
    return "done"


print(sometimes_none_or_zero())  # "done" на 3-й попытке


# 4) Использование predicate-функции
def is_bad(result):
    # допустим, повторяем, пока строка короче 5 символов
    return isinstance(result, str) and len(result) < 5


d = {"n": 0}
@retry(times=4, delay=0, retry_on=is_bad)
def produce_string():
    d["n"] += 1
    return "x" * d["n"]  # "x", "xx", "xxx", ...


print(produce_string())  # вернёт строку длины >=5 либо последний результат, если попытки исчерпаны
