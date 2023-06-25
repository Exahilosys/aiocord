import importlib.metadata


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


def get_user_agent():

    name = __name__.split('.', 1)[0]

    try:
        metadata = importlib.metadata.metadata(name)
    except importlib.metadata.PackageNotFoundError:
        return None

    url = metadata['Home-Page']
    version = metadata['Version']

    user_agent = f'DiscordBot ({url} {version})'

    return user_agent