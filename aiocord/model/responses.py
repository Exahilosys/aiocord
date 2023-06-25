import typing

from . import types   as _types
from . import enums   as _enums
from . import objects as _objects


__all__ = (
    'get_public_archived_threads', 'get_private_archived_threads',
    'get_self_private_archived_threads', 'get_active_guild_threads',
    'get_self_authorization_information'
)


class get_public_archived_threads(typing.NamedTuple):

    threads       : list[_objects.Channel]
    thread_members: list[_objects.ThreadMember]
    outstanding   : _types.Boolean


class get_private_archived_threads(typing.NamedTuple):

    threads       : list[_objects.Channel]
    thread_members: list[_objects.ThreadMember]
    outstanding   : _types.Boolean


class get_self_private_archived_threads(typing.NamedTuple):

    threads       : list[_objects.Channel]
    thread_members: list[_objects.ThreadMember]
    outstanding   : _types.Boolean


class get_active_guild_threads(typing.NamedTuple):

    threads       : list[_objects.Channel]
    thread_members: list[_objects.ThreadMember]


class get_self_authorization_information(typing.NamedTuple):

    application: _objects.Application
    scopes     : list[_types.String]
    expires    : _types.ISO8601Timestamp
    core_user  : _objects.User