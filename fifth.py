from functools import wraps


def enforce_types(*types):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i, (type_exp, arg) in enumerate(zip(types, args), start=1):
                if not isinstance(arg, type_exp):
                    raise TypeError(f'argument "{i}" must be {type_exp.__name__}')
            return func(*args, **kwargs)
        return wrapper
    return decorator


@enforce_types(int, str)
def f(a, b, c): 
    pass


f(1, "x", True)  # ok
f("no", "x", True)  # TypeError: argument 1 must be int


@enforce_types(int)
def sum_three(a, b, c): 
    pass


sum_three(1, 2, 3)  # ok (проверяется только первый аргумент)
