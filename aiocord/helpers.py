import sys
import os
import importlib.util


__all__ = ()


def get_shard_id_via_guild_id(shard_count, guild_id):

    return (int(guild_id) >> 22) % shard_count


def yank_dict(origin, keys):

    target = {}
    for key in keys:
        try:
            value = origin[key]
        except KeyError:
            continue
        target[key] = value

    return target


def load_module_via_path(name, path, attach = True, execute = True):

    if os.path.isdir(path):
        path = os.path.join(path, '__init__.py')

    spec = importlib.util.spec_from_file_location(name, path)

    if spec is None:
        raise ModuleNotFoundError(path)

    module = importlib.util.module_from_spec(spec)

    if attach:
        sys.modules[module.__name__] = module

    if execute:
        spec.loader.exec_module(module)

    return module


def drop_module(source):

    for target in tuple(sys.modules):
        if not source.startswith(target):
            continue
        del sys.modules[target]