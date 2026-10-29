from functools import wraps


def call_counter(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1  # type: ignore
        print(func(*args, **kwargs))

    wrapper.calls = 0  # type: ignore
    return wrapper


# Пример
@call_counter
def greet(name):
    return f"Hello, {name}"


@call_counter
def add(a, b):
    return a + b


greet("Alice")
greet("Bob")
print(greet.calls)  # 2

add(1, 2)   # 3
print(add.calls)  # 1
