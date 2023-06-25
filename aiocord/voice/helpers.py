

__all__ = ()


def max_add(value, extra, limit, /, reset = 0):

    value += extra

    if value > limit:
        value = reset

    return value