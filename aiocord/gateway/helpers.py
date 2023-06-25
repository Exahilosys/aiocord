
__all__ = ()


def clean_query(store):

    for key in tuple(store):
        value = store[key]
        if value is None:
            del store[key]; continue
        if isinstance(value, bool):
            value = int(value)
        if isinstance(value, int):
            value = str(value)
        store[key] = value


def clean_headers(store):

    for key in tuple(store):
        value = store[key]
        if value is None:
            del store[key]; continue
        store[key] = str(value)