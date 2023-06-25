import os
import asyncio
import argparse
import json
import functools
import operator

from . import helpers as _helpers
from . import enums   as _enums
from . import events  as _events
from . import client  as _client
from . import utils   as _utils
from . import widget  as _widget


__all__ = ('main',)


_parser = argparse.ArgumentParser(
    description = 'manage a discord client'
)

_parser.add_argument(
    '--token',
    help = 'the client\'s type-less authentication token (if missing, sought as DISCORD_TOKEN env-var)',
    default = None
)


def _get_client(info):

    if (token := info.token) is None:
        try:
            token = os.environ['DISCORD_TOKEN']
        except KeyError:
            print('token not specified or set in environment')
            exit()

    token = 'Bot ' + token

    client = _client.Client(token = token)

    return client


_manage_parsers = _parser.add_subparsers(
    dest = 'action',
    required = True
)

def _main(args = None):

    info = _parser.parse_args(args)

    space = globals()

    function = space[f'_main_{info.action}']
    
    function(info)
  

_manage_start_parser = _manage_parsers.add_parser(
    'start',
    description = 'start the client'
)

_manage_start_parser.add_argument(
    'path',
    help = 'the entry widget\'s location'
)

_manage_start_parser.add_argument(
    '--intents',
    help = 'the intents to use (comma-delimited)',
    type = lambda data: functools.reduce(operator.xor, map(_enums.Intents.__getitem__, data.split(','))),
    default = 0,
    required = False
)

_manage_start_parser.add_argument(
    '--shard-ids',
    help = 'the shard ids to use (comma-delimited)',
    type = lambda data: tuple(map(int, data.split(','))),
    default = None,
    required = False
)

_manage_start_parser.add_argument(
    '--shard-count',
    help = 'the shard count',
    type = lambda data: int(data),
    default = None,
    required = False
)

_main_start_enter_default_Events = {
    # required for voice
    _events.UpdateVoiceState
}

async def _main_start_enter(client, path, intents, shard_ids, shard_count):

    path, name = os.path.split(path)

    await _widget.load(client, name, path)

    Events = set(_main_start_enter_default_Events)

    for asset in _widget._assets.values():
        Events.update(asset.Events)

    intents |= _utils.get_eventful_intents(Events)

    await client.start(intents, shard_ids, shard_count)

    await client.ready()

    return name

async def _main_start_leave(client, name):

    await client.stop()

    await _widget.drop(client, name)


def _main_start(info):

    loop = asyncio.get_event_loop()

    client = _get_client(info)

    coro = _main_start_enter(client, info.path, info.intents, info.shard_ids, info.shard_count)
    name = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        coro = _main_start_leave(client, name)
        loop.run_until_complete(coro)


_manage_update_parser = _manage_parsers.add_parser(
    'update',
    description = 'update the client\'s commands',
)

_manage_update_parser.add_argument(
    'path',
    help = 'the command file\'s extension-less location'
)

async def _main_update_perform(client: _client.Client, commands):

    application = await client.get_self_application_information()
    
    await client.update_all_global_application_commands(application.id, commands)

    await client.stop()

def _main_update(info):

    client = _get_client(info)

    loop = asyncio.get_event_loop()

    base_path = info.path
    init_path = base_path + '.py'
    data_path = base_path + '.json'

    try:
        module = _helpers.load_module_via_path('commands', init_path, attach = False)
    except ModuleNotFoundError:
        with open(data_path, 'r') as file:
            commands = json.load(file)
    else:
        commands = module.commands
        with open(data_path, 'w') as file:
            json.dump(commands, file, indent = 4)

    coro = _main_update_perform(client, commands)
    loop.run_until_complete(coro)


main = _main

