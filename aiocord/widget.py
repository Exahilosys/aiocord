import typing
import os
import asyncio
import functools
import types
import weakref
import inspect
import itertools
import aiohttp
import re
import io
import zipfile
import tempfile

from . import helpers as _helpers
from . import model   as _model
from . import client  as _client
from . import events  as _events


__all__ = ('Info', 'callback', 'interact', 'load', 'drop')


_V = typing.TypeVar('_V')
_P = typing.ParamSpec('_P')


class Info(typing.NamedTuple):

    """
    Holds global information.
    """

    client : _client.Client
    """
    The client for which this widget has been loaded.
    """
    widgets: dict[str, types.ModuleType]
    """
    All currently loaded widgets.
    """


def _load_module(path, *, ids = itertools.count(0)):

    intermediary = next(ids)

    name = os.path.basename(path)

    module_name = f'{__name__}.{intermediary}.{name}'

    module = _helpers.load_module_via_path(module_name, path)

    return module


_latent_callback_assets = []


def _callback(Event):
    def decorator(function):
        _latent_callback_assets.append((Event, function))
        return function
    return decorator


def callback(Event: _V) -> typing.Callable[[typing.Callable[_P, _V]], typing.Callable[[Info, typing.Unpack[tuple[_V, ...]]], None]]:

    """
    Create a callback for an core_event.

    :param Event:
        Any event dispatchable by :class:`.client.Client`.
    """

    return _callback(Event)


_latent_interact_assets = []


def _interact(path):
    def decorator(function):
        _latent_interact_assets.append((path, function))
        return function
    return decorator


def interact(*path: typing.Unpack[tuple[str, ...]]) -> typing.Callable[[typing.Callable[_P, _V]], typing.Callable[[Info, _events.CreateIntegration], typing.Awaitable[_model.protocols.InteractionResponse | None]]]:

    """
    Create a callback for an interaction.

    If a :code:`.model.protocols.InteractionResponse` is returned, it is used to respond via :meth:`.client.create_interaction_response`.

    :param *path:
        The ``command-name`` to ``sub[command/group]-name`` leading to the desired command.
    """

    return _interact(path)


_modules_group = weakref.WeakKeyDictionary()


_assets = weakref.WeakKeyDictionary()


def _find_caller_widget_asset():

    stack = inspect.stack()

    for index, frame in enumerate(stack):
        if index < 2:
            continue
        module = inspect.getmodule(frame)
        try:
            asset = _assets[module]
        except KeyError:
            continue
        break
    else:
        asset = None
    
    return module, asset


async def _load_internal_widget(client, name, module):

    try:
        await _drop(client, name, pop = False)
    except KeyError:
        pass

    try:
        modules = _modules_group[client]
    except KeyError:
        modules = _modules_group[client] = weakref.WeakValueDictionary()

    modules[name] = module

    if not (application := client.cache.application):
        application = await client.get_self_application_information()

    commands = await client.get_global_application_commands(application.id)

    info = Info(client, types.MappingProxyType(modules))

    callbacks = []

    Events = set()

    def load_callback(Event, function):
        Events.add(Event)
        async def callback(event, *args, **kwargs):
            if not isinstance(event, Event):
                return
            await function(info, event, *args, **kwargs)
        return callback

    for asset in _latent_callback_assets:
        callback = load_callback(*asset)
        callbacks.append(callback)

    _latent_callback_assets.clear()

    def get_command(path, commands = commands):
        name, *path = path
        for command in commands:
            if not command.name == name:
                continue
            break
        if not path:
            return command
        return get_command(path, commands = command.options)

    def load_interact_callback(path, function):
        command = get_command(path)
        async def callback(info, core_event, *args, **kwargs):
            if not core_event.interaction.type == _model.enums.InteractionType.application_command:
                return
            if not core_event.interaction.data.id == command.id:
                return
            response = await function(info, core_event, *args, **kwargs)
            if not response is None:
                await client.create_interaction_response(core_event.interaction.id, core_event.interaction.token, **response)
        return callback
    
    for asset in _latent_interact_assets:
        callback = load_interact_callback(*asset)
        callback = load_callback(_events.CreateInteraction, callback)
        callbacks.append(callback)

    _latent_interact_assets.clear()

    try:
        load = getattr(module, '__load__')
    except AttributeError:
        pass
    else:
        await load(info)

    client.callbacks.extend(callbacks)

    asset = _assets[module] = types.SimpleNamespace(
        name = name,
        info = info, 
        Events = Events,
        callbacks = callbacks
    )

    return asset


