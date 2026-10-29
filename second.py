from functools import wraps


def uppercase_output(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        try:
            return result.upper()
        except AttributeError:
            return result
    return wrapper

# Пример
@uppercase_output
def greeting():
    return "hello"


@uppercase_output
def get_number(): 
    return 42


@uppercase_output
def hi(name):
    return f"Hi, {name}"


print(hi("Bob"))
print(greeting())  # "HELLO"
print(get_number())
