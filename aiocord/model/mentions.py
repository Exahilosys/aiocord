import vessel

from . import types as _types
from . import enums as _enums


__all__ = (
    'user', 'channel', 'role', 'command', 'emoji', 'timestamp'
)


def _make(prefix, parts, delimiter = ':'):

    if any(part is vessel.missing for part in parts):
        return vessel.missing
    
    body = delimiter.join(map(str, parts))

    return f'<{prefix}{body}>'


def user(user_id: _types.Snowflake):

    parts = [user_id]

    return _make('@', parts)


def channel(channel_id: _types.Snowflake):

    parts = [channel_id]

    return _make('#', parts)


def role(role_id: _types.Snowflake):

    parts = [role_id]

    return _make('@&', parts)


def command(command_name: _types.String, command_id: _types.Snowflake):

    parts = [command_name, command_id]

    return _make('/', parts)


def emoji(emoji_name: _types.String, emoji_id: _types.Snowflake, animated: _types.Boolean = False):

    parts = ['a' if animated else '', emoji_name, emoji_id]

    return _make('', parts)


def timestamp(value: _types.Timestamp, style: _enums.TimestampStyle = None):

    parts = [value]

    if not style is None:
        parts.append(style)

    return _make('t', parts)