async def _load_internal(client, name, path):

    loop = asyncio.get_event_loop()

    if path is None:
        module, asset = _find_caller_widget_asset()
        if asset is None:
            raise ModuleNotFoundError('implicit path used with unknown calling widget')
        path = os.path.dirname(module.__path__[0])

    load_module = functools.partial(_load_module, path)

    module = await loop.run_in_executor(None, load_module)
    
    asset = await _load_internal_widget(client, name, module)

    return module


async def _load_external_github(session, client, name, author, project, version):

    response = await session.request('GET', f'https://api.github.com/repos/{author}/{project}/tags')
    tags = await response.json()

    if version is None:
        tag = max(tags, key = lambda tag: tag['name'])
    else:
        version_pattern = re.compile(version)
        try:
            tag = next(filter(lambda tag: version_pattern.match(tag['name']), tags))
        except StopIteration:
            raise ModuleNotFoundError(f'unknown tag {version} for {author}/{project}')
    
    response = await session.request('GET', tag['zipball_url'])
    data = await response.read()
    archive = zipfile.ZipFile(io.BytesIO(data))

    loop = asyncio.get_event_loop()

    def load_module():
        with tempfile.TemporaryDirectory(prefix = __name__ + '_') as project_path_base:
            archive.extractall(project_path_base)
            for project_path_name in os.listdir(project_path_base):
                if any(map(project_path_name.startswith, ('.', '_'))):
                    continue
                project_path = os.path.join(project_path_base, project_path_name)
                if not os.path.isdir(project_path):
                    continue
                break
            else:
                raise ModuleNotFoundError(f'could not find project directory')
            module_path = os.path.join(project_path, 'widget')
            module = _load_module(module_path)
        return module
    
    module = await loop.run_in_executor(None, load_module)
    
    asset = await _load_internal_widget(client, name, module)

    return module


_load_external_functions = {
    'github': _load_external_github
} 


async def _load_external(vendor, client, name, path, version):

    function = _load_external_functions[vendor]

    author, project = path.split('/')

    async with aiohttp.ClientSession() as session:
        module = await function(session, client, name, author, project, version)

    return module


async def _load(client, name, path, vendor, *, version = None):

    if vendor is None:
        function = lambda: _load_internal(client, name, path)
    else:
        function = lambda: _load_external(vendor, client, name, path, version)

    module = await function()

    return module


def load(client : _client.Client, 
         name   : str, 
         path   : str                      = None,
         vendor : typing.Literal['github'] = None,
         *,
         version: str                      = None) -> typing.Awaitable[types.ModuleType]:
    
    """
    Load a widget by creating and attaching events to the client.
    
    :param client:
        The client to load the widget for.
    :param name:
        The name of the widget, used for identifying in :attr:`.Info.widgets` and :func:`.drop`\ing.
    :param path:
        The location of the package. If not specified, the calling widget's parent directory is used.
    :param vendor:
        The vendor from which to download the widget, given that :paramref:`.path` is an the form of ``author/project/version``.
    :param version:
        The project version to fetch. The latest is used if not specified. Only valid when :paramref:`.vendor` is used. 

    The widget may define a ``__load__(info)`` function, which will be called before callbacks are attached.
    """

    return _load(client, name, path, vendor, version = version)


def _drop_module(name):

    _helpers.drop_module(name)


async def _drop(client, name, *, pop = True):

    loop = asyncio.get_event_loop()

    modules = _modules_group[client]

    getter = modules.pop if pop else modules.__getitem__

    try:
        module = getter(name)
    except KeyError:
        return

    asset = _assets.pop(module)

    for callback in asset.callbacks:
        client.callbacks.remove(callback)

    try:
        drop = getattr(module, '__drop__')
    except AttributeError:
        pass
    else:
        await drop(asset.info)

    drop_module = functools.partial(_drop_module, module.__name__)

    await loop.run_in_executor(None, drop_module)


def drop(client: _client.Client, 
         name: str) -> typing.Awaitable[None]:

    """
    Unload a widget by detaching all the related callbles from the client.

    :param client:
        The client to unload the widget for.
    :param name:
        The name of the widget, as specified in :func:`.load`.

    The widget may define a ``__drop__`` function which will be called after callbacks are detached.
    """

    return _drop(client, name)
