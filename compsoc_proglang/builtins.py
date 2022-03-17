def add(params):
    out = 0

    for value in params:
        out += value

    return out


def mul(params):
    out = 1

    for value in params:
        out *= value

    return out


def my_print(params):
    print(*params)

def my_list(params):
    return params

mylang_builtins = {
    "+": add,
    "*": mul,
    "print": my_print,
    "list": my_print
}
