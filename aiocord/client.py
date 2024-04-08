import typing
import json
import aiohttp
import asyncio
import vessel
import copy
import functools
import io
import collections

from . import helpers as _helpers
from . import http    as _http
from . import gateway as _gateway
from . import model   as _model
from . import voice   as _voice
from . import enums   as _enums
from . import events  as _events


__all__ = ('HTTPMeddle', 'GatewayCache', 'Client')


_V = typing.TypeVar('_V')


class HTTPMeddle(typing.Generic[_V]):

    """
    HTTPMeddle(...)

    Returned for all HTTP-related methods.
     
    Facilitates editing a request's options before it's performed.
    
    Useful for attaching request/request-specific headers.

    ``await``\ing the instance will perform the request.

    .. code-block:: python

        request = client.update_channel(channel_id, topic = 'silly fun')
        request.set_reason('just so things dont get too serious')
        channel = await request
    """

    __slots__ = ('_resolve', '_perform', '_options')

    def __init__(self, perform, resolve, options):
        
        self._resolve = resolve
        self._perform = perform
        self._options = options

    def _set_header(self, name, value):

        try:
            headers = self._options['headers']
        except KeyError:
            headers = self._options['headers'] = {}

        if value is None:
            del headers[name]
        else:
            headers[name] = value

    def _set_reason(self, value):

        self._set_header('X-Audit-Log-Reason', value)

    def set_reason(self, value: str):

        """
        Set the :ddoc:`Audit Log Reason </resources/audit-log#audit-logs>` for executing this request.
        """

        self._set_reason(value)

        return self

    async def _execute(self) -> _V:

        data = await self._perform(**self._options)

        with vessel.theme(vessel.Object, unique = True):
            core = self._resolve(data)

        return core

    def __await__(self):

        return self._execute().__await__()


_Cache_fields = {
    'user': vessel.SetField(
        create = lambda path, data: _model.objects.User(data)
    ),
    'guilds': vessel.SetField(
        create = lambda path, data: vessel.Collection(_model.objects.Guild, data)
    ),
    'application': vessel.SetField(
        create = lambda path, data: _model.objects.Application(data)
    )
}


class GatewayCache(vessel.Object, fields = _Cache_fields):

    """
    GatewayCache(...)
    
    Holds objects during gateway connections.
    """

    user: _model.objects.User = vessel.GetField(
        select = lambda root: root['user']
    )
    guilds: vessel.Collection[_model.objects.Guild] = vessel.GetField(
        select = lambda root: root['guilds']
    )
    application: _model.objects.Application = vessel.GetField(
        select = lambda root: root['application']
    )


class GatewaySentinel(typing.NamedTuple):

    event: asyncio.Event
    check: typing.Callable[[typing.Any, typing.Optional[typing.Any]], bool] | None
    task : asyncio.Task


class Client:

    """
    Core means of interaction with the Discord API components.
    
    :param token:   
        The type-less authentication token.
    :param loads:
        Used for converting json text to objects.
    :param dumps:
        Used for converting json objects to text.
    """

    __slots__ = (
        '_token', '_session', '_http', '_loads', '_dumps',  '_callbacks', 
        '_shards', '_cache', '_guild_members_chunk_indexes', '_sentinels',
        '_voices', '__weakref__'
    )

    def __init__(self, 
                 token = None,
                 loads = json.loads, 
                 dumps = json.dumps):
        
        self._token = token
        
        session = aiohttp.ClientSession(
            json_serialize = dumps
        )

        self._session = session

        http = _http.client.Client(
            session, 
            loads = loads, 
            dumps = dumps
        )

        self._http = http
        
        self._loads = loads
        self._dumps = dumps

        http.authenticate(token)

        self._callbacks = []

        self._shards = {}
        self._cache = GatewayCache({})

        self._guild_members_chunk_indexes = {}

        self._sentinels = collections.defaultdict(list)

        self._voices = {}

    @property
    def session(self) -> aiohttp.ClientSession:

        """
        The session for making requests.
        """

        return self._session

    @property
    def http(self) -> _http.client.Client:

        """
        The HTTP client for executing routes.
        """

        return self._http
    
    @property
    def callbacks(self) -> typing.Callable:

        """
        The functions called upon receiving an event.
        """

        return self._callbacks
    
    @property
    def shards(self) -> dict[int, _gateway.client.Client]:

        """
        The gateway clients againt their ids.
        """

        return self._shards
    
    @property
    def cache(self) -> GatewayCache:

        """
        The dispatch cache.
        """

        return self._cache
    
    @property
    def voices(self) -> dict[_model.types.Snowflake, _voice.client.Client]:

        """
        The voice clients.
        """

        return self._voices
    
    async def _ready_gateway(self):

        coros = []
        for shard in self._shards.values():
            coro = shard.event_complete.wait()
            coros.append(coro)

        await asyncio.gather(*coros)
    
    def ready(self) -> typing.Awaitable[None]:

        """
        Wait until all shards are ready to dispatch events.
        """

        return self._ready_gateway()
    
    def _get_shard_via_guild_id(self, guild_id):

        shard = next(iter(self._shards.values())) # sample

        shard_id = _helpers.get_shard_id_via_guild_id(int(guild_id), shard.info.count)

        shard = self._shards[shard_id] # actual
        
        return shard
    
    def _request(self, route, resolve, path, /, **options):

        perform = functools.partial(route, self._http, *path)
        
        meddle = HTTPMeddle(perform, resolve, options)
        
        return meddle
    
    class ___get_global_application_commands_hint(typing.TypedDict):

        with_localizations: typing.Optional[_model.types.Boolean]

    def get_global_application_commands(self,
                                        application_id: _model.types.Snowflake,
                                        /, 
                                        **fields      : typing.Unpack[___get_global_application_commands_hint]) -> HTTPMeddle[list[_model.objects.ApplicationCommand]]:

        """
        Use :data:`.http.routes.get_global_application_commands`.
        
        :param with_localizations:
            |dsrc| **with_localizations**
        """

        path = [application_id]

        query = fields

        def _resolve(data):
            return list(map(_model.objects.ApplicationCommand, data))

        return self._request(_http.routes.get_global_application_commands, _resolve, path, query = query)

    class ___create_global_application_command_hint(typing.TypedDict):

        name                      : typing.Required[_model.types.String]
        name_localizations        : typing.Optional[dict[_model.enums.Locale, _model.types.String]]
        description               : typing.Optional[_model.types.String]
        description_localizations : typing.Optional[dict[_model.enums.Locale, _model.types.String]]
        options                   : typing.Optional[list[_model.protocols.ApplicationCommandOption]]
        default_member_permissions: typing.Optional[_model.enums.Permissions]
        dm_permission             : typing.Optional[_model.types.Boolean]
        type                      : typing.Optional[_model.enums.ApplicationCommandType]
        nsfw                      : typing.Optional[_model.types.Boolean]

    def create_global_application_command(self,
                                          application_id: _model.types.Snowflake,
                                          /, 
                                          **fields      : typing.Unpack[___create_global_application_command_hint]) -> HTTPMeddle[_model.objects.ApplicationCommand]:

        """
        Use :data:`.http.routes.create_global_application_command`.

        :param name:
            |dsrc| **name**
        :param name_localizations:
            |dsrc| **name_localizations**
        :param description:
            |dsrc| **description**
        :param description_localizations:
            |dsrc| **description_localizations**
        :param options:
            |dsrc| **options**
        :param default_member_permissions:
            |dsrc| **default_member_permissions**
        :param dm_permission:
            |dsrc| **dm_permission**
        :param type:
            |dsrc| **type**
        :param nsfw:
            |dsrc| **nsfw**
        """

        path = [application_id]

        json = fields

        def _resolve(data):
            core = _model.objects.ApplicationCommand(data)
            return core

        return self._request(_http.routes.create_global_application_command, _resolve, path, json = json)

    class ___get_global_application_command_hint(typing.TypedDict):

        pass

    def get_global_application_command(self,
                                       application_id: _model.types.Snowflake,
                                       command_id    : _model.types.Snowflake,
                                       /, 
                                       **fields      : typing.Unpack[___get_global_application_command_hint]) -> HTTPMeddle[_model.objects.ApplicationCommand]:

        """
        Use :data:`.http.routes.get_global_application_command`.
        """

        path = [application_id, command_id]

        def _resolve(data):
            core = _model.objects.ApplicationCommand(data)
            return core

        return self._request(_http.routes.get_global_application_command, _resolve, path)

    class ___update_global_application_command_hint(typing.TypedDict):

        name                      : typing.Optional[_model.types.String]
        name_localizations        : typing.Optional[dict[_model.enums.Locale, _model.types.String]]
        description               : typing.Optional[_model.types.String]
        description_localizations : typing.Optional[dict[_model.enums.Locale, _model.types.String]]
        options                   : typing.Optional[list[_model.protocols.ApplicationCommandOption]]
        default_member_permissions: typing.Optional[_model.types.String]
        dm_permission             : typing.Optional[_model.types.Boolean]
        default_permission        : typing.Optional[_model.types.Boolean]
        nsfw                      : typing.Optional[_model.types.Boolean]

    def update_global_application_command(self,
                                          application_id: _model.types.Snowflake,
                                          command_id    : _model.types.Snowflake,
                                          /, 
                                          **fields      : typing.Unpack[___update_global_application_command_hint]) -> HTTPMeddle[_model.objects.ApplicationCommand]:

        """
        Use :data:`.http.routes.update_global_application_command`.
        
        :param name:
            |dsrc| **name**
        :param name_localizations:
            |dsrc| **name_localizations**
        :param description:
            |dsrc| **description**
        :param description_localizations:
            |dsrc| **description_localizations**
        :param options:
            |dsrc| **options**
        :param default_member_permissions:
            |dsrc| **default_member_permissions**
        :param dm_permission:
            |dsrc| **dm_permission**
        :param default_permission:
            |dsrc| **default_permission**
        :param nsfw:
            |dsrc| **nsfw**
        """

        path = [application_id, command_id]

        json = fields

        def _resolve(data):
            core = _model.objects.ApplicationCommand(data)
            return core

        return self._request(_http.routes.update_global_application_command, _resolve, path, json = json)

    class ___delete_global_application_command_hint(typing.TypedDict):

        pass

    def delete_global_application_command(self,
                                          application_id: _model.types.Snowflake,
                                          command_id    : _model.types.Snowflake,
                                          /, 
                                          **fields      : typing.Unpack[___delete_global_application_command_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.delete_global_application_command`.
        """

        path = [application_id, command_id]

        def _resolve(data):
            return None

        return self._request(_http.routes.delete_global_application_command, _resolve, path)

    def update_all_global_application_commands(self,
                                               application_id: _model.types.Snowflake,
                                               /, 
                                               commands      : list[_model.protocols.ApplicationCommand]) -> HTTPMeddle[list[_model.objects.ApplicationCommand]]:

        """
        Use :data:`.http.routes.update_all_global_application_commands`.
        """

        path = [application_id]

        json = commands

        def _resolve(data):
            return list(map(_model.objects.ApplicationCommand, data))

        return self._request(_http.routes.update_all_global_application_commands, _resolve, path, json = json)

    class ___get_guild_application_commands_hint(typing.TypedDict):

        localized: typing.Optional[_model.types.Boolean]

    def get_guild_application_commands(self,
                                       application_id: _model.types.Snowflake,
                                       guild_id      : _model.types.Snowflake,
                                       /, 
                                       **fields      : typing.Unpack[___get_guild_application_commands_hint]) -> HTTPMeddle[list[_model.objects.ApplicationCommand]]:

        """
        :param localized:
            |dsrc| **with_localizations**

        Use :data:`.http.routes.get_guild_application_commands`.
        """

        path = [application_id, guild_id]

        query = fields

        def _resolve(data):
            return list(map(_model.objects.ApplicationCommand, data))

        return self._request(_http.routes.get_guild_application_commands, _resolve, path, query = query)

    class ___create_guild_application_command_hint(typing.TypedDict):

        name                      : typing.Required[_model.types.String]
        name_localizations        : typing.Optional[dict[_model.enums.Locale, _model.types.String]]
        description               : typing.Optional[_model.types.String]
        description_localizations : typing.Optional[dict[_model.enums.Locale, _model.types.String]]
        options                   : typing.Optional[list[_model.protocols.ApplicationCommandOption]]
        default_member_permissions: typing.Optional[_model.types.String]
        default_permission        : typing.Optional[_model.types.Boolean]
        type                      : typing.Optional[_model.enums.ApplicationCommandType]
        nsfw                      : typing.Optional[_model.types.Boolean]

    def create_guild_application_command(self,
                                         application_id: _model.types.Snowflake,
                                         guild_id      : _model.types.Snowflake,
                                         /, 
                                         **fields      : typing.Unpack[___create_guild_application_command_hint]) -> HTTPMeddle[_model.objects.ApplicationCommand]:

        """
        Use :data:`.http.routes.create_guild_application_command`.

        :param name:
            |dsrc| **name**
        :param name_localizations:
            |dsrc| **name_localizations**
        :param description:
            |dsrc| **description**
        :param description_localizations:
            |dsrc| **description_localizations**
        :param options:
            |dsrc| **options**
        :param default_member_permissions:
            |dsrc| **default_member_permissions**
        :param default_permission:
            |dsrc| **default_permission**
        :param type:
            |dsrc| **type**
        :param nsfw:
            |dsrc| **nsfw**
        """

        path = [application_id, guild_id]

        json = fields

        def _resolve(data):
            core = _model.objects.ApplicationCommand(data)
            return core

        return self._request(_http.routes.create_guild_application_command, _resolve, path, json = json)

    class ___get_guild_application_command_hint(typing.TypedDict):

        pass

    def get_guild_application_command(self,
                                      application_id: _model.types.Snowflake,
                                      guild_id      : _model.types.Snowflake,
                                      command_id    : _model.types.Snowflake,
                                      /, 
                                      **fields      : typing.Unpack[___get_guild_application_command_hint]) -> HTTPMeddle[_model.objects.ApplicationCommand]:

        """
        Use :data:`.http.routes.get_guild_application_command`.
        """

        path = [application_id, guild_id, command_id]

        def _resolve(data):
            core = _model.objects.ApplicationCommand(data)
            return core

        return self._request(_http.routes.get_guild_application_command, _resolve, path)

    class ___update_guild_application_command_hint(typing.TypedDict):

        name                      : typing.Optional[_model.types.String]
        name_localizations        : typing.Optional[dict[_model.enums.Locale, _model.types.String]]
        description               : typing.Optional[_model.types.String]
        description_localizations : typing.Optional[dict[_model.enums.Locale, _model.types.String]]
        options                   : typing.Optional[list[_model.protocols.ApplicationCommandOption]]
        default_member_permissions: typing.Optional[_model.types.String]
        default_permission        : typing.Optional[_model.types.Boolean]
        nsfw                      : typing.Optional[_model.types.Boolean]

    def update_guild_application_command(self,
                                         application_id: _model.types.Snowflake,
                                         guild_id      : _model.types.Snowflake,
                                         command_id    : _model.types.Snowflake,
                                         /, 
                                         **fields      : typing.Unpack[___update_guild_application_command_hint]) -> HTTPMeddle[_model.objects.ApplicationCommand]:

        """
        Use :data:`.http.routes.update_guild_application_command`.

        :param name:
            |dsrc| **name**
        :param name_localizations:
            |dsrc| **name_localizations**
        :param description:
            |dsrc| **description**
        :param description_localizations:
            |dsrc| **description_localizations**
        :param options:
            |dsrc| **options**
        :param default_member_permissions:
            |dsrc| **default_member_permissions**
        :param default_permission:
            |dsrc| **default_permission**
        :param nsfw:
            |dsrc| **nsfw**
        """

        path = [application_id, guild_id, command_id]

        json = fields

        def _resolve(data):
            core = _model.objects.ApplicationCommand(data)
            return core

        return self._request(_http.routes.update_guild_application_command, _resolve, path, json = json)

    class ___delete_guild_application_command_hint(typing.TypedDict):

        pass

    def delete_guild_application_command(self,
                                         application_id: _model.types.Snowflake,
                                         guild_id      : _model.types.Snowflake,
                                         command_id    : _model.types.Snowflake,
                                         /, 
                                         **fields      : typing.Unpack[___delete_guild_application_command_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.delete_guild_application_command`.
        """

        path = [application_id, guild_id, command_id]

        def _resolve(data):
            return None

        return self._request(_http.routes.delete_guild_application_command, _resolve, path)

    class ___update_all_guild_application_commands_hint(typing.TypedDict):

        name                      : typing.Required[_model.types.String]
        description               : typing.Required[_model.types.String]
        id                        : typing.Optional[_model.types.Snowflake]
        name_localizations        : typing.Optional[dict[_model.enums.Locale, _model.types.String]]
        description_localizations : typing.Optional[dict[_model.enums.Locale, _model.types.String]]
        options                   : typing.Optional[list[_model.protocols.ApplicationCommandOption]]
        default_member_permissions: typing.Optional[_model.types.String]
        dm_permission             : typing.Optional[_model.types.Boolean]
        default_permission        : typing.Optional[_model.types.Boolean]
        type                      : typing.Optional[_model.enums.ApplicationCommandType]
        nsfw                      : typing.Optional[_model.types.Boolean]

    def update_all_guild_application_commands(self,
                                              application_id: _model.types.Snowflake,
                                              guild_id      : _model.types.Snowflake,
                                              /, 
                                              **fields      : typing.Unpack[___update_all_guild_application_commands_hint]) -> HTTPMeddle[list[_model.objects.ApplicationCommand]]:

        """
        Use :data:`.http.routes.update_all_guild_application_commands`.

        :param id:
            |dsrc| **id**
        :param name:
            |dsrc| **name**
        :param name_localizations:
            |dsrc| **name_localizations**
        :param description:
            |dsrc| **description**
        :param description_localizations:
            |dsrc| **description_localizations**
        :param options:
            |dsrc| **options**
        :param default_member_permissions:
            |dsrc| **default_member_permissions**
        :param dm_permission:
            |dsrc| **dm_permission**
        :param default_permission:
            |dsrc| **default_permission**
        :param type:
            |dsrc| **type**
        :param nsfw:
            |dsrc| **nsfw**
        """

        path = [application_id, guild_id]

        json = fields

        def _resolve(data):
            return list(map(_model.objects.ApplicationCommand, data))

        return self._request(_http.routes.update_all_guild_application_commands, _resolve, path, json = json)

    class ___get_guild_application_command_permissions_hint(typing.TypedDict):

        pass

    def get_guild_application_command_permissions(self,
                                                  application_id: _model.types.Snowflake,
                                                  guild_id      : _model.types.Snowflake,
                                                  /, 
                                                  **fields      : typing.Unpack[___get_guild_application_command_permissions_hint]) -> HTTPMeddle[list[_model.objects.GuildApplicationCommandPermissions]]:

        """
        Use :data:`.http.routes.get_guild_application_command_permissions`.
        """

        path = [application_id, guild_id]

        def _resolve(data):
            return list(map(_model.objects.GuildApplicationCommandPermissions, data))

        return self._request(_http.routes.get_guild_application_command_permissions, _resolve, path)

    class ___get_application_command_permissions_hint(typing.TypedDict):

        pass

    def get_application_command_permissions(self,
                                            application_id: _model.types.Snowflake,
                                            guild_id      : _model.types.Snowflake,
                                            command_id    : _model.types.Snowflake,
                                            /, 
                                            **fields      : typing.Unpack[___get_application_command_permissions_hint]) -> HTTPMeddle[_model.objects.GuildApplicationCommandPermissions]:

        """
        Use :data:`.http.routes.get_application_command_permissions`.
        """

        path = [application_id, guild_id, command_id]

        def _resolve(data):
            core = _model.objects.GuildApplicationCommandPermissions(data)
            return core

        return self._request(_http.routes.get_application_command_permissions, _resolve, path)

    class ___update_application_command_permissions_hint(typing.TypedDict):

        permissions: typing.Required[list[_model.protocols.ApplicationCommandPermission]]

    def update_application_command_permissions(self,
                                               application_id: _model.types.Snowflake,
                                               guild_id      : _model.types.Snowflake,
                                               command_id    : _model.types.Snowflake,
                                               /, 
                                               **fields      : typing.Unpack[___update_application_command_permissions_hint]) -> HTTPMeddle[_model.objects.GuildApplicationCommandPermissions]:

        """
        Use :data:`.http.routes.update_application_command_permissions`.

        :param permissions:
            |dsrc| **permissions**
        """

        path = [application_id, guild_id, command_id]

        json = fields

        def _resolve(data):
            core = _model.objects.GuildApplicationCommandPermissions(data)
            return core

        return self._request(_http.routes.update_application_command_permissions, _resolve, path, json = json)

    class ___create_interaction_response_hint(typing.TypedDict):

        pass

    def create_interaction_response(self,
                                    interaction_id   : _model.types.Snowflake,
                                    interaction_token: _model.types.String,
                                    /, 
                                    **fields         : typing.Unpack[___create_interaction_response_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.create_interaction_response`.
        """

        path = [interaction_id, interaction_token]

        json = fields

        def _resolve(data):
            return None

        return self._request(_http.routes.create_interaction_response, _resolve, path, json = json)

    class ___get_interaction_response_hint(typing.TypedDict):

        thread_id: typing.Optional[_model.types.Snowflake]

    def get_interaction_response(self,
                                 application_id   : _model.types.Snowflake,
                                 interaction_token: _model.types.String,
                                 /, 
                                 **fields         : typing.Unpack[___get_interaction_response_hint]) -> HTTPMeddle[_model.objects.Message]:

        """
        Use :data:`.http.routes.get_interaction_response`.

        :param thread_id:
            |dsrc| **thread_id**
        """

        path = [application_id, interaction_token]

        query = fields

        def _resolve(data):
            core = _model.objects.Message(data)
            return core

        return self._request(_http.routes.get_interaction_response, _resolve, path, query = query)

    class ___update_interaction_response_hint(typing.TypedDict):

        thread_id       : typing.Optional[_model.types.Snowflake | None]
        content         : typing.Optional[_model.types.String | None]
        allowed_mentions: typing.Optional[_model.protocols.AllowedMentions | None]
        components      : typing.Optional[list[_model.protocols.MessageActionRowComponent | _model.protocols.MessageButtonComponent | _model.protocols.MessageTextInputComponent | _model.protocols.MessageSelectMenuComponent] | None]
        files           : typing.Optional[list[io.BytesIO] | None]
        attachments     : typing.Optional[list[_model.protocols.Attachment] | None]

    def update_interaction_response(self,
                                    application_id   : _model.types.Snowflake,
                                    interaction_token: _model.types.String,
                                    /, 
                                    **fields         : typing.Unpack[___update_interaction_response_hint]) -> HTTPMeddle[_model.objects.Message]:

        """
        Use :data:`.http.routes.update_interaction_response`.

        :param thread_id:
            |dsrc| **thread_id**
        :param content:
            |dsrc| **content**
        :param components:
            |dsrc| **components**
        :param files:
            |dsrc| **files[n]**
        :param embeds:
            |dsrc| **embeds**
        :param allowed_mentions:
            |dsrc| **allowed_mentions**
        :param attachments:
            |dsrc| **attachments**
        """

        path = [application_id, interaction_token]

        files = fields.pop('files', None)

        query = _helpers.yank_dict(fields, ('thread_id',))

        json = fields

        def _resolve(data):
            core = _model.objects.Message(data)
            return core

        return self._request(_http.routes.update_interaction_response, _resolve, path, query = query, json = json, files = files)

    class ___delete_interaction_response_hint(typing.TypedDict):

        pass

    def delete_interaction_response(self,
                                    application_id   : _model.types.Snowflake,
                                    interaction_token: _model.types.String,
                                    /, 
                                    **fields         : typing.Unpack[___delete_interaction_response_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.delete_interaction_response`.
        """

        path = [application_id, interaction_token]

        def _resolve(data):
            return None

        return self._request(_http.routes.delete_interaction_response, _resolve, path)

    class ___create_followup_message_hint(typing.TypedDict):

        thread_id       : typing.Optional[_model.types.Snowflake]
        content         : typing.Optional[_model.types.String]
        username        : typing.Optional[_model.types.String]
        avatar_url      : typing.Optional[_model.types.String]
        tts             : typing.Optional[_model.types.Boolean]
        embeds          : typing.Optional[list[_model.protocols.Embed]]
        allowed_mentions: typing.Optional[_model.protocols.AllowedMentions]
        components      : typing.Optional[list[_model.protocols.MessageActionRowComponent | _model.protocols.MessageButtonComponent | _model.protocols.MessageTextInputComponent | _model.protocols.MessageSelectMenuComponent]]
        files           : typing.Optional[list[io.BytesIO]]
        attachments     : typing.Optional[list[_model.protocols.Attachment]]
        thread_name     : typing.Optional[_model.types.String]

    def create_followup_message(self,
                                application_id   : _model.types.Snowflake,
                                interaction_token: _model.types.String,
                                /, 
                                **fields         : typing.Unpack[___create_followup_message_hint]) -> HTTPMeddle[_model.objects.Message]:

        """
        Use :data:`.http.routes.create_followup_message`.

        :param thread_id:
            |dsrc| **thread_id**
        :param content:
            |dsrc| **content**
        :param username:
            |dsrc| **username**
        :param avatar_url:
            |dsrc| **avatar_url**
        :param tts:
            |dsrc| **tts**
        :param components:
            |dsrc| **components**
        :param files:
            |dsrc| **files[n]**
        :param flags:
            |dsrc| **flags**
        :param thread_name:
            |dsrc| **thread_name**
        :param embeds:
            |dsrc| **embeds**
        :param allowed_mentions:
            |dsrc| **allowed_mentions**
        :param attachments:
            |dsrc| **attachments**
        """

        path = [application_id, interaction_token]

        files = fields.pop('files', None)

        query = _helpers.yank_dict(fields, ('wait', 'thread_id'))

        json = fields

        def _resolve(data):
            core = _model.objects.Message(data)
            return core

        return self._request(_http.routes.create_followup_message, _resolve, path, query = query, json = json, files = files)

    class ___get_followup_message_hint(typing.TypedDict):

        pass

    def get_followup_message(self,
                             application_id   : _model.types.Snowflake,
                             interaction_token: _model.types.String,
                             message_id       : _model.types.Snowflake,
                             /, 
                             **fields         : typing.Unpack[___get_followup_message_hint]) -> HTTPMeddle[_model.objects.Message]:

        """
        Use :data:`.http.routes.get_followup_message`.
        """

        path = [application_id, interaction_token, message_id]

        def _resolve(data):
            core = _model.objects.Message(data)
            return core

        return self._request(_http.routes.get_followup_message, _resolve, path)

    class ___update_followup_message_hint(typing.TypedDict):

        thread_id       : typing.Optional[_model.types.Snowflake | None]
        content         : typing.Optional[_model.types.String | None]
        allowed_mentions: typing.Optional[_model.protocols.AllowedMentions | None]
        components      : typing.Optional[list[_model.protocols.MessageActionRowComponent | _model.protocols.MessageButtonComponent | _model.protocols.MessageTextInputComponent | _model.protocols.MessageSelectMenuComponent] | None]
        files           : typing.Optional[list[io.BytesIO] | None]
        attachments     : typing.Optional[list[_model.protocols.Attachment] | None]

    def update_followup_message(self,
                                application_id   : _model.types.Snowflake,
                                interaction_token: _model.types.String,
                                message_id       : _model.types.Snowflake,
                                /, 
                                **fields         : typing.Unpack[___update_followup_message_hint]) -> HTTPMeddle[_model.objects.Message]:

        """
        Use :data:`.http.routes.update_followup_message`.

        :param thread_id:
            |dsrc| **thread_id**
        :param content:
            |dsrc| **content**
        :param components:
            |dsrc| **components**
        :param files:
            |dsrc| **files[n]**
        :param embeds:
            |dsrc| **embeds**
        :param allowed_mentions:
            |dsrc| **allowed_mentions**
        :param attachments:
            |dsrc| **attachments**
        """

        path = [application_id, interaction_token, message_id]

        files = fields.pop('files', None)

        query = _helpers.yank_dict(fields, ('thread_id',))

        json = fields

        def _resolve(data):
            core = _model.objects.Message(data)
            return core

        return self._request(_http.routes.update_followup_message, _resolve, path, query = query, json = json, files = files)

    class ___delete_followup_message_hint(typing.TypedDict):

        pass

    def delete_followup_message(self,
                                application_id   : _model.types.Snowflake,
                                interaction_token: _model.types.String,
                                message_id       : _model.types.Snowflake,
                                /, 
                                **fields         : typing.Unpack[___delete_followup_message_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.delete_followup_message`.
        """

        path = [application_id, interaction_token, message_id]

        def _resolve(data):
            return None

        return self._request(_http.routes.delete_followup_message, _resolve, path)

    class ___get_application_role_connection_metadata_hint(typing.TypedDict):

        pass

    def get_application_role_connection_metadata(self,
                                                 application_id: _model.types.Snowflake,
                                                 /, 
                                                 **fields      : typing.Unpack[___get_application_role_connection_metadata_hint]) -> HTTPMeddle[list[_model.objects.ApplicationRoleConnectionMetadata]]:

        """
        Use :data:`.http.routes.get_application_role_connection_metadata`.
        """

        path = [application_id]

        def _resolve(data):
            return list(map(_model.objects.ApplicationRoleConnectionMetadata, data))

        return self._request(_http.routes.get_application_role_connection_metadata, _resolve, path)

    class ___update_application_role_connection_metadata_hint(typing.TypedDict):

        pass

    def update_application_role_connection_metadata(self,
                                                    application_id: _model.types.Snowflake,
                                                    /, 
                                                    **fields      : typing.Unpack[___update_application_role_connection_metadata_hint]) -> HTTPMeddle[list[_model.objects.ApplicationRoleConnectionMetadata]]:

        """
        Use :data:`.http.routes.update_application_role_connection_metadata`.
        """

        path = [application_id]

        def _resolve(data):
            return list(map(_model.objects.ApplicationRoleConnectionMetadata, data))

        return self._request(_http.routes.update_application_role_connection_metadata, _resolve, path)

    class ___get_guild_audit_log_hint(typing.TypedDict):

        user_id    : typing.Optional[_model.types.Snowflake]
        action_type: typing.Optional[_model.enums.AuditLogEvent]
        before     : typing.Optional[_model.types.Snowflake]
        after      : typing.Optional[_model.types.Snowflake]
        limit      : typing.Optional[_model.types.Integer]

    def get_guild_audit_log(self,
                            guild_id: _model.types.Snowflake,
                            /, 
                            **fields: typing.Unpack[___get_guild_audit_log_hint]) -> HTTPMeddle[_model.objects.AuditLog]:

        """
        Use :data:`.http.routes.get_guild_audit_log`.

        :param user_id:
            |dsrc| **user_id**
        :param action_type:
            |dsrc| **action_type**
        :param before:
            |dsrc| **before**
        :param after:
            |dsrc| **after**
        :param limit:
            |dsrc| **limit**
        """

        path = [guild_id]

        query = fields

        def _resolve(data):
            core = _model.objects.AuditLog(data)
            return core

        return self._request(_http.routes.get_guild_audit_log, _resolve, path, query = query)

    class ___get_guild_auto_moderation_rules_hint(typing.TypedDict):

        pass

    def get_guild_auto_moderation_rules(self,
                                        guild_id: _model.types.Snowflake,
                                        /, 
                                        **fields: typing.Unpack[___get_guild_auto_moderation_rules_hint]) -> HTTPMeddle[list[_model.objects.AutoModerationRule]]:

        """
        Use :data:`.http.routes.get_guild_auto_moderation_rules`.
        """

        path = [guild_id]

        def _resolve(data):
            return list(map(_model.objects.AutoModerationRule, data))

        return self._request(_http.routes.get_guild_auto_moderation_rules, _resolve, path)

    class ___get_auto_moderation_rule_hint(typing.TypedDict):

        pass

    def get_auto_moderation_rule(self,
                                 guild_id               : _model.types.Snowflake,
                                 auto_moderation_rule_id: _model.types.Snowflake,
                                 /, 
                                 **fields               : typing.Unpack[___get_auto_moderation_rule_hint]) -> HTTPMeddle[_model.objects.AutoModerationRule]:

        """
        Use :data:`.http.routes.get_auto_moderation_rule`.
        """

        path = [guild_id, auto_moderation_rule_id]

        def _resolve(data):
            core = _model.objects.AutoModerationRule(data)
            return core

        return self._request(_http.routes.get_auto_moderation_rule, _resolve, path)

    class ___create_auto_moderation_rule_hint(typing.TypedDict):

        name            : typing.Required[_model.types.String]
        event_type      : typing.Required[_model.types.Integer]
        trigger_type    : typing.Required[_model.types.Integer]
        actions         : typing.Required[list[_model.protocols.AutoModerationAction]]
        enabled         : typing.Optional[_model.types.Boolean]
        exempt_roles    : typing.Optional[list[_model.types.Snowflake]]
        exempt_channels : typing.Optional[list[_model.types.Snowflake]]
        trigger_metadata: typing.Optional[_model.protocols.AutoModerationTriggerMetadata]

    def create_auto_moderation_rule(self,
                                    guild_id: _model.types.Snowflake,
                                    /, 
                                    **fields: typing.Unpack[___create_auto_moderation_rule_hint]) -> HTTPMeddle[_model.objects.AutoModerationRule]:

        """
        Use :data:`.http.routes.create_auto_moderation_rule`.

        :param name:
            |dsrc| **name**
        :param event_type:
            |dsrc| **event_type**
        :param trigger_type:
            |dsrc| **trigger_type**
        :param enabled:
            |dsrc| **enabled**
        :param exempt_roles:
            |dsrc| **exempt_roles**
        :param exempt_channels:
            |dsrc| **exempt_channels**
        :param trigger_metadata:
            |dsrc| **trigger_metadata**
        :param actions:
            |dsrc| **actions**
        """

        path = [guild_id]

        json = fields

        def _resolve(data):
            core = _model.objects.AutoModerationRule(data)
            return core

        return self._request(_http.routes.create_auto_moderation_rule, _resolve, path, json = json)

    class ___update_auto_moderation_rule_hint(typing.TypedDict):

        name            : typing.Required[_model.types.String]
        event_type      : typing.Required[_model.types.Integer]
        enabled         : typing.Required[_model.types.Boolean]
        actions         : typing.Required[list[_model.protocols.AutoModerationAction]]
        exempt_roles    : typing.Required[list[_model.types.Snowflake]]
        exempt_channels : typing.Required[list[_model.types.Snowflake]]
        trigger_metadata: typing.Optional[_model.protocols.AutoModerationTriggerMetadata]

    def update_auto_moderation_rule(self,
                                    guild_id               : _model.types.Snowflake,
                                    auto_moderation_rule_id: _model.types.Snowflake,
                                    /, 
                                    **fields               : typing.Unpack[___update_auto_moderation_rule_hint]) -> HTTPMeddle[_model.objects.AutoModerationRule]:

        """
        Use :data:`.http.routes.update_auto_moderation_rule`.

        :param name:
            |dsrc| **name**
        :param event_type:
            |dsrc| **event_type**
        :param enabled:
            |dsrc| **enabled**
        :param exempt_roles:
            |dsrc| **exempt_roles**
        :param exempt_channels:
            |dsrc| **exempt_channels**
        :param trigger_metadata:
            |dsrc| **trigger_metadata**
        :param actions:
            |dsrc| **actions**
        """

        path = [guild_id, auto_moderation_rule_id]

        json = fields

        def _resolve(data):
            core = _model.objects.AutoModerationRule(data)
            return core

        return self._request(_http.routes.update_auto_moderation_rule, _resolve, path, json = json)

    class ___delete_auto_moderation_rule_hint(typing.TypedDict):

        pass

    def delete_auto_moderation_rule(self,
                                    guild_id               : _model.types.Snowflake,
                                    auto_moderation_rule_id: _model.types.Snowflake,
                                    /, 
                                    **fields: typing.Unpack[___delete_auto_moderation_rule_hint]) -> HTTPMeddle[_model.objects.AutoModerationRule]:

        """
        Use :data:`.http.routes.delete_auto_moderation_rule`.
        """

        path = [guild_id, auto_moderation_rule_id]

        def _resolve(data):
            core = _model.objects.AutoModerationRule(data)
            return core

        return self._request(_http.routes.delete_auto_moderation_rule, _resolve, path)

    class ___get_channel_hint(typing.TypedDict):

        pass

    def get_channel(self,
                    channel_id: _model.types.Snowflake,
                    /, 
                    **fields  : typing.Unpack[___get_channel_hint]) -> HTTPMeddle[_model.objects.Channel]:

        """
        Use :data:`.http.routes.get_channel`.
        """

        path = [channel_id]

        def _resolve(data):
            core = _model.objects.Channel(data)
            return core

        return self._request(_http.routes.get_channel, _resolve, path)
    
    class ___update_channel_hint(typing.TypedDict):

        name: typing.Optional[_model.types.String]
        icon: typing.Optional[_model.types.String]
    
    @typing.overload
    def update_channel(self,
                       channel_id: _model.types.Snowflake,
                       /, 
                       **fields  : typing.Unpack[___update_channel_hint]) -> HTTPMeddle[_model.objects.Channel]:

        ...

    class ___update_channel_hint(typing.TypedDict):

        name                              : typing.Optional[_model.types.String]
        type                              : typing.Optional[_model.types.Integer]
        position                          : typing.Optional[None | _model.types.Integer]
        topic                             : typing.Optional[None | _model.types.String]
        nsfw                              : typing.Optional[None | _model.types.Boolean]
        rate_limit_per_user               : typing.Optional[None | _model.types.Integer]
        bitrate                           : typing.Optional[None | _model.types.Integer]
        user_limit                        : typing.Optional[None | _model.types.Integer]
        permission_overwrites             : typing.Optional[None | list[_model.protocols.Overwrite]]
        parent_id                         : typing.Optional[None | _model.types.Snowflake]
        rtc_region                        : typing.Optional[None | _model.types.String]
        video_quality_mode                : typing.Optional[None | _model.types.Integer]
        default_auto_archive_duration     : typing.Optional[None | _model.types.Integer]
        flags                             : typing.Optional[_model.enums.ChannelFlags]
        available_tags                    : typing.Optional[list[_model.protocols.ForumTag]]
        default_reaction_emoji            : typing.Optional[None | _model.protocols.DefaultReaction]
        default_thread_rate_limit_per_user: typing.Optional[_model.types.Integer]
        default_sort_order                : typing.Optional[_model.types.Integer]
        default_forum_layout              : typing.Optional[_model.enums.ForumLayoutType]
    
    @typing.overload
    def update_channel(self,
                       channel_id: _model.types.Snowflake,
                       /, 
                       **fields  : typing.Unpack[___update_channel_hint]) -> HTTPMeddle[_model.objects.Channel]:

        ...

    class ___update_channel_hint(typing.TypedDict):

        name                 : typing.Optional[_model.types.String]
        archived             : typing.Optional[_model.types.Boolean]
        auto_archive_duration: typing.Optional[_model.types.Integer]
        locked               : typing.Optional[_model.types.Boolean]
        invitable            : typing.Optional[_model.types.Boolean]
        rate_limit_per_user  : typing.Optional[None | _model.types.Integer | None]
        flags                : typing.Optional[_model.types.Integer]
        applied_tags         : typing.Optional[list[_model.types.Snowflake]]

    def update_channel(self,
                       channel_id: _model.types.Snowflake,
                       /, 
                       **fields  : typing.Unpack[___update_channel_hint]) -> HTTPMeddle[_model.objects.Channel]:

        """
        Use :data:`.http.routes.update_channel`.

        :param name:
            |dsrc| **name**
        :param archived:
            |dsrc| **archived**
        :param auto_archive_duration:
            |dsrc| **auto_archive_duration**
        :param locked:
            |dsrc| **locked**
        :param invitable:
            |dsrc| **invitable**
        :param rate_limit_per_user:
            |dsrc| **rate_limit_per_user**
        :param flags:
            |dsrc| **flags**
        :param applied_tags:
            |dsrc| **applied_tags**
        """

        path = [channel_id]

        json = fields

        def _resolve(data):
            core = _model.objects.Channel(data)
            return core

        return self._request(_http.routes.update_channel, _resolve, path, json = json)

    class ___delete_channel_hint(typing.TypedDict):

        pass

    def delete_channel(self,
                       channel_id: _model.types.Snowflake,
                       /, 
                       **fields  : typing.Unpack[___delete_channel_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.delete_channel`.
        """

        path = [channel_id]

        def _resolve(data):
            return None

        return self._request(_http.routes.delete_channel, _resolve, path)

    class ___get_messages_hint(typing.TypedDict):

        around: typing.Optional[_model.types.Snowflake]
        before: typing.Optional[_model.types.Snowflake]
        after : typing.Optional[_model.types.Snowflake]
        limit : typing.Optional[_model.types.Integer]

    def get_messages(self,
                     channel_id: _model.types.Snowflake,
                     /, 
                     **fields  : typing.Unpack[___get_messages_hint]) -> HTTPMeddle[list[_model.objects.Message]]:

        """
        Use :data:`.http.routes.get_messages`.

        :param around:
            |dsrc| **around**
        :param before:
            |dsrc| **before**
        :param after:
            |dsrc| **after**
        :param limit:
            |dsrc| **limit**
        """

        path = [channel_id]

        query = fields

        def _resolve(data):
            return list(map(_model.objects.Message, data))

        return self._request(_http.routes.get_messages, _resolve, path, query = query)

    class ___get_message_hint(typing.TypedDict):

        pass

    def get_message(self,
                    channel_id: _model.types.Snowflake,
                    message_id: _model.types.Snowflake,
                    /, 
                    **fields  : typing.Unpack[___get_message_hint]) -> HTTPMeddle[_model.objects.Message]:

        """
        Use :data:`.http.routes.get_message`.
        """

        path = [channel_id, message_id]

        def _resolve(data):
            core = _model.objects.Message(data)
            return core

        return self._request(_http.routes.get_message, _resolve, path)

    class ___create_message_hint(typing.TypedDict):

        content          : typing.Optional[_model.types.String]
        nonce            : _model.types.Integer | _model.types.String | None
        tts              : typing.Optional[_model.types.Boolean]
        message_reference: typing.Optional[_model.protocols.MessageReference]
        sticker_ids      : typing.Optional[list[_model.types.Snowflake]]
        files            : typing.Optional[list[io.BytesIO]]
        flags            : typing.Optional[_model.types.Integer]
        embeds           : typing.Optional[list[_model.protocols.Embed]]
        allowed_mentions : typing.Optional[_model.protocols.AllowedMentions]
        components       : typing.Optional[list[_model.protocols.MessageActionRowComponent | _model.protocols.MessageButtonComponent | _model.protocols.MessageTextInputComponent | _model.protocols.MessageSelectMenuComponent]]
        attachments      : typing.Optional[list[_model.protocols.Attachment]]

    def create_message(self,
                       channel_id: _model.types.Snowflake,
                       /, 
                       **fields  : typing.Unpack[___create_message_hint]) -> HTTPMeddle[_model.objects.Message]:

        """
        Use :data:`.http.routes.create_message`.

        :param content:
            |dsrc| **content**
        :param nonce:
            |dsrc| **nonce**
        :param tts:
            |dsrc| **tts**
        :param message_reference:
            |dsrc| **message_reference**
        :param sticker_ids:
            |dsrc| **sticker_ids**
        :param files:
            |dsrc| **files[n]**
        :param flags:
            |dsrc| **flags**
        :param embeds:
            |dsrc| **embeds**
        :param allowed_mentions:
            |dsrc| **allowed_mentions**
        :param components:
            |dsrc| **components**
        :param attachments:
            |dsrc| **attachments**
        """

        path = [channel_id]

        files = fields.pop('files', None)

        json = fields

        def _resolve(data):
            core = _model.objects.Message(data)
            return core

        return self._request(_http.routes.create_message, _resolve, path, json = json, files = files)

    class ___create_message_crosspost_hint(typing.TypedDict):

        pass

    def create_message_crosspost(self,
                                 channel_id: _model.types.Snowflake,
                                 message_id: _model.types.Snowflake,
                                 /, 
                                 **fields  : typing.Unpack[___create_message_crosspost_hint]) -> HTTPMeddle[_model.objects.Message]:

        """
        Use :data:`.http.routes.create_message_crosspost`.
        """

        path = [channel_id, message_id]

        def _resolve(data):
            core = _model.objects.Message(data)
            return core

        return self._request(_http.routes.create_message_crosspost, _resolve, path)

    class ___create_reaction_hint(typing.TypedDict):

        emoji: typing.Required[_model.types.String]

    def create_reaction(self,
                        channel_id: _model.types.Snowflake,
                        message_id: _model.types.Snowflake,
                        emoji     : _model.types.String,
                        /, 
                        **fields  : typing.Unpack[___create_reaction_hint]) -> HTTPMeddle[_model.objects.Reaction]:

        """
        Use :data:`.http.routes.create_reaction`.
        """

        path = [channel_id, message_id, emoji]

        def _resolve(data):
            core = _model.objects.Reaction(data)
            return core

        return self._request(_http.routes.create_reaction, _resolve, path)

    class ___delete_own_reaction_hint(typing.TypedDict):

        pass

    def delete_own_reaction(self,
                            channel_id: _model.types.Snowflake,
                            message_id: _model.types.Snowflake,
                            emoji     : _model.types.String,
                            /, 
                            **fields  : typing.Unpack[___delete_own_reaction_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.delete_own_reaction`.
        """

        path = [channel_id, message_id, emoji]

        def _resolve(data):
            return None

        return self._request(_http.routes.delete_own_reaction, _resolve, path)

    class ___delete_user_reaction_hint(typing.TypedDict):

        pass

    def delete_user_reaction(self,
                             channel_id: _model.types.Snowflake,
                             message_id: _model.types.Snowflake,
                             emoji     : _model.types.String,
                             user_id   : _model.types.Snowflake,
                             /, 
                             **fields  : typing.Unpack[___delete_user_reaction_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.delete_user_reaction`.
        """

        path = [channel_id, message_id, emoji, user_id]

        def _resolve(data):
            return None

        return self._request(_http.routes.delete_user_reaction, _resolve, path)

    class ___get_reactions_hint(typing.TypedDict):

        after: typing.Optional[_model.types.Snowflake]
        limit: typing.Optional[_model.types.Integer]

    def get_reactions(self,
                      channel_id: _model.types.Snowflake,
                      message_id: _model.types.Snowflake,
                      emoji     : _model.types.Snowflake,
                      /, 
                      **fields  : typing.Unpack[___get_reactions_hint]) -> HTTPMeddle[list[_model.objects.User]]:

        """
        Use :data:`.http.routes.get_reactions`.

        :param after:
            |dsrc| **after**
        :param limit:
            |dsrc| **limit**
        """

        path = [channel_id, message_id, emoji]

        query = fields

        def _resolve(data):
            return list(map(_model.objects.User, data))

        return self._request(_http.routes.get_reactions, _resolve, path, query = query)

    class ___delete_all_reactions_hint(typing.TypedDict):

        pass

    def delete_all_reactions(self,
                             channel_id: _model.types.Snowflake,
                             message_id: _model.types.Snowflake,
                             /, 
                             **fields  : typing.Unpack[___delete_all_reactions_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.delete_all_reactions`.
        """

        path = [channel_id, message_id]

        def _resolve(data):
            return None

        return self._request(_http.routes.delete_all_reactions, _resolve, path)

    class ___delete_all_emoji_reactions_hint(typing.TypedDict):

        pass

    def delete_all_emoji_reactions(self,
                                   channel_id: _model.types.Snowflake,
                                   message_id: _model.types.Snowflake,
                                   emoji     : _model.types.String,
                                   /, 
                                   **fields  : typing.Unpack[___delete_all_emoji_reactions_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.delete_all_emoji_reactions`.
        """

        path = [channel_id, message_id, emoji]

        def _resolve(data):
            return None

        return self._request(_http.routes.delete_all_emoji_reactions, _resolve, path)

    class ___update_message_hint(typing.TypedDict):

        content         : typing.Optional[_model.types.String]
        flags           : typing.Optional[_model.types.Integer]
        components      : typing.Optional[list[_model.protocols.MessageActionRowComponent | _model.protocols.MessageButtonComponent | _model.protocols.MessageTextInputComponent | _model.protocols.MessageSelectMenuComponent]]
        files           : typing.Optional[list[io.BytesIO]]
        embeds          : typing.Optional[list[_model.protocols.Embed]]
        allowed_mentions: typing.Optional[_model.protocols.AllowedMentions]
        attachments     : typing.Optional[list[_model.protocols.Attachment]]

    def update_message(self,
                       channel_id: _model.types.Snowflake,
                       message_id: _model.types.Snowflake,
                       /, 
                       **fields  : typing.Unpack[___update_message_hint]) -> HTTPMeddle[_model.objects.Message]:

        """
        Use :data:`.http.routes.update_message`.

        :param content:
            |dsrc| **content**
        :param flags:
            |dsrc| **flags**
        :param components:
            |dsrc| **components**
        :param files:
            |dsrc| **files[n]**
        :param embeds:
            |dsrc| **embeds**
        :param allowed_mentions:
            |dsrc| **allowed_mentions**
        :param attachments:
            |dsrc| **attachments**
        """

        path = [channel_id, message_id]

        files = fields.pop('files', None)

        json = fields

        def _resolve(data):
            core = _model.objects.Message(data)
            return core

        return self._request(_http.routes.update_message, _resolve, path, json = json, files = files)

    class ___delete_message_hint(typing.TypedDict):

        pass

    def delete_message(self,
                       channel_id: _model.types.Snowflake,
                       message_id: _model.types.Snowflake,
                       /, 
                       **fields  : typing.Unpack[___delete_message_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.delete_message`.
        """

        path = [channel_id, message_id]

        def _resolve(data):
            return None 

        return self._request(_http.routes.delete_message, _resolve, path)

    class ___delete_messages_hint(typing.TypedDict):

        messages: typing.Required[list[_model.types.Snowflake]]

    def delete_messages(self,
                        channel_id: _model.types.Snowflake,
                        /, 
                        **fields  : typing.Unpack[___delete_messages_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.delete_messages`.

        :param message_ids:
            |dsrc| **messages**
        """

        path = [channel_id]

        json = fields

        def _resolve(data):
            return None

        return self._request(_http.routes.delete_messages, _resolve, path, json = json)

    class ___update_channel_permissions_hint(typing.TypedDict):

        type : typing.Required[_model.types.Integer]
        allow: typing.Optional[_model.types.String]
        deny : typing.Optional[_model.types.String]

    def update_channel_permissions(self,
                                   channel_id  : _model.types.Snowflake,
                                   overwrite_id: _model.types.Snowflake,
                                   /, 
                                   **fields    : typing.Unpack[___update_channel_permissions_hint]) -> HTTPMeddle[None]:

        """
        :param allow:
            |dsrc| **allow**
        :param deny:
            |dsrc| **deny**
        :param type:
            |dsrc| **type**

        Use :data:`.http.routes.update_channel_permissions`.
        """

        path = [channel_id, overwrite_id]

        json = fields

        def _resolve(data):
            return None

        return self._request(_http.routes.update_channel_permissions, _resolve, path, json = json)

    class ___get_channel_invites_hint(typing.TypedDict):

        pass

    def get_channel_invites(self,
                            channel_id: _model.types.Snowflake,
                            /, 
                            **fields  : typing.Unpack[___get_channel_invites_hint]) -> HTTPMeddle[list[_model.objects.Invite]]:

        """
        Use :data:`.http.routes.get_channel_invites`.
        """

        path = [channel_id]

        def _resolve(data):
            return list(map(_model.objects.Invite, data))

        return self._request(_http.routes.get_channel_invites, _resolve, path)

    class ___create_channel_invite_hint(typing.TypedDict):

        max_age              : typing.Required[_model.types.Integer]
        max_uses             : typing.Required[_model.types.Integer]
        temporary            : typing.Required[_model.types.Boolean]
        unique               : typing.Required[_model.types.Boolean]
        target_type          : typing.Required[_model.types.Integer]
        target_user_id       : typing.Required[_model.types.Snowflake]
        target_application_id: typing.Required[_model.types.Snowflake]

    def create_channel_invite(self,
                              channel_id: _model.types.Snowflake,
                              /, 
                              **fields  : typing.Unpack[___create_channel_invite_hint]) -> HTTPMeddle[_model.objects.Invite]:

        """
        Use :data:`.http.routes.create_channel_invite`.

        :param max_age:
            |dsrc| **max_age**
        :param max_uses:
            |dsrc| **max_uses**
        :param temporary:
            |dsrc| **temporary**
        :param unique:
            |dsrc| **unique**
        :param target_type:
            |dsrc| **target_type**
        :param target_user_id:
            |dsrc| **target_user_id**
        :param target_application_id:
            |dsrc| **target_application_id**
        """

        path = [channel_id]

        json = fields

        def _resolve(data):
            core = _model.objects.Invite(data)
            return core

        return self._request(_http.routes.create_channel_invite, _resolve, path, json = json)

    class ___delete_channel_permission_hint(typing.TypedDict):

        pass

    def delete_channel_permission(self,
                                  channel_id  : _model.types.Snowflake,
                                  overwrite_id: _model.types.Snowflake,
                                  /, 
                                  **fields    : typing.Unpack[___delete_channel_permission_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.delete_channel_permission`.
        """

        path = [channel_id, overwrite_id]

        def _resolve(data):
            return None

        return self._request(_http.routes.delete_channel_permission, _resolve, path)

    class ___create_channel_follow_hint(typing.TypedDict):

        webhook_channel_id: _model.types.Snowflake

    def create_channel_follow(self,
                              channel_id: _model.types.Snowflake,
                              /, 
                              **fields  : typing.Unpack[___create_channel_follow_hint]) -> HTTPMeddle[_model.objects.FollowedChannel]:

        """
        Use :data:`.http.routes.create_channel_follow`.

        :param webhook_channel_id:
            |dsrc| **webhook_channel_id**
        """

        path = [channel_id]

        json = fields

        def _resolve(data):
            core = _model.objects.FollowedChannel(data)
            return core

        return self._request(_http.routes.create_channel_follow, _resolve, path, json = json)

    class ___create_typing_indicator_hint(typing.TypedDict):

        pass

    def create_typing_indicator(self,
                                channel_id: _model.types.Snowflake,
                                /, 
                                **fields  : typing.Unpack[___create_typing_indicator_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.create_typing_indicator`.
        """

        path = [channel_id]

        def _resolve(data):
            return None

        return self._request(_http.routes.create_typing_indicator, _resolve, path)

    class ___get_channel_pins_hint(typing.TypedDict):

        pass

    def get_channel_pins(self,
                         channel_id: _model.types.Snowflake,
                         /, 
                         **fields  : typing.Unpack[___get_channel_pins_hint]) -> HTTPMeddle[list[_model.objects.Message]]:

        """
        Use :data:`.http.routes.get_channel_pins`.
        """

        path = [channel_id]

        def _resolve(data):
            core = _model.objects.Message(data)
            return core

        return self._request(_http.routes.get_channel_pins, _resolve, path)

    class ___create_channel_pin_hint(typing.TypedDict):

        pass

    def create_channel_pin(self,
                           channel_id: _model.types.Snowflake,
                           message_id: _model.types.Snowflake,
                           /, 
                           **fields  : typing.Unpack[___create_channel_pin_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.create_channel_pin`.
        """

        path = [channel_id, message_id]

        def _resolve(data):
            return None

        return self._request(_http.routes.create_channel_pin, _resolve, path)

    class ___delete_channel_pin_hint(typing.TypedDict):

        pass

    def delete_channel_pin(self,
                           channel_id: _model.types.Snowflake,
                           message_id: _model.types.Snowflake,
                           /, 
                           **fields  : typing.Unpack[___delete_channel_pin_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.delete_channel_pin`.
        """

        path = [channel_id, message_id]

        def _resolve(data):
            return None

        return self._request(_http.routes.delete_channel_pin, _resolve, path)

    class ___create_channel_recipient_hint(typing.TypedDict):

        access_token: typing.Required[_model.types.String]
        nick        : typing.Required[_model.types.String]

    def create_channel_recipient(self,
                                 channel_id: _model.types.Snowflake,
                                 user_id   : _model.types.Snowflake,
                                 /, 
                                 **fields  : typing.Unpack[___create_channel_recipient_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.create_channel_recipient`.

        :param access_token:
            |dsrc| **access_token**
        :param nick:
            |dsrc| **nick**
        """

        path = [channel_id, user_id]

        json = fields

        def _resolve(data):
            return None

        return self._request(_http.routes.create_channel_recipient, _resolve, path, json = json)

    class ___delete_channel_recipient_hint(typing.TypedDict):

        pass

    def delete_channel_recipient(self,
                                 channel_id: _model.types.Snowflake,
                                 user_id   : _model.types.Snowflake,
                                 /, 
                                 **fields  : typing.Unpack[___delete_channel_recipient_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.delete_channel_recipient`.
        """

        path = [channel_id, user_id]

        def _resolve(data):
            return None

        return self._request(_http.routes.delete_channel_recipient, _resolve, path)

    class ___create_message_thread_hint(typing.TypedDict):

        name                 : typing.Required[_model.types.String]
        auto_archive_duration: typing.Optional[_model.types.Integer]
        rate_limit_per_user  : typing.Optional[_model.types.Integer]

    def create_message_thread(self,
                              channel_id: _model.types.Snowflake,
                              message_id: _model.types.Snowflake,
                              /, 
                              **fields  : typing.Unpack[___create_message_thread_hint]) -> HTTPMeddle[_model.objects.Channel]:

        """
        Use :data:`.http.routes.create_message_thread`.

        :param name:
            |dsrc| **name**
        :param auto_archive_duration:
            |dsrc| **auto_archive_duration**
        :param rate_limit_per_user:
            |dsrc| **rate_limit_per_user**
        """

        path = [channel_id, message_id]

        json = fields

        def _resolve(data):
            core = _model.objects.Channel(data)
            return core

        return self._request(_http.routes.create_message_thread, _resolve, path, json = json)

    class ___create_thread_hint(typing.TypedDict):

        name                 : typing.Required[_model.types.String]
        auto_archive_duration: typing.Optional[_model.types.Integer]
        type                 : typing.Optional[_model.types.Integer]
        invitable            : typing.Optional[_model.types.Boolean]
        rate_limit_per_user  : typing.Optional[_model.types.Integer]

    @typing.overload
    def create_thread(self,
                      channel_id: _model.types.Snowflake,
                      /, 
                      **fields  : typing.Unpack[___create_thread_hint]) -> HTTPMeddle[_model.objects.Channel]:
        
        ...

    class ___create_thread_hint(typing.TypedDict):

        name                 : typing.Required[_model.types.String]
        auto_archive_duration: typing.Optional[_model.types.Integer]
        rate_limit_per_user  : typing.Optional[_model.types.Integer]
        message              : typing.Optional[_model.protocols.Message]
        applied_tags         : list[_model.types.Snowflake]

    @typing.overload
    def create_thread(self,
                      channel_id: _model.types.Snowflake,
                      /, 
                      **fields  : typing.Unpack[___create_thread_hint]) -> HTTPMeddle[_model.objects.Channel]:
        
        ...

    def create_thread(self,
                      channel_id,
                      /, 
                      **fields):

        """
        Use :data:`.http.routes.create_thread`.

        :param name:
            |dsrc| **name**
        :param auto_archive_duration:
            |dsrc| **auto_archive_duration**
        :param type:
            |dsrc| **type**
        :param invitable:
            |dsrc| **invitable**
        :param rate_limit_per_user:
            |dsrc| **rate_limit_per_user**
        :param message:
            |dsrc| **message**
        :param applied_tags:
            |dsrc| **applied_tags**
        """

        path = [channel_id]

        files = fields.pop('files', None)

        json = fields

        def _resolve(data):
            core = _model.objects.Channel(data)
            return core

        return self._request(_http.routes.create_thread, _resolve, path, json = json, files = files)

    class ___create_self_thread_member_hint(typing.TypedDict):

        pass

    def create_self_thread_member(self,
                                  channel_id: _model.types.Snowflake,
                                  /, 
                                  **fields  : typing.Unpack[___create_self_thread_member_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.create_self_thread_member`.
        """

        path = [channel_id]

        def _resolve(data):
            return None

        return self._request(_http.routes.create_self_thread_member, _resolve, path)

    class ___create_thread_member_hint(typing.TypedDict):

        pass

    def create_thread_member(self,
                             channel_id: _model.types.Snowflake,
                             user_id   : _model.types.Snowflake,
                             /, 
                             **fields  : typing.Unpack[___create_thread_member_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.create_thread_member`.
        """

        path = [channel_id, user_id]

        def _resolve(data):
            return None

        return self._request(_http.routes.create_thread_member, _resolve, path)

    class ___delete_self_thread_member_hint(typing.TypedDict):

        pass

    def delete_self_thread_member(self,
                                  channel_id: _model.types.Snowflake,
                                  /, 
                                  **fields  : typing.Unpack[___delete_self_thread_member_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.delete_self_thread_member`.
        """

        path = [channel_id]

        def _resolve(data):
            return None

        return self._request(_http.routes.delete_self_thread_member, _resolve, path)

    class ___delete_thread_member_hint(typing.TypedDict):

        pass

    def delete_thread_member(self,
                             channel_id: _model.types.Snowflake,
                             user_id   : _model.types.Snowflake,
                             /, 
                             **fields  : typing.Unpack[___delete_thread_member_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.delete_thread_member`.
        """

        path = [channel_id, user_id]

        def _resolve(data):
            return None

        return self._request(_http.routes.delete_thread_member, _resolve, path)

    class ___get_thread_member_hint(typing.TypedDict):

        with_member: typing.Optional[_model.types.Boolean]

    def get_thread_member(self,
                          channel_id: _model.types.Snowflake,
                          user_id   : _model.types.Snowflake,
                          /, 
                          **fields  : typing.Unpack[___get_thread_member_hint]) -> HTTPMeddle[_model.objects.ThreadMember]:

        """
        Use :data:`.http.routes.get_thread_member`.

        :param with_member:
            |dsrc| **with_member**
        """

        path = [channel_id, user_id]

        query = fields

        def _resolve(data):
            core = _model.objects.ThreadMember(data)
            return core

        return self._request(_http.routes.get_thread_member, _resolve, path, query = query)

    class ___get_thread_members_hint(typing.TypedDict):

        with_member: typing.Optional[_model.types.Boolean]
        after      : typing.Optional[_model.types.Snowflake]
        limit      : typing.Optional[_model.types.Integer]

    def get_thread_members(self,
                           channel_id: _model.types.Snowflake,
                           /, 
                           **fields  : typing.Unpack[___get_thread_members_hint]) -> HTTPMeddle[list[_model.objects.ThreadMember]]:

        """
        When with_member is set to true, the results will be paginated and each thread member object will include a member field containing a guild member object.

        :param with_member:
            |dsrc| **with_member**
        :param after:
            |dsrc| **after**
        :param limit:
            |dsrc| **limit**

        Use :data:`.http.routes.get_thread_members`.
        """

        path = [channel_id]

        query = fields

        def _resolve(data):
            return list(map(_model.objects.ThreadMember, data))

        return self._request(_http.routes.get_thread_members, _resolve, path, query = query)

    class ___get_public_archived_threads_hint(typing.TypedDict):

        before: typing.Optional[_model.types.ISO8601Timestamp]
        limit : typing.Optional[_model.types.Integer]

    def get_public_archived_threads(self,
                                    channel_id: _model.types.Snowflake,
                                    /, 
                                    **fields  : typing.Unpack[___get_public_archived_threads_hint]) -> HTTPMeddle[_model.responses.get_public_archived_threads]:

        """
        Use :data:`.http.routes.get_public_archived_threads`.

        :param before:
            |dsrc| **before**
        :param limit:
            |dsrc| **limit**
        """

        path = [channel_id]

        query = fields

        def _resolve(data):
            data_threads = data['threads']
            core_threads = list(map(_model.objects.Channel, data_threads))
            data_thread_members = data['thread_members']
            core_thread_members = list(map(_model.objects.Channel, data_thread_members))
            data_outstanding = data['outstanding']
            core_outstanding = list(map(_model.objects.Channel, data_outstanding))
            core = _model.responses.get_public_archived_threads(core_threads, core_thread_members, core_outstanding)
            return core

        return self._request(_http.routes.get_public_archived_threads, _resolve, path, query = query)

    class ___get_private_archived_threads_hint(typing.TypedDict):

        before: typing.Optional[_model.types.ISO8601Timestamp]
        limit : typing.Optional[_model.types.Integer]

    def get_private_archived_threads(self,
                                     channel_id: _model.types.Snowflake,
                                     /, 
                                     **fields  : typing.Unpack[___get_private_archived_threads_hint]) -> HTTPMeddle[_model.responses.get_public_archived_threads]:

        """
        Use :data:`.http.routes.get_private_archived_threads`.

        :param before:
            |dsrc| **before**
        :param limit:
            |dsrc| **limit**
        """

        path = [channel_id]

        query = fields

        def _resolve(data):
            data_threads = data['threads']
            core_threads = list(map(_model.objects.Channel, data_threads))
            data_thread_members = data['thread_members']
            core_thread_members = list(map(_model.objects.Channel, data_thread_members))
            data_outstanding = data['outstanding']
            core_outstanding = list(map(_model.objects.Channel, data_outstanding))
            core = _model.responses.get_private_archived_threads(core_threads, core_thread_members, core_outstanding)
            return core

        return self._request(_http.routes.get_private_archived_threads, _resolve, path, query = query)
    
    class ___get_self_private_archived_threads_hint(typing.TypedDict):

        before: typing.Optional[_model.types.ISO8601Timestamp]
        limit : typing.Optional[_model.types.Integer]
    
    def get_self_private_archived_threads(self,
                                     channel_id: _model.types.Snowflake,
                                     /, 
                                     **fields  : typing.Unpack[___get_self_private_archived_threads_hint]) -> HTTPMeddle[_model.responses.get_self_private_archived_threads]:

        """
        Use :data:`.http.routes.get_self_private_archived_threads`.

        :param before:
            |dsrc| **before**
        :param limit:
            |dsrc| **limit**
        """

        path = [channel_id]

        query = fields

        def _resolve(data):
            data_threads = data['threads']
            core_threads = list(map(_model.objects.Channel, data_threads))
            data_thread_members = data['thread_members']
            core_thread_members = list(map(_model.objects.Channel, data_thread_members))
            data_outstanding = data['outstanding']
            core_outstanding = list(map(_model.objects.Channel, data_outstanding))
            core = _model.responses.get_self_private_archived_threads(core_threads, core_thread_members, core_outstanding)
            return core

        return self._request(_http.routes.get_self_private_archived_threads, _resolve, path, query = query)

    class ___get_guild_emojis_hint(typing.TypedDict):

        pass

    def get_guild_emojis(self,
                         guild_id: _model.types.Snowflake,
                         /, 
                         **fields: typing.Unpack[___get_guild_emojis_hint]) -> HTTPMeddle[list[_model.objects.Emoji]]:

        """
        Use :data:`.http.routes.get_guild_emojis`.
        """

        path = [guild_id]

        def _resolve(data):
            return list(map(_model.objects.Emoji, data))

        return self._request(_http.routes.get_guild_emojis, _resolve, path)

    class ___get_guild_emoji_hint(typing.TypedDict):

        pass

    def get_guild_emoji(self,
                        guild_id: _model.types.Snowflake,
                        emoji_id: _model.types.Snowflake,
                        /, 
                        **fields: typing.Unpack[___get_guild_emoji_hint]) -> HTTPMeddle[_model.objects.Emoji]:

        """
        Use :data:`.http.routes.get_guild_emoji`.
        """

        path = [guild_id, emoji_id]

        def _resolve(data):
            core = _model.objects.Emoji(data)
            return core

        return self._request(_http.routes.get_guild_emoji, _resolve, path)

    class ___create_guild_emoji_hint(typing.TypedDict):

        name : typing.Required[_model.types.String]
        image: typing.Required[_model.types.String]
        roles: typing.Required[list[_model.types.Snowflake]]

    def create_guild_emoji(self,
                           guild_id: _model.types.Snowflake,
                           /, 
                           **fields: typing.Unpack[___create_guild_emoji_hint]) -> HTTPMeddle[_model.objects.Emoji]:

        """
        Use :data:`.http.routes.create_guild_emoji`.

        :param name:
            |dsrc| **name**
        :param image:
            |dsrc| **image**
        :param roles:
            |dsrc| **roles**
        """

        path = [guild_id]

        json = fields

        def _resolve(data):
            core = _model.objects.Emoji(data)
            return core

        return self._request(_http.routes.create_guild_emoji, _resolve, path, json = json)

    class ___update_guild_emoji_hint(typing.TypedDict):

        name : typing.Required[_model.types.String]
        roles: typing.Required[list[_model.types.Snowflake] | None]

    def update_guild_emoji(self,
                           guild_id: _model.types.Snowflake,
                           emoji_id: _model.types.Snowflake,
                           /, 
                           **fields: typing.Unpack[___update_guild_emoji_hint]) -> HTTPMeddle[_model.objects.Emoji]:

        """
        Use :data:`.http.routes.update_guild_emoji`.

        :param name:
            |dsrc| **name**
        :param roles:
            |dsrc| **roles**
        """

        path = [guild_id, emoji_id]

        json = fields

        def _resolve(data):
            core = _model.objects.Emoji(data)
            return core

        return self._request(_http.routes.update_guild_emoji, _resolve, path, json = json)

    class ___delete_guild_emoji_hint(typing.TypedDict):

        pass

    def delete_guild_emoji(self,
                           guild_id: _model.types.Snowflake,
                           emoji_id: _model.types.Snowflake,
                           /, 
                           **fields: typing.Unpack[___delete_guild_emoji_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.delete_guild_emoji`.

        :param name:
            |dsrc| **name**
        :param roles:
            |dsrc| **roles**
        """

        path = [guild_id, emoji_id]

        def _resolve(data):
            return None

        return self._request(_http.routes.delete_guild_emoji, _resolve, path)

    class ___create_guild_hint(typing.TypedDict):

        name                         : typing.Required[_model.types.String]
        region                       : typing.Optional[_model.types.String]
        icon                         : typing.Optional[_model.types.String]
        verification_level           : typing.Optional[_model.types.Integer]
        default_message_notifications: typing.Optional[_model.types.Integer]
        explicit_content_filter      : typing.Optional[_model.types.Integer]
        afk_channel_id               : typing.Optional[_model.types.Snowflake]
        afk_timeout                  : typing.Optional[_model.types.Integer]
        system_channel_id            : typing.Optional[_model.types.Snowflake]
        system_channel_flags         : typing.Optional[_model.types.Integer]
        roles                        : typing.Optional[list[_model.protocols.Role]]
        channels                     : typing.Optional[list[_model.protocols.Channel]]

    def create_guild(self,
                     /, 
                     **fields: typing.Unpack[___create_guild_hint]) -> HTTPMeddle[_model.objects.Guild]:

        """
        Use :data:`.http.routes.create_guild`.

        :param name:
            |dsrc| **name**
        :param region:
            |dsrc| **region**
        :param icon:
            |dsrc| **icon**
        :param verification_level:
            |dsrc| **verification_level**
        :param default_message_notifications:
            |dsrc| **default_message_notifications**
        :param explicit_content_filter:
            |dsrc| **explicit_content_filter**
        :param afk_channel_id:
            |dsrc| **afk_channel_id**
        :param afk_timeout:
            |dsrc| **afk_timeout**
        :param system_channel_id:
            |dsrc| **system_channel_id**
        :param system_channel_flags:
            |dsrc| **system_channel_flags**
        :param roles:
            |dsrc| **roles**
        :param channels:
            |dsrc| **channels**
        """

        path = []

        json = fields

        def _resolve(data):
            core = _model.objects.Guild(data)
            return core

        return self._request(_http.routes.create_guild, _resolve, path, json = json)

    class ___get_guild_hint(typing.TypedDict):

        with_counts: typing.Optional[_model.types.Boolean]

    def get_guild(self,
                  guild_id: _model.types.Snowflake,
                  /, 
                  **fields: typing.Unpack[___get_guild_hint]) -> HTTPMeddle[_model.objects.Guild]:

        """
        Use :data:`.http.routes.get_guild`.

        :param with_counts:
            |dsrc| **with_counts**
        """
        
        path = [guild_id]

        query = fields

        def _resolve(data):
            core = _model.objects.Guild(data)
            return core

        return self._request(_http.routes.get_guild, _resolve, path, query = query)

    class ___get_guild_preview_hint(typing.TypedDict):

        pass

    def get_guild_preview(self,
                          guild_id: _model.types.Snowflake,
                          /, 
                          **fields: typing.Unpack[___get_guild_preview_hint]) -> HTTPMeddle[_model.objects.Guild]:

        """
        Use :data:`.http.routes.get_guild_preview`.
        """

        path = [guild_id]

        def _resolve(data):
            core = _model.objects.Guild(data)
            return core

        return self._request(_http.routes.get_guild_preview, _resolve, path)

    class ___update_guild_hint(typing.TypedDict):

        name                         : typing.Optional[_model.types.String]
        region                       : typing.Optional[_model.types.String]
        verification_level           : typing.Optional[_model.types.Integer]
        default_message_notifications: typing.Optional[_model.types.Integer]
        explicit_content_filter      : typing.Optional[_model.types.Integer]
        afk_channel_id               : typing.Optional[_model.types.Snowflake]
        afk_timeout                  : typing.Optional[_model.types.Integer]
        icon                         : typing.Optional[_model.types.String]
        owner_id                     : typing.Optional[_model.types.Snowflake]
        splash                       : typing.Optional[_model.types.String]
        discovery_splash             : typing.Optional[_model.types.String]
        banner                       : typing.Optional[_model.types.String]
        system_channel_id            : typing.Optional[_model.types.Snowflake]
        system_channel_flags         : typing.Optional[_model.types.Integer]
        rules_channel_id             : typing.Optional[_model.types.Snowflake]
        public_updates_channel_id    : typing.Optional[_model.types.Snowflake]
        preferred_locale             : typing.Optional[_model.types.String]
        features                     : typing.Optional[list[_model.enums.GuildFeature]]
        description                  : typing.Optional[_model.types.String]
        premium_progress_bar_enabled : typing.Optional[_model.types.Boolean]

    def update_guild(self,
                     guild_id: _model.types.Snowflake,
                     /, 
                     **fields: typing.Unpack[___update_guild_hint]) -> HTTPMeddle[_model.objects.Guild]:

        """
        Use :data:`.http.routes.update_guild`.

        :param name:
            |dsrc| **name**
        :param region:
            |dsrc| **region**
        :param verification_level:
            |dsrc| **verification_level**
        :param default_message_notifications:
            |dsrc| **default_message_notifications**
        :param explicit_content_filter:
            |dsrc| **explicit_content_filter**
        :param afk_channel_id:
            |dsrc| **afk_channel_id**
        :param afk_timeout:
            |dsrc| **afk_timeout**
        :param icon:
            |dsrc| **icon**
        :param owner_id:
            |dsrc| **owner_id**
        :param splash:
            |dsrc| **splash**
        :param discovery_splash:
            |dsrc| **discovery_splash**
        :param banner:
            |dsrc| **banner**
        :param system_channel_id:
            |dsrc| **system_channel_id**
        :param system_channel_flags:
            |dsrc| **system_channel_flags**
        :param rules_channel_id:
            |dsrc| **rules_channel_id**
        :param public_updates_channel_id:
            |dsrc| **public_updates_channel_id**
        :param preferred_locale:
            |dsrc| **preferred_locale**
        :param features:
            |dsrc| **features**
        :param description:
            |dsrc| **description**
        :param premium_progress_bar_enabled:
            |dsrc| **premium_progress_bar_enabled**
        """

        path = [guild_id]

        json = fields

        def _resolve(data):
            core = _model.objects.Guild(data)
            return core

        return self._request(_http.routes.update_guild, _resolve, path, json = json)

    class ___delete_guild_hint(typing.TypedDict):

        pass

    def delete_guild(self,
                     guild_id: _model.types.Snowflake,
                     /, 
                     **fields: typing.Unpack[___delete_guild_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.delete_guild`.
        """

        path = [guild_id]

        def _resolve(data):
            return None

        return self._request(_http.routes.delete_guild, _resolve, path)

    class ___get_guild_channels_hint(typing.TypedDict):

        pass

    def get_guild_channels(self,
                           guild_id: _model.types.Snowflake,
                           /, 
                           **fields: typing.Unpack[___get_guild_channels_hint]) -> HTTPMeddle[list[_model.objects.Channel]]:

        """
        Use :data:`.http.routes.get_guild_channels`.
        """

        path = [guild_id]

        def _resolve(data):
            core = _model.objects.Channel(data)
            return core

        return self._request(_http.routes.get_guild_channels, _resolve, path)

    class ___create_guild_channel_hint(typing.TypedDict):

        name                         : typing.Required[_model.types.String]
        type                         : typing.Optional[_model.types.Integer]
        topic                        : typing.Optional[_model.types.String]
        bitrate                      : typing.Optional[_model.types.Integer]
        user_limit                   : typing.Optional[_model.types.Integer]
        rate_limit_per_user          : typing.Optional[_model.types.Integer]
        position                     : typing.Optional[_model.types.Integer]
        parent_id                    : typing.Optional[_model.types.Snowflake]
        nsfw                         : typing.Optional[_model.types.Boolean]
        rtc_region                   : typing.Optional[_model.types.String]
        video_quality_mode           : typing.Optional[_model.types.Integer]
        default_auto_archive_duration: typing.Optional[_model.types.Integer]
        default_sort_order           : typing.Optional[_model.types.Integer]
        permission_overwrites        : typing.Optional[list[_model.protocols.Overwrite]]
        default_reaction_emoji       : typing.Optional[_model.protocols.DefaultReaction]
        available_tags               : typing.Optional[list[_model.protocols.ForumTag]]

    def create_guild_channel(self,
                             guild_id: _model.types.Snowflake,
                             /, 
                             **fields: typing.Unpack[___create_guild_channel_hint]) -> HTTPMeddle[_model.objects.Channel]:

        """
        Use :data:`.http.routes.create_guild_channel`.

        :param name:
            |dsrc| **name**
        :param type:
            |dsrc| **type**
        :param topic:
            |dsrc| **topic**
        :param bitrate:
            |dsrc| **bitrate**
        :param user_limit:
            |dsrc| **user_limit**
        :param rate_limit_per_user:
            |dsrc| **rate_limit_per_user**
        :param position:
            |dsrc| **position**
        :param parent_id:
            |dsrc| **parent_id**
        :param nsfw:
            |dsrc| **nsfw**
        :param rtc_region:
            |dsrc| **rtc_region**
        :param video_quality_mode:
            |dsrc| **video_quality_mode**
        :param default_auto_archive_duration:
            |dsrc| **default_auto_archive_duration**
        :param default_sort_order:
            |dsrc| **default_sort_order**
        :param permission_overwrites:
            |dsrc| **permission_overwrites**
        :param default_reaction_emoji:
            |dsrc| **default_reaction_emoji**
        :param available_tags:
            |dsrc| **available_tags**
        """

        path  = [guild_id]

        json = fields

        def _resolve(data):
            core = _model.objects.Channel(data)
            return core

        return self._request(_http.routes.create_guild_channel, _resolve, path, json = json)

    class ___update_guild_channel_positions_hint(typing.TypedDict):

        id              : _model.types.Snowflake
        position        : _model.types.Integer | None
        lock_permissions: _model.types.Boolean | None
        parent_id       : _model.types.Snowflake

    def update_guild_channel_positions(self,
                                       guild_id : _model.types.Snowflake,
                                       /, 
                                       positions: list[___update_guild_channel_positions_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.update_guild_channel_positions`.

        :param positions:
            An array of objects.

        Each element of :paramref:`.positions` must abide to the following:

        :param id:
            |dsrc| **id**
        :param position:
            |dsrc| **position**
        :param lock_permissions:
            |dsrc| **lock_permissions**
        :param parent_id:
            |dsrc| **parent_id**
        """

        path = [guild_id]

        json = positions

        def _resolve(data):
            return None

        return self._request(_http.routes.update_guild_channel_positions, _resolve, path, json = json)

    class ___get_active_guild_threads_hint(typing.TypedDict):

        pass

    def get_active_guild_threads(self,
                                 guild_id: _model.types.Snowflake,
                                 /, 
                                 **fields: typing.Unpack[___get_active_guild_threads_hint]) -> HTTPMeddle[_model.responses.get_active_guild_threads]:

        """
        Use :data:`.http.routes.get_active_guild_threads`.
        """

        path = [guild_id]

        def _resolve(data):
            data_threads = data['threads']
            core_threads = list(map(_model.objects.Channel, data_threads))
            data_thread_members = data['thread_members']
            core_thread_members = list(map(_model.objects.Channel, data_thread_members))
            core = _model.responses.get_active_guild_threads(core_threads, core_thread_members)
            return core

        return self._request(_http.routes.get_active_guild_threads, _resolve, path)

    class ___get_guild_member_hint(typing.TypedDict):

        pass

    def get_guild_member(self,
                         guild_id: _model.types.Snowflake,
                         user_id : _model.types.Snowflake,
                         /, 
                         **fields: typing.Unpack[___get_guild_member_hint]) -> HTTPMeddle[_model.objects.GuildMember]:

        """
        Use :data:`.http.routes.get_guild_member`.
        """

        path = [guild_id, user_id]

        def _resolve(data):
            core = _model.objects.GuildMember(data)
            return core

        return self._request(_http.routes.get_guild_member, _resolve, path)

    class ___get_guild_members_hint(typing.TypedDict):

        limit: typing.Required[_model.types.Integer]
        after: typing.Required[_model.types.Snowflake]

    def get_guild_members(self,
                          guild_id: _model.types.Snowflake,
                          /, 
                          **fields: typing.Unpack[___get_guild_members_hint]) -> HTTPMeddle[_model.objects.GuildMember]:

        """
        Use :data:`.http.routes.get_guild_members`.

        :param limit:
            |dsrc| **limit**
        :param after:
            |dsrc| **after**
        """

        path = [guild_id]

        query = fields

        def _resolve(data):
            core = _model.objects.GuildMember(data)
            return core

        return self._request(_http.routes.get_guild_members, _resolve, path, query = query)

    class ___search_guild_members_hint(typing.TypedDict):

        query: typing.Required[_model.types.String]
        limit: typing.Optional[_model.types.Integer]

    def search_guild_members(self,
                             guild_id: _model.types.Snowflake,
                             /, 
                             **fields: typing.Unpack[___search_guild_members_hint]) -> HTTPMeddle[list[_model.objects.GuildMember]]:

        """
        Use :data:`.http.routes.search_guild_members`.

        :param query:
            |dsrc| **query**
        :param limit:
            |dsrc| **limit**
        """

        path = [guild_id]

        query = fields

        def _resolve(data):
            return list(map(_model.objects.GuildMember, data))

        return self._request(_http.routes.search_guild_members, _resolve, path, query = query)

    class ___create_guild_member_hint(typing.TypedDict):

        access_token: typing.Required[_model.types.String]
        nick        : typing.Optional[_model.types.String]
        roles       : typing.Optional[list[_model.types.Snowflake]]
        mute        : typing.Optional[_model.types.Boolean]
        deaf        : typing.Optional[_model.types.Boolean]

    def create_guild_member(self,
                            guild_id: _model.types.Snowflake,
                            user_id : _model.types.Snowflake,
                            /, 
                            **fields: typing.Unpack[___create_guild_member_hint]) -> HTTPMeddle[_model.objects.GuildMember]:

        """
        Use :data:`.http.routes.create_guild_member`.

        :param access_token:
            |dsrc| **access_token**
        :param nick:
            |dsrc| **nick**
        :param roles:
            |dsrc| **roles**
        :param mute:
            |dsrc| **mute**
        :param deaf:
            |dsrc| **deaf**
        """

        path = [guild_id, user_id]

        json = fields

        def _resolve(data):
            core = _model.objects.GuildMember(data)
            return core

        return self._request(_http.routes.create_guild_member, _resolve, path, json = json)

    class ___update_guild_member_hint(typing.TypedDict):

        nick                        : typing.Optional[_model.types.String]
        roles                       : typing.Optional[list[_model.types.Snowflake]]
        mute                        : typing.Optional[_model.types.Boolean]
        deaf                        : typing.Optional[_model.types.Boolean]
        channel_id                  : typing.Optional[_model.types.Snowflake]
        communication_disabled_until: typing.Optional[_model.types.ISO8601Timestamp]
        flags                       : typing.Optional[_model.types.Integer]

    def update_guild_member(self,
                            guild_id: _model.types.Snowflake,
                            user_id : _model.types.Snowflake,
                            /, 
                            **fields: typing.Unpack[___update_guild_member_hint]) -> HTTPMeddle[_model.objects.GuildMember]:

        """
        Use :data:`.http.routes.update_guild_member`.

        :param nick:
            |dsrc| **nick**
        :param roles:
            |dsrc| **roles**
        :param mute:
            |dsrc| **mute**
        :param deaf:
            |dsrc| **deaf**
        :param channel_id:
            |dsrc| **channel_id**
        :param communication_disabled_until:
            |dsrc| **communication_disabled_until**
        :param flags:
            |dsrc| **flags**
        """

        path = [guild_id, user_id]

        json = fields

        def _resolve(data):
            core = _model.objects.GuildMember(data)
            return core

        return self._request(_http.routes.update_guild_member, _resolve, path, json = json)

    class ___update_self_guild_member_hint(typing.TypedDict):

        nick: typing.Optional[_model.types.String]

    def update_self_guild_member(self,
                                 guild_id: _model.types.Snowflake,
                                 /, 
                                 **fields: typing.Unpack[___update_self_guild_member_hint]) -> HTTPMeddle[_model.objects.GuildMember]:

        """
        Use :data:`.http.routes.update_self_guild_member`.

        :param nick:
            |dsrc| **nick**
        """

        path = [guild_id]

        json = fields

        def _resolve(data):
            core = _model.objects.GuildMember(data)
            return core

        return self._request(_http.routes.update_self_guild_member, _resolve, path, json = json)

    class ___create_guild_member_role_hint(typing.TypedDict):

        pass

    def create_guild_member_role(self,
                                 guild_id: _model.types.Snowflake,
                                 user_id : _model.types.Snowflake,
                                 role_id : _model.types.Snowflake,
                                 /, 
                                 **fields: typing.Unpack[___create_guild_member_role_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.create_guild_member_role`.
        """

        path = [guild_id, user_id, role_id]

        def _resolve(data):
            return None

        return self._request(_http.routes.create_guild_member_role, _resolve, path)

    class ___delete_guild_member_role_hint(typing.TypedDict):

        pass

    def delete_guild_member_role(self,
                                 guild_id: _model.types.Snowflake,
                                 user_id : _model.types.Snowflake,
                                 role_id : _model.types.Snowflake,
                                 /, 
                                 **fields: typing.Unpack[___delete_guild_member_role_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.delete_guild_member_role`.
        """

        path = [guild_id, user_id, role_id]

        def _resolve(data):
            return None

        return self._request(_http.routes.delete_guild_member_role, _resolve, path)

    class ___delete_guild_member_hint(typing.TypedDict):

        pass

    def delete_guild_member(self,
                            guild_id: _model.types.Snowflake,
                            user_id : _model.types.Snowflake,
                            /, 
                            **fields: typing.Unpack[___delete_guild_member_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.delete_guild_member`.
        """

        path = [guild_id, user_id]

        def _resolve(data):
            return None

        return self._request(_http.routes.delete_guild_member, _resolve, path)

    class ___get_guild_bans_hint(typing.TypedDict):

        limit : typing.Optional[_model.types.Integer]
        before: typing.Optional[_model.types.Snowflake]
        after : typing.Optional[_model.types.Snowflake]

    def get_guild_bans(self,
                       guild_id: _model.types.Snowflake,
                       /, 
                       **fields: typing.Unpack[___get_guild_bans_hint]) -> HTTPMeddle[list[_model.objects.Ban]]:

        """
        Use :data:`.http.routes.get_guild_bans`.

        :param limit:
            |dsrc| **limit**
        :param before:
            |dsrc| **before**
        :param after:
            |dsrc| **after**
        """

        path = [guild_id]

        query = fields

        def _resolve(data):
            return list(map(_model.objects.Ban, data))

        return self._request(_http.routes.get_guild_bans, _resolve, path, query = query)

    class ___get_guild_ban_hint(typing.TypedDict):

        pass

    def get_guild_ban(self,
                      guild_id: _model.types.Snowflake,
                      user_id : _model.types.Snowflake,
                      /, 
                      **fields: typing.Unpack[___get_guild_ban_hint]) -> HTTPMeddle[_model.objects.Ban]:

        """
        Use :data:`.http.routes.get_guild_ban`.
        """

        path = [guild_id, user_id]

        def _resolve(data):
            core = _model.objects.Ban(data)
            return core

        return self._request(_http.routes.get_guild_ban, _resolve, path)

    class ___create_guild_ban_hint(typing.TypedDict):

        delete_message_days   : typing.Optional[_model.types.Integer]
        delete_message_seconds: typing.Optional[_model.types.Integer]

    def create_guild_ban(self,
                         guild_id: _model.types.Snowflake,
                         user_id : _model.types.Snowflake,
                         /, 
                         **fields: typing.Unpack[___create_guild_ban_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.create_guild_ban`.
        """

        path = [guild_id, user_id]

        json = fields

        def _resolve(data):
            return None

        return self._request(_http.routes.create_guild_ban, _resolve, path, json = json)

    class ___delete_guild_ban_hint(typing.TypedDict):

        pass

    def delete_guild_ban(self,
                         guild_id: _model.types.Snowflake,
                         user_id : _model.types.Snowflake,
                         /, 
                         **fields: typing.Unpack[___delete_guild_ban_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.delete_guild_ban`.
        """

        path = [guild_id, user_id]

        def _resolve(data):
            return None

        return self._request(_http.routes.delete_guild_ban, _resolve, path)

    class ___get_guild_roles_hint(typing.TypedDict):

        pass

    def get_guild_roles(self,
                        guild_id: _model.types.Snowflake,
                        /, 
                        **fields: typing.Unpack[___get_guild_roles_hint]) -> HTTPMeddle[list[_model.objects.Role]]:

        """
        Use :data:`.http.routes.get_guild_roles`.
        """

        path = [guild_id]

        def _resolve(data):
            return list(map(_model.objects.Role, data))

        return self._request(_http.routes.get_guild_roles, _resolve, path)

    class ___create_guild_role_hint(typing.TypedDict):

        name         : typing.Optional[_model.types.String]
        permissions  : typing.Optional[_model.types.String]
        color        : typing.Optional[_model.types.Integer]
        hoist        : typing.Optional[_model.types.Boolean]
        icon         : typing.Optional[_model.types.String]
        unicode_emoji: typing.Optional[_model.types.String]
        mentionable  : typing.Optional[_model.types.Boolean]

    def create_guild_role(self,
                          guild_id: _model.types.Snowflake,
                          /, 
                          **fields: typing.Unpack[___create_guild_role_hint]) -> HTTPMeddle[_model.objects.Role]:

        """
        Use :data:`.http.routes.create_guild_role`.

        :param name:
            |dsrc| **name**
        :param permissions:
            |dsrc| **permissions**
        :param color:
            |dsrc| **color**
        :param hoist:
            |dsrc| **hoist**
        :param icon:
            |dsrc| **icon**
        :param unicode_emoji:
            |dsrc| **unicode_emoji**
        :param mentionable:
            |dsrc| **mentionable**
        """

        path = [guild_id]

        json = fields

        def _resolve(data):
            core = _model.objects.Role(data)
            return core

        return self._request(_http.routes.create_guild_role, _resolve, path, json = json)

    class ___update_guild_role_positions_hint(typing.TypedDict):

        id      : _model.types.Snowflake
        position: _model.types.Integer | None

    def update_guild_role_positions(self,
                                    guild_id: _model.types.Snowflake,
                                    /, 
                                    positions: list[___update_guild_role_positions_hint]) -> HTTPMeddle[list[_model.objects.Role]]:

        """
        Use :data:`.http.routes.update_guild_role_positions`.

        :param positions:
            An array of objects.

        Each element of :paramref:`.positions` must abide to the following:

        :param id:
            |dsrc| **id**
        :param position:
            |dsrc| **position**
        """

        path = [guild_id]

        json = positions

        def _resolve(data):
            return list(map(_model.objects.Role, data))

        return self._request(_http.routes.update_guild_role_positions, _resolve, path, json = json)

    class ___update_guild_role_hint(typing.TypedDict):

        name         : typing.Optional[_model.types.String]
        permissions  : typing.Optional[_model.types.String]
        color        : typing.Optional[_model.types.Integer]
        hoist        : typing.Optional[_model.types.Boolean]
        icon         : typing.Optional[_model.types.String]
        unicode_emoji: typing.Optional[_model.types.String]
        mentionable  : typing.Optional[_model.types.Boolean]

    def update_guild_role(self,
                          guild_id: _model.types.Snowflake,
                          role_id : _model.types.Snowflake,
                          /, 
                          **fields: typing.Unpack[___update_guild_role_hint]) -> HTTPMeddle[_model.objects.Role]:

        """
        Use :data:`.http.routes.update_guild_role`.

        :param name:
            |dsrc| **name**
        :param permissions:
            |dsrc| **permissions**
        :param color:
            |dsrc| **color**
        :param hoist:
            |dsrc| **hoist**
        :param icon:
            |dsrc| **icon**
        :param unicode_emoji:
            |dsrc| **unicode_emoji**
        :param mentionable:
            |dsrc| **mentionable**
        """

        path = [guild_id, role_id]

        json = fields

        def _resolve(data):
            core = _model.objects.Role(data)
            return core

        return self._request(_http.routes.update_guild_role, _resolve, path, json = json)

    class ___update_guild_mfa_level_hint(typing.TypedDict):

        level: typing.Required[_model.types.Integer]

    def update_guild_mfa_level(self,
                               guild_id: _model.types.Snowflake,
                               /, 
                               **fields: typing.Unpack[___update_guild_mfa_level_hint]) -> HTTPMeddle[_model.enums.GuildMFALevel]:

        """
        Use :data:`.http.routes.update_guild_mfa_level`.

        :param level:
            |dsrc| **level**
        """

        path = [guild_id]

        json = fields

        def _resolve(data):
            core = _model.enums.GuildMFALevel(data)
            return core

        return self._request(_http.routes.update_guild_mfa_level, _resolve, path, json = json)

    class ___delete_guild_role_hint(typing.TypedDict):

        pass

    def delete_guild_role(self,
                          guild_id: _model.types.Snowflake,
                          role_id : _model.types.Snowflake,
                          /, 
                          **fields: typing.Unpack[___delete_guild_role_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.delete_guild_role`.
        """

        path = [guild_id, role_id]

        def _resolve(data):
            return None

        return self._request(_http.routes.delete_guild_role, _resolve, path)

    class ___get_guild_prune_count_hint(typing.TypedDict):

        days         : typing.Required[_model.types.Integer]
        include_roles: typing.Required[list[_model.types.String]]

    def get_guild_prune_count(self,
                              guild_id: _model.types.Snowflake,
                              /, 
                              **fields: typing.Unpack[___get_guild_prune_count_hint]) -> HTTPMeddle[_model.types.Integer]:

        """
        Use :data:`.http.routes.get_guild_prune_count`.

        :param days:
            |dsrc| **days**
        :param include_roles:
            |dsrc| **include_roles**
        """

        path = [guild_id]

        query = fields

        def _resolve(data):
            core = _model.types.Integer(data['pruned'])
            return core

        return self._request(_http.routes.get_guild_prune_count, _resolve, path, query = query)

    class ___start_guild_prune_hint(typing.TypedDict):

        days               : typing.Required[_model.types.Integer]
        compute_prune_count: typing.Required[_model.types.Boolean]
        include_roles      : typing.Required[list[_model.types.Snowflake]]
        reason             : typing.Optional[_model.types.String]

    def start_guild_prune(self,
                          guild_id: _model.types.Snowflake,
                          /, 
                          **fields: typing.Unpack[___start_guild_prune_hint]) -> HTTPMeddle[_model.types.Integer]:

        """
        Use :data:`.http.routes.start_guild_prune`.

        :param days:
            |dsrc| **days**
        :param compute_prune_count:
            |dsrc| **compute_prune_count**
        :param include_roles:
            |dsrc| **include_roles**
        :param reason:
            |dsrc| **reason**
        """

        path = [guild_id]

        json = fields

        def _resolve(data):
            core = _model.types.Integer(data['pruned'])
            return core

        return self._request(_http.routes.start_guild_prune, _resolve, path, json = json)

    class ___get_guild_voice_regions_hint(typing.TypedDict):

        pass

    def get_guild_voice_regions(self,
                                guild_id: _model.types.Snowflake,
                                /, 
                                **fields: typing.Unpack[___get_guild_voice_regions_hint]) -> HTTPMeddle[list[_model.objects.VoiceRegion]]:

        """
        Use :data:`.http.routes.get_guild_voice_regions`.
        """

        path = [guild_id]

        def _resolve(data):
            return list(map(_model.objects.VoiceRegion, data))

        return self._request(_http.routes.get_guild_voice_regions, _resolve, path)

    class ___get_guild_invites_hint(typing.TypedDict):

        pass

    def get_guild_invites(self,
                          guild_id: _model.types.Snowflake,
                          /, 
                          **fields: typing.Unpack[___get_guild_invites_hint]) -> HTTPMeddle[list[_model.objects.Invite]]:

        """
        Use :data:`.http.routes.get_guild_invites`.
        """

        path = [guild_id]

        def _resolve(data):
            return list(map(_model.objects.Invite, data))

        return self._request(_http.routes.get_guild_invites, _resolve, path)

    class ___get_guild_integrations_hint(typing.TypedDict):

        pass

    def get_guild_integrations(self,
                               guild_id: _model.types.Snowflake,
                               /, 
                               **fields: typing.Unpack[___get_guild_integrations_hint]) -> HTTPMeddle[list[_model.objects.Integration]]:

        """
        Use :data:`.http.routes.get_guild_integrations`.
        """

        path = [guild_id]

        def _resolve(data):
            return list(map(_model.objects.Integration, data))

        return self._request(_http.routes.get_guild_integrations, _resolve, path)

    class ___delete_guild_integration_hint(typing.TypedDict):

        pass

    def delete_guild_integration(self,
                                 guild_id      : _model.types.Snowflake,
                                 integration_id: _model.types.Snowflake,
                                 /, 
                                 **fields: typing.Unpack[___delete_guild_integration_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.delete_guild_integration`.
        """

        path = [guild_id, integration_id]

        def _resolve(data):
            return None

        return self._request(_http.routes.delete_guild_integration, _resolve, path)

    class ___get_guild_widget_settings_hint(typing.TypedDict):

        pass

    def get_guild_widget_settings(self,
                                  guild_id: _model.types.Snowflake,
                                  /, 
                                  **fields: typing.Unpack[___get_guild_widget_settings_hint]) -> HTTPMeddle[_model.objects.GuildWidgetSettings]:

        """
        Use :data:`.http.routes.get_guild_widget_settings`.
        """

        path = [guild_id]

        def _resolve(data):
            core = _model.objects.GuildWidgetSettings(data)
            return core

        return self._request(_http.routes.get_guild_widget_settings, _resolve, path)

    ___update_guild_widget_hint = _model.protocols.GuildWidgetSettings

    def update_guild_widget(self,
                            guild_id: _model.types.Snowflake,
                            /, 
                            **fields: typing.Unpack[___update_guild_widget_hint]) -> HTTPMeddle[_model.objects.GuildWidgetSettings]:

        """
        Use :data:`.http.routes.update_guild_widget`.
        """
        
        path = [guild_id]

        json = fields

        def _resolve(data):
            core = _model.objects.GuildWidgetSettings(data)
            return core

        return self._request(_http.routes.update_guild_widget, _resolve, path, json = json)

    class ___get_guild_widget_hint(typing.TypedDict):

        pass

    def get_guild_widget(self,
                         guild_id: _model.types.Snowflake,
                         /, 
                         **fields: typing.Unpack[___get_guild_widget_hint]) -> HTTPMeddle[_model.objects.GuildWidget]:

        """
        Use :data:`.http.routes.get_guild_widget`.
        """

        path = [guild_id]

        def _resolve(data):
            core = _model.objects.GuildWidget(data)
            return core

        return self._request(_http.routes.get_guild_widget, _resolve, path)

    class ___get_guild_vanity_url_hint(typing.TypedDict):

        pass

    def get_guild_vanity_url(self,
                             guild_id: _model.types.Snowflake,
                             /, 
                             **fields: typing.Unpack[___get_guild_vanity_url_hint]) -> HTTPMeddle[_model.objects.Invite]:

        """
        Use :data:`.http.routes.get_guild_vanity_url`.
        """

        path = [guild_id]

        def _resolve(data):
            core = _model.objects.Invite(data)
            return core

        return self._request(_http.routes.get_guild_vanity_url, _resolve, path)

    class ___get_guild_widget_image_hint(typing.TypedDict):

        style: typing.Required[_model.enums.WidgetStyleOption]

    def get_guild_widget_image(self,
                               guild_id: _model.types.Snowflake,
                               /, 
                               **fields: typing.Unpack[___get_guild_widget_image_hint]) -> HTTPMeddle[typing.Any]:

        """
        Use :data:`.http.routes.get_guild_widget_image`.

        :param style:
            |dsrc| **style**
        """

        # NOTE: return type is not documented

        path = [guild_id]

        query = fields

        def _resolve(data):
            return data

        return self._request(_http.routes.get_guild_widget_image, _resolve, path, query = query)

    class ___get_guild_welcome_screen_hint(typing.TypedDict):

        pass

    def get_guild_welcome_screen(self,
                                 guild_id: _model.types.Snowflake,
                                 /, 
                                 **fields: typing.Unpack[___get_guild_welcome_screen_hint]) -> HTTPMeddle[_model.objects.WelcomeScreen]:

        """
        Use :data:`.http.routes.get_guild_welcome_screen`.
        """

        path = [guild_id]

        def _resolve(data):
            core = _model.objects.WelcomeScreen(data)
            return core

        return self._request(_http.routes.get_guild_welcome_screen, _resolve, path)

    class ___update_guild_welcome_screen_hint(typing.TypedDict):

        enabled         : typing.Optional[_model.types.Boolean]
        description     : typing.Optional[_model.types.String]
        welcome_channels: typing.Optional[list[_model.protocols.WelcomeScreenChannel]]

    def update_guild_welcome_screen(self,
                                    guild_id: _model.types.Snowflake,
                                    /, 
                                    **fields: typing.Unpack[___update_guild_welcome_screen_hint]) -> HTTPMeddle[_model.objects.WelcomeScreen]:

        """
        Use :data:`.http.routes.update_guild_welcome_screen`.

        :param enabled:
            |dsrc| **enabled**
        :param description:
            |dsrc| **description**
        :param welcome_channels:
            |dsrc| **welcome_channels**
        """

        path = [guild_id]

        json = fields

        def _resolve(data):
            core = _model.objects.WelcomeScreen(data)
            return core

        return self._request(_http.routes.update_guild_welcome_screen, _resolve, path, json = json)

    class ___get_guild_onboarding_hint(typing.TypedDict):

        pass

    def get_guild_onboarding(self,
                             guild_id: _model.types.Snowflake,
                             /, 
                             **fields: typing.Unpack[___get_guild_onboarding_hint]) -> HTTPMeddle[_model.objects.GuildOnboarding]:

        """
        Use :data:`.http.routes.get_guild_onboarding`.
        """

        path = [guild_id]

        def _resolve(data):
            core = _model.objects.GuildOnboarding(data)
            return core

        return self._request(_http.routes.get_guild_onboarding, _resolve, path)

    class ___update_self_voice_state_hint(typing.TypedDict):

        channel_id                : typing.Optional[_model.types.Snowflake]
        suppress                  : typing.Optional[_model.types.Boolean]
        request_to_speak_timestamp: typing.Optional[_model.types.ISO8601Timestamp]

    def update_self_voice_state(self,
                                guild_id: _model.types.Snowflake,
                                /, 
                                **fields: typing.Unpack[___update_self_voice_state_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.update_self_voice_state`.

        :param channel_id:
            |dsrc| **channel_id**
        :param suppress:
            |dsrc| **suppress**
        :param request_to_speak_timestamp:
            |dsrc| **request_to_speak_timestamp**
        """

        path = [guild_id]

        json = fields

        def _resolve(data):
            return None

        return self._request(_http.routes.update_self_voice_state, _resolve, path, json = json)

    class ___update_voice_state_hint(typing.TypedDict):

        channel_id: typing.Required[_model.types.Snowflake]
        suppress  : typing.Optional[_model.types.Boolean]

    def update_voice_state(self,
                           guild_id: _model.types.Snowflake,
                           user_id : _model.types.Snowflake,
                           /, 
                           **fields: typing.Unpack[___update_voice_state_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.update_voice_state`.

        :param channel_id:
            |dsrc| **channel_id**
        :param suppress:
            |dsrc| **suppress**
        :param request_to_speak_timestamp:
            |dsrc| **request_to_speak_timestamp**
        """

        path = [guild_id, user_id]

        json = fields

        def _resolve(data):
            return None

        return self._request(_http.routes.update_voice_state, _resolve, path, json = json)

    class ___get_guild_scheduled_events_hint(typing.TypedDict):

        with_user_count: typing.Optional[_model.types.Boolean]

    def get_guild_scheduled_events(self,
                                   guild_id: _model.types.Snowflake,
                                   /, 
                                   **fields: typing.Unpack[___get_guild_scheduled_events_hint]) -> HTTPMeddle[_model.objects.GuildScheduledEvent]:

        """
        Use :data:`.http.routes.get_guild_scheduled_events`.

        :param with_user_count:
            |dsrc| **with_user_count**
        """

        path = [guild_id]

        query = fields

        def _resolve(data):
            core = _model.objects.GuildScheduledEvent(data)
            return core

        return self._request(_http.routes.get_guild_scheduled_events, _resolve, path, query = query)

    class ___create_guild_scheduled_event_hint(typing.TypedDict):

        name                : typing.Required[_model.types.String]
        privacy_level       : typing.Required[_model.enums.GuildScheduledEventPrivacyLevel]
        entity_type         : typing.Required[_model.enums.GuildScheduledEventEntityType]
        scheduled_start_time: typing.Required[_model.types.ISO8601Timestamp]
        entity_metadata     : typing.Optional[_model.protocols.GuildScheduledEventEntityMetadata]
        channel_id          : typing.Optional[_model.types.Snowflake]
        scheduled_end_time  : typing.Optional[_model.types.ISO8601Timestamp]
        description         : typing.Optional[_model.types.String]
        image               : typing.Optional[_model.types.String]

    def create_guild_scheduled_event(self,
                                     guild_id: _model.types.Snowflake,
                                     /, 
                                     **fields: typing.Unpack[___create_guild_scheduled_event_hint]) -> HTTPMeddle[_model.objects.GuildScheduledEvent]:

        """
        Use :data:`.http.routes.create_guild_scheduled_event`.

        :param channel_id:
            |dsrc| **channel_id**
        :param entity_metadata:
            |dsrc| **entity_metadata**
        :param name:
            |dsrc| **name**
        :param privacy_level:
            |dsrc| **privacy_level**
        :param scheduled_start_time:
            |dsrc| **scheduled_start_time**
        :param scheduled_end_time:
            |dsrc| **scheduled_end_time**
        :param description:
            |dsrc| **description**
        :param entity_type:
            |dsrc| **entity_type**
        :param image:
            |dsrc| **image**
        """

        path = [guild_id]

        json = fields

        def _resolve(data):
            core = _model.objects.GuildScheduledEvent(data)
            return core

        return self._request(_http.routes.create_guild_scheduled_event, _resolve, path, json = json)

    class ___get_guild_scheduled_event_hint(typing.TypedDict):

        with_user_count: typing.Optional[_model.types.Boolean]

    def get_guild_scheduled_event(self,
                                  guild_id                : _model.types.Snowflake,
                                  guild_scheduled_event_id: _model.types.Snowflake,
                                  /, 
                                  **fields                : typing.Unpack[___get_guild_scheduled_event_hint]) -> HTTPMeddle[_model.objects.GuildScheduledEvent]:

        """
        Use :data:`.http.routes.get_guild_scheduled_event`.

        :param with_user_count:
            |dsrc| **with_user_count**
        """

        path = [guild_id, guild_scheduled_event_id]

        query = fields

        def _resolve(data):
            core = _model.objects.GuildScheduledEvent(data)
            return core

        return self._request(_http.routes.get_guild_scheduled_event, _resolve, path, query = query)

    class ___update_guild_scheduled_event_hint(typing.TypedDict):

        channel_id          : typing.Optional[_model.types.Snowflake]
        entity_metadata     : typing.Optional[_model.protocols.GuildScheduledEventEntityMetadata]
        name                : typing.Optional[_model.types.String]
        privacy_level       : typing.Optional[_model.enums.GuildScheduledEventPrivacyLevel]
        scheduled_start_time: typing.Optional[_model.types.ISO8601Timestamp]
        scheduled_end_time  : typing.Optional[_model.types.ISO8601Timestamp]
        description         : typing.Optional[_model.types.String]
        entity_type         : typing.Optional[_model.enums.GuildScheduledEventEntityType]
        status              : typing.Optional[_model.enums.GuildScheduledEventStatus]
        image               : typing.Optional[_model.types.String]

    def update_guild_scheduled_event(self,
                                     guild_id                : _model.types.Snowflake,
                                     guild_scheduled_event_id: _model.types.Snowflake,
                                     /, 
                                     **fields                : typing.Unpack[___update_guild_scheduled_event_hint]) -> HTTPMeddle[_model.objects.GuildScheduledEvent]:

        """
        Use :data:`.http.routes.update_guild_scheduled_event`.

        :param channel_id:
            |dsrc| **channel_id**
        :param entity_metadata:
            |dsrc| **entity_metadata**
        :param name:
            |dsrc| **name**
        :param privacy_level:
            |dsrc| **privacy_level**
        :param scheduled_start_time:
            |dsrc| **scheduled_start_time**
        :param scheduled_end_time:
            |dsrc| **scheduled_end_time**
        :param description:
            |dsrc| **description**
        :param entity_type:
            |dsrc| **entity_type**
        :param status:
            |dsrc| **status**
        :param image:
            |dsrc| **image**
        """

        path = [guild_id, guild_scheduled_event_id]

        json = fields

        def _resolve(data):
            core = _model.objects.GuildScheduledEvent(data)
            return core

        return self._request(_http.routes.update_guild_scheduled_event, _resolve, path, json = json)

    class ___delete_guild_scheduled_event_hint(typing.TypedDict):

        pass

    def delete_guild_scheduled_event(self,
                                     guild_id                : _model.types.Snowflake,
                                     guild_scheduled_event_id: _model.types.Snowflake,
                                     /, 
                                     **fields                : typing.Unpack[___delete_guild_scheduled_event_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.delete_guild_scheduled_event`.
        """

        path = [guild_id, guild_scheduled_event_id]

        def _resolve(data):
            return None

        return self._request(_http.routes.delete_guild_scheduled_event, _resolve, path)

    class ___get_guild_scheduled_event_users_hint(typing.TypedDict):

        limit      : typing.Optional[_model.types.Integer]
        with_member: typing.Optional[_model.types.Boolean]
        before     : typing.Optional[_model.types.Snowflake]
        after      : typing.Optional[_model.types.Snowflake]

    def get_guild_scheduled_event_users(self,
                                        guild_id                : _model.types.Snowflake,
                                        guild_scheduled_event_id: _model.types.Snowflake,
                                        /, 
                                        **fields                : typing.Unpack[___get_guild_scheduled_event_users_hint]) -> HTTPMeddle[None]:
        
        """
        Use :data:`.http.routes.get_guild_scheduled_event_users`
        """

        path = [guild_id, guild_scheduled_event_id]

        query = fields

        def _resolve(data):
            return None

        return self._request(_http.routes.delete_guild_scheduled_event, _resolve, path, query = query)

    class ___get_guild_template_hint(typing.TypedDict):

        pass

    def get_guild_template(self,
                           template_code: _model.types.String,
                           /, 
                           **fields     : typing.Unpack[___get_guild_template_hint]) -> HTTPMeddle[_model.objects.GuildTemplate]:

        """
        Use :data:`.http.routes.get_guild_template`.
        """

        path = [template_code]

        json = fields

        def _resolve(data):
            core = _model.objects.GuildTemplate(data)
            return core

        return self._request(_http.routes.get_guild_template, _resolve, path, json = json)

    class ___create_guild_via_guild_template_hint(typing.TypedDict):

        name: typing.Required[_model.types.String]
        icon: typing.Optional[_model.types.String]

    def create_guild_via_guild_template(self,
                                        template_code: _model.types.String,
                                        /, 
                                        **fields     : typing.Unpack[___create_guild_via_guild_template_hint]) -> HTTPMeddle[_model.objects.Guild]:

        """
        Use :data:`.http.routes.create_guild_via_guild_template`.

        :param name:
            |dsrc| **name**
        :param icon:
            |dsrc| **icon**
        """

        path = [template_code]

        json = fields

        def _resolve(data):
            core = _model.objects.Guild(data)
            return core

        return self._request(_http.routes.create_guild_via_guild_template, _resolve, path, json = json)

    class ___get_guild_templates_hint(typing.TypedDict):

        pass

    def get_guild_templates(self,
                            guild_id: _model.types.Snowflake,
                            /, 
                            **fields: typing.Unpack[___get_guild_templates_hint]) -> HTTPMeddle[list[_model.objects.GuildTemplate]]:

        """
        Use :data:`.http.routes.get_guild_templates`.
        """

        path = [guild_id]

        def _resolve(data):
            return list(map(_model.objects.GuildTemplate, data))

        return self._request(_http.routes.get_guild_templates, _resolve, path)

    class ___create_guild_template_hint(typing.TypedDict):

        name       : typing.Required[_model.types.String]
        description: typing.Optional[_model.types.String]

    def create_guild_template(self,
                              guild_id: _model.types.Snowflake,
                              /, 
                              **fields: typing.Unpack[___create_guild_template_hint]) -> HTTPMeddle[_model.objects.GuildTemplate]:

        """
        Use :data:`.http.routes.create_guild_template`.

        :param name:
            |dsrc| **name**
        :param description:
            |dsrc| **description**
        """

        path = [guild_id]

        json = fields

        def _resolve(data):
            core = _model.objects.GuildTemplate(data)
            return core

        return self._request(_http.routes.create_guild_template, _resolve, path, json = json)

    class ___sync_guild_template_hint(typing.TypedDict):

        pass

    def sync_guild_template(self,
                            guild_id     : _model.types.Snowflake,
                            template_code: _model.types.String,
                            /, 
                            **fields     : typing.Unpack[___sync_guild_template_hint]) -> HTTPMeddle[_model.objects.GuildTemplate]:

        """
        Use :data:`.http.routes.sync_guild_template`.
        """

        path = [guild_id, template_code]

        def _resolve(data):
            core = _model.objects.GuildTemplate(data)
            return core

        return self._request(_http.routes.sync_guild_template, _resolve, path)

    class ___update_guild_template_hint(typing.TypedDict):

        name       : typing.Optional[_model.types.String]
        description: typing.Optional[_model.types.String]

    def update_guild_template(self,
                              guild_id     : _model.types.Snowflake,
                              template_code: _model.types.Snowflake,
                              /, 
                              **fields     : typing.Unpack[___update_guild_template_hint]) -> HTTPMeddle[_model.objects.GuildTemplate]:

        """
        Use :data:`.http.routes.update_guild_template`.

        :param name:
            |dsrc| **name**
        :param description:
            |dsrc| **description**
        """

        path = [guild_id, template_code]

        json = fields

        def _resolve(data):
            core = _model.objects.GuildTemplate(data)
            return core

        return self._request(_http.routes.update_guild_template, _resolve, path, json = json)

    class ___delete_guild_template_hint(typing.TypedDict):

        pass

    def delete_guild_template(self,
                              guild_id     : _model.types.Snowflake,
                              template_code: _model.types.Snowflake,
                              /, 
                              **fields     : typing.Unpack[___delete_guild_template_hint]) -> HTTPMeddle[_model.objects.GuildTemplate]:

        """
        Use :data:`.http.routes.delete_guild_template`.

        :param name:
            |dsrc| **name**
        :param description:
            |dsrc| **description**
        """

        path = [guild_id, template_code]

        def _resolve(data):
            core = _model.objects.GuildTemplate(data)
            return core

        return self._request(_http.routes.delete_guild_template, _resolve, path)

    class ___get_invite_hint(typing.TypedDict):

        with_counts             : typing.Optional[_model.types.Boolean]
        with_expiration         : typing.Optional[_model.types.Boolean]
        guild_scheduled_event_id: typing.Optional[_model.types.Snowflake]

    def get_invite(self,
                   invite_code: _model.types.Snowflake,
                   /, 
                   **fields   : typing.Unpack[___get_invite_hint]) -> HTTPMeddle[_model.objects.Invite]:

        """
        Use :data:`.http.routes.get_invite`.

        :param with_counts:
            |dsrc| **with_counts**
        :param with_expiration:
            |dsrc| **with_expiration**
        :param guild_scheduled_event_id:
            |dsrc| **guild_scheduled_event_id**
        """

        path = [invite_code]

        query = fields

        def _resolve(data):
            core = _model.objects.Invite(data)
            return core

        return self._request(_http.routes.get_invite, _resolve, path, query = query)

    class ___delete_invite_hint(typing.TypedDict):

        pass

    def delete_invite(self,
                      invite_code: _model.types.Snowflake,
                      /, 
                      **fields   : typing.Unpack[___delete_invite_hint]) -> HTTPMeddle[_model.objects.Invite]:
   
        """
        Use :data:`.http.routes.delete_invite`.
        """

        path = [invite_code]

        def _resolve(data):
            core = _model.objects.Invite(data)
            return core

        return self._request(_http.routes.delete_invite, _resolve, path)

    class ___create_stage_instance_hint(typing.TypedDict):

        channel_id             : typing.Required[_model.types.Snowflake]
        topic                  : typing.Required[_model.types.String]
        privacy_level          : typing.Optional[_model.types.Integer]
        send_start_notification: typing.Optional[_model.types.Boolean]

    def create_stage_instance(self,
                              /, 
                              **fields: typing.Unpack[___create_stage_instance_hint]) -> HTTPMeddle[_model.objects.StageInstance]:

        """
        Use :data:`.http.routes.create_stage_instance`.
        
        :param channel_id:
            |dsrc| **channel_id**
        :param topic:
            |dsrc| **topic**
        :param privacy_level:
            |dsrc| **privacy_level**
        :param send_start_notification:
            |dsrc| **send_start_notification**
        """

        path = []

        json = fields

        def _resolve(data):
            core = _model.objects.StageInstance(data)
            return core

        return self._request(_http.routes.create_stage_instance, _resolve, path, json = json)

    class ___get_stage_instance_hint(typing.TypedDict):

        pass

    def get_stage_instance(self,
                           channel_id: _model.types.Snowflake,
                           /, 
                           **fields  : typing.Unpack[___get_stage_instance_hint]) -> HTTPMeddle[_model.objects.StageInstance]:

        """
        Use :data:`.http.routes.get_stage_instance`.
        """

        path = [channel_id]

        def _resolve(data):
            core = _model.objects.StageInstance(data)
            return core

        return self._request(_http.routes.get_stage_instance, _resolve, path)

    class ___update_stage_instance_hint(typing.TypedDict):

        topic        : typing.Optional[_model.types.String]
        privacy_level: typing.Optional[_model.types.Integer]

    def update_stage_instance(self,
                              channel_id: _model.types.Snowflake,
                              /, 
                              **fields  : typing.Unpack[___update_stage_instance_hint]) -> HTTPMeddle[_model.objects.StageInstance]:

        """
        Use :data:`.http.routes.update_stage_instance`.

        :param topic:
            |dsrc| **topic**
        :param privacy_level:
            |dsrc| **privacy_level**
        """

        path = [channel_id]

        json = fields

        def _resolve(data):
            core = _model.objects.StageInstance(data)
            return core

        return self._request(_http.routes.update_stage_instance, _resolve, path, json = json)

    class ___delete_stage_instance_hint(typing.TypedDict):

        pass

    def delete_stage_instance(self,
                              channel_id: _model.types.Snowflake,
                              /, 
                              **fields  : typing.Unpack[___delete_stage_instance_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.delete_stage_instance`.

        :param topic:
            |dsrc| **topic**
        :param privacy_level:
            |dsrc| **privacy_level**
        """

        path = [channel_id]

        json = fields

        def _resolve(data):
            return None

        return self._request(_http.routes.delete_stage_instance, _resolve, path, json = json)

    class ___get_sticker_hint(typing.TypedDict):

        pass

    def get_sticker(self,
                    sticker_id: _model.types.Snowflake,
                    /, 
                    **fields  : typing.Unpack[___get_sticker_hint]) -> HTTPMeddle[_model.objects.Sticker]:

        """
        Use :data:`.http.routes.get_sticker`.
        """

        path = [sticker_id]

        def _resolve(data):
            core = _model.objects.Sticker(data)
            return core

        return self._request(_http.routes.get_sticker, _resolve, path)

    class ___get_sticker_packs_hint(typing.TypedDict):

        pass

    def get_sticker_packs(self,
                          guild_id: _model.types.Snowflake,
                          /, 
                          **fields: typing.Unpack[___get_sticker_packs_hint]) -> HTTPMeddle[list[_model.objects.StickerPack]]:

        """
        Use :data:`.http.routes.get_sticker_packs`.
        """

        path = [guild_id]

        def _resolve(data):
            return list(map(_model.objects.StickerPack, data['sticker_packs']))

        return self._request(_http.routes.get_sticker_packs, _resolve, path)

    class ___get_guild_stickers_hint(typing.TypedDict):

        pass

    def get_guild_stickers(self,
                           guild_id: _model.types.Snowflake,
                           /, 
                           **fields: typing.Unpack[___get_guild_stickers_hint]) -> HTTPMeddle[list[_model.objects.Sticker]]:

        """
        Use :data:`.http.routes.get_guild_stickers`.
        """

        path = [guild_id]

        def _resolve(data):
            return list(map(_model.objects.Sticker, data))

        return self._request(_http.routes.get_guild_stickers, _resolve, path)

    class ___get_guild_sticker_hint(typing.TypedDict):

        pass

    def get_guild_sticker(self,
                          guild_id  : _model.types.Snowflake,
                          sticker_id: _model.types.Snowflake,
                          /, 
                          **fields  : typing.Unpack[___get_guild_sticker_hint]) -> HTTPMeddle[_model.objects.Sticker]:

        """
        Use :data:`.http.routes.get_guild_sticker`.
        """

        path = [guild_id, sticker_id]

        def _resolve(data):
            core = _model.objects.Sticker(data)
            return core

        return self._request(_http.routes.get_guild_sticker, _resolve, path)

    class ___create_guild_sticker_hint(typing.TypedDict):

        name       : typing.Required[_model.types.String]
        description: typing.Required[_model.types.String]
        tags       : typing.Required[_model.types.String]
        file       : typing.Required[list[io.BytesIO]]

    def create_guild_sticker(self,
                             guild_id: _model.types.Snowflake,
                             /, 
                             **fields: typing.Unpack[___create_guild_sticker_hint]) -> HTTPMeddle[_model.objects.Sticker]:

        """
        Use :data:`.http.routes.create_guild_sticker`.

        :param name:
            |dsrc| **name**
        :param description:
            |dsrc| **description**
        :param tags:
            |dsrc| **tags**
        :param file:
            |dsrc| **file**
        """

        path = [guild_id]

        _data = fields

        def _resolve(data):
            core = _model.objects.Sticker(data)
            return core

        return self._request(_http.routes.create_guild_sticker, _resolve, path, data = _data)

    class ___update_guild_sticker_hint(typing.TypedDict):

        name       : typing.Optional[_model.types.String]
        description: typing.Optional[_model.types.String]
        tags       : typing.Optional[_model.types.String]

    def update_guild_sticker(self,
                             guild_id  : _model.types.Snowflake,
                             sticker_id: _model.types.Snowflake,
                             /, 
                             **fields  : typing.Unpack[___update_guild_sticker_hint]) -> HTTPMeddle[_model.objects.Sticker]:

        """
        Use :data:`.http.routes.update_guild_sticker`.

        :param name:
            |dsrc| **name**
        :param description:
            |dsrc| **description**
        :param tags:
            |dsrc| **tags**
        """

        path = [guild_id, sticker_id]

        json = fields

        def _resolve(data):
            core = _model.objects.Sticker(data)
            return core

        return self._request(_http.routes.update_guild_sticker, _resolve, path, json = json)

    class ___delete_guild_sticker_hint(typing.TypedDict):

        pass

    def delete_guild_sticker(self,
                             guild_id  : _model.types.Snowflake,
                             sticker_id: _model.types.Snowflake,
                             /, 
                             **fields  : typing.Unpack[___delete_guild_sticker_hint]) -> HTTPMeddle[_model.objects.Sticker]:

        """
        Use :data:`.http.routes.delete_guild_sticker`.

        :param name:
            |dsrc| **name**
        :param description:
            |dsrc| **description**
        :param tags:
            |dsrc| **tags**
        """

        path = [guild_id, sticker_id]

        def _resolve(data):
            core = _model.objects.Sticker(data)
            return core

        return self._request(_http.routes.delete_guild_sticker, _resolve, path)

    class ___get_self_user_hint(typing.TypedDict):

        pass

    def get_self_user(self, 
                      /, 
                      **fields: typing.Unpack[___get_self_user_hint]) -> HTTPMeddle[_model.objects.User]:

        """
        Use :data:`.http.routes.get_self_user`.
        """

        path = []

        def _resolve(data):
            core = _model.objects.User(data)
            return core

        return self._request(_http.routes.get_self_user, _resolve, path)

    class ___get_user_hint(typing.TypedDict):

        pass

    def get_user(self,
                 user_id : _model.types.Snowflake,
                 /, 
                 **fields: typing.Unpack[___get_user_hint]) -> HTTPMeddle[_model.objects.User]:

        """
        Use :data:`.http.routes.get_user`.
        """

        path = [user_id]

        def _resolve(data):
            core = _model.objects.User(data)
            return core

        return self._request(_http.routes.get_user, _resolve, path)

    class ___update_self_user_hint(typing.TypedDict):

        username: typing.Optional[_model.types.String]
        avatar  : typing.Optional[_model.types.String]

    def update_self_user(self,
                         /, 
                         **fields: typing.Unpack[___update_self_user_hint]) -> HTTPMeddle[_model.objects.User]:

        """
        Use :data:`.http.routes.update_self_user`.

        :param username:
            |dsrc| **username**
        :param avatar:
            |dsrc| **avatar**
        """

        path = []

        json = fields

        def _resolve(data):
            core = _model.objects.User(data)
            return core

        return self._request(_http.routes.update_self_user, _resolve, path, json = json)

    class ___get_self_guilds_hint(typing.TypedDict):

        before: typing.Required[_model.types.Snowflake]
        after : typing.Required[_model.types.Snowflake]
        limit : typing.Required[_model.types.Integer]

    def get_self_guilds(self,
                        /, 
                        **fields: typing.Unpack[___get_self_guilds_hint]) -> HTTPMeddle[list[_model.objects.Guild]]:

        """
        Use :data:`.http.routes.get_self_guilds`.

        :param before:
            |dsrc| **before**
        :param after:
            |dsrc| **after**
        :param limit:
            |dsrc| **limit**
        """

        path = []

        query = fields

        def _resolve(data):
            return list(map(_model.objects.Guild, data))

        return self._request(_http.routes.get_self_guilds, _resolve, path, query = query)

    class ___get_self_guild_member_hint(typing.TypedDict):

        pass

    def get_self_guild_member(self,
                              guild_id: _model.types.Snowflake,
                              /, 
                              **fields: typing.Unpack[___get_self_guild_member_hint]) -> HTTPMeddle[_model.objects.GuildMember]:

        """
        Use :data:`.http.routes.get_self_guild_member`.
        """

        path = [guild_id]

        def _resolve(data):
            core = _model.objects.GuildMember(data)
            return core

        return self._request(_http.routes.get_self_guild_member, _resolve, path)

    class ___delete_self_guild_member_hint(typing.TypedDict):

        pass

    def delete_self_guild_member(self,
                                 guild_id: _model.types.Snowflake,
                                 /, 
                                 **fields: typing.Unpack[___delete_self_guild_member_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.delete_self_guild_member`.
        """

        path = [guild_id]

        def _resolve(data):
            return None

        return self._request(_http.routes.delete_self_guild_member, _resolve, path)

    class ___create_self_channel_hint(typing.TypedDict):

        recipient_id : typing.Required[_model.types.Snowflake]

    @typing.overload
    def create_self_channel(self,
                            /, 
                            **fields: typing.Unpack[___create_self_channel_hint]) -> HTTPMeddle[_model.objects.Channel]:

        ...

    class ___create_self_channel_hint(typing.TypedDict):

        access_tokens: typing.Required[list[_model.types.String]]
        nicks        : typing.Optional[dict[_model.types.Snowflake, _model.types.String]]

    @typing.overload
    def create_self_channel(self,
                            /, 
                            **fields: typing.Unpack[___create_self_channel_hint]) -> HTTPMeddle[_model.objects.Channel]:

        ...

    def create_self_channel(self,
                            /, 
                            **fields):

        """
        Use :data:`.http.routes.create_self_channel`.

        :param recipient_id:
            |dsrc| **recipient_id**
        """

        path = []

        json = fields

        def _resolve(data):
            core = _model.objects.Channel(data)
            return core

        return self._request(_http.routes.create_self_channel, _resolve, path, json = json)

    class ___get_self_connections_hint(typing.TypedDict):

        pass

    def get_self_connections(self, 
                             /, 
                             **fields: typing.Unpack[___get_self_connections_hint]) -> HTTPMeddle[list[_model.objects.Connection]]:

        """
        Use :data:`.http.routes.get_self_connections`.
        """

        path = []

        def _resolve(data):
            return list(map(_model.objects.Connection, data))

        return self._request(_http.routes.get_self_connections, _resolve, path)

    class ___get_self_application_role_connection_hint(typing.TypedDict):

        pass

    def get_self_application_role_connection(self,
                                             application_id: _model.types.Snowflake,
                                             /, 
                                             **fields      : typing.Unpack[___get_self_application_role_connection_hint]) -> HTTPMeddle[_model.objects.ApplicationRoleConnection]:

        """
        Use :data:`.http.routes.get_self_application_role_connection`.
        """

        path = [application_id]

        def _resolve(data):
            core = _model.objects.ApplicationRoleConnection(data)
            return core

        return self._request(_http.routes.get_self_application_role_connection, _resolve, path)

    class ___update_self_application_role_connection_hint(typing.TypedDict):

        platform_name    : typing.Optional[_model.types.String]
        platform_username: typing.Optional[_model.types.String]
        metadata         : typing.Optional[_model.protocols.ApplicationRoleConnectionMetadata]

    def update_self_application_role_connection(self,
                                                application_id: _model.types.Snowflake,
                                                /, 
                                                **fields      : typing.Unpack[___update_self_application_role_connection_hint]) -> HTTPMeddle[_model.objects.ApplicationRoleConnection]:

        """
        Use :data:`.http.routes.update_self_application_role_connection`.
        """

        path = [application_id]

        json = fields

        def _resolve(data):
            core = _model.objects.ApplicationRoleConnection(data)
            return core

        return self._request(_http.routes.update_self_application_role_connection, _resolve, path, json = json)

    class ___get_voice_regions_hint(typing.TypedDict):

        pass

    def get_voice_regions(self, 
                          /, 
                          **fields: typing.Unpack[___get_voice_regions_hint]) -> HTTPMeddle[list[_model.objects.VoiceRegion]]:

        """
        Use :data:`.http.routes.get_voice_regions`.
        """

        path = []

        def _resolve(data):
            return list(map(_model.objects.VoiceRegion, data))

        return self._request(_http.routes.get_voice_regions, _resolve, path)

    class ___create_webhook_hint(typing.TypedDict):

        name  : typing.Required[_model.types.String]
        avatar: typing.Optional[_model.types.String]

    def create_webhook(self,
                       channel_id: _model.types.Snowflake,
                       /, 
                       **fields  : typing.Unpack[___create_webhook_hint]) -> HTTPMeddle[_model.objects.Webhook]:

        """
        Use :data:`.http.routes.create_webhook`.

        :param name:
            |dsrc| **name**
        :param avatar:
            |dsrc| **avatar**
        """

        path = [channel_id]

        json = fields

        def _resolve(data):
            core = _model.objects.Webhook(data)
            return core

        return self._request(_http.routes.create_webhook, _resolve, path, json = json)

    class ___get_channel_webhooks_hint(typing.TypedDict):

        pass

    def get_channel_webhooks(self,
                             channel_id: _model.types.Snowflake,
                             /, 
                             **fields  : typing.Unpack[___get_channel_webhooks_hint]) -> HTTPMeddle[list[_model.objects.Webhook]]:

        """
        Use :data:`.http.routes.get_channel_webhooks`.
        """

        path = [channel_id]

        def _resolve(data):
            return list(map(_model.objects.Webhook, data))

        return self._request(_http.routes.get_channel_webhooks, _resolve, path)

    class ___get_guild_webhooks_hint(typing.TypedDict):

        pass

    def get_guild_webhooks(self,
                           guild_id: _model.types.Snowflake,
                           /, 
                           **fields: typing.Unpack[___get_guild_webhooks_hint]) -> HTTPMeddle[list[_model.objects.Webhook]]:

        """
        Use :data:`.http.routes.get_guild_webhooks`.
        """

        path = [guild_id]

        def _resolve(data):
            return list(map(_model.objects.Webhook, data))

        return self._request(_http.routes.get_guild_webhooks, _resolve, path)

    class ___get_webhook_hint(typing.TypedDict):

        pass

    def get_webhook(self,
                    webhook_id: _model.types.Snowflake,
                    /, 
                    **fields  : typing.Unpack[___get_webhook_hint]) -> HTTPMeddle[_model.objects.Webhook]:

        """
        Use :data:`.http.routes.get_webhook`.
        """

        path = [webhook_id]

        def _resolve(data):
            core = _model.objects.Webhook(data)
            return core

        return self._request(_http.routes.get_webhook, _resolve, path)

    class ___get_webhook_via_token_hint(typing.TypedDict):

        pass

    def get_webhook_via_token(self,
                              webhook_id   : _model.types.Snowflake,
                              webhook_token: _model.types.Snowflake,
                              /, 
                              **fields     : typing.Unpack[___get_webhook_via_token_hint]) -> HTTPMeddle[_model.objects.Webhook]:

        """
        Use :data:`.http.routes.get_webhook_via_token`.
        """

        path = [webhook_id, webhook_token]

        def _resolve(data):
            core = _model.objects.Webhook(data)
            return core

        return self._request(_http.routes.get_webhook_via_token, _resolve, path)

    class ___update_webhook_hint(typing.TypedDict):

        name      : typing.Optional[_model.types.String]
        avatar    : typing.Optional[_model.types.String]
        channel_id: typing.Optional[_model.types.Snowflake]

    def update_webhook(self,
                       webhook_id: _model.types.Snowflake,
                       /, 
                       **fields  : typing.Unpack[___update_webhook_hint]) -> HTTPMeddle[_model.objects.Webhook]:

        """
        Use :data:`.http.routes.update_webhook`.

        :param name:
            |dsrc| **name**
        :param avatar:
            |dsrc| **avatar**
        :param channel_id:
            |dsrc| **channel_id**
        """

        path = [webhook_id]

        json = fields

        def _resolve(data):
            core = _model.objects.Webhook(data)
            return core

        return self._request(_http.routes.update_webhook, _resolve, path, json = json)

    class ___update_webhook_via_token_hint(typing.TypedDict):

        name      : typing.Optional[_model.types.String]
        avatar    : typing.Optional[_model.types.String]
        channel_id: typing.Optional[_model.types.Snowflake]

    def update_webhook_via_token(self,
                                 webhook_id   : _model.types.Snowflake,
                                 webhook_token: _model.types.Snowflake,
                                 /, 
                                 **fields     : typing.Unpack[___update_webhook_via_token_hint]) -> HTTPMeddle[_model.objects.Webhook]:

        """
        Use :data:`.http.routes.update_webhook_via_token`.
        """

        path = [webhook_id, webhook_token]

        json = fields

        def _resolve(data):
            core = _model.objects.Webhook(data)
            return core

        return self._request(_http.routes.update_webhook_via_token, _resolve, path, json = json)

    class ___delete_webhook_hint(typing.TypedDict):

        pass

    def delete_webhook(self,
                       webhook_id: _model.types.Snowflake,
                       /, 
                       **fields  : typing.Unpack[___delete_webhook_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.delete_webhook`.
        """

        path = [webhook_id]

        def _resolve(data):
            return None

        return self._request(_http.routes.delete_webhook, _resolve, path)

    class ___delete_webhook_via_token_hint(typing.TypedDict):

        pass

    def delete_webhook_via_token(self,
                                 webhook_id   : _model.types.Snowflake,
                                 webhook_token: _model.types.Snowflake,
                                 /, 
                                 **fields     : typing.Unpack[___delete_webhook_via_token_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.delete_webhook_via_token`.
        """

        path = [webhook_id, webhook_token]

        def _resolve(data):
            return None

        return self._request(_http.routes.delete_webhook_via_token, _resolve, path)
    
    class ___create_webhook_message_hint(typing.TypedDict):

        wait            : typing.Optional[_model.types.Boolean]
        thread_id       : typing.Optional[_model.types.Snowflake]
        content         : typing.Optional[_model.types.String]
        username        : typing.Optional[_model.types.String]
        avatar_url      : typing.Optional[_model.types.String]
        tts             : typing.Optional[_model.types.Boolean]
        embeds          : typing.Optional[list[_model.protocols.Embed]]
        allowed_mentions: typing.Optional[_model.protocols.AllowedMentions]
        components      : typing.Optional[list[_model.protocols.MessageActionRowComponent | _model.protocols.MessageButtonComponent | _model.protocols.MessageTextInputComponent | _model.protocols.MessageSelectMenuComponent]]
        files           : typing.Optional[list[io.BytesIO]]
        attachments     : typing.Optional[list[_model.protocols.Attachment]]
        thread_name     : typing.Optional[_model.types.String]

    def create_webhook_message(self,
                               webhook_id   : _model.types.Snowflake,
                               webhook_token: _model.types.Snowflake,
                               /,
                               **fields     : typing.Unpack[___create_webhook_message_hint]) -> HTTPMeddle[_model.objects.Message | None]:
        
        """
        Use :data:`.http.routes.create_webhook_message`.

        :param wait:
            |dsrc| **wait**
        :param thread_id:
            |dsrc| **thread_id**
        :param content:
            |dsrc| **content**
        :param username:
            |dsrc| **username**
        :param avatar_url:
            |dsrc| **avatar_url**
        :param tts:
            |dsrc| **tts**
        :param components:
            |dsrc| **components**
        :param files:
            |dsrc| **files[n]**
        :param flags:
            |dsrc| **flags**
        :param thread_name:
            |dsrc| **thread_name**
        :param embeds:
            |dsrc| **embeds**
        :param allowed_mentions:
            |dsrc| **allowed_mentions**
        :param attachments:
            |dsrc| **attachments**
        """

        path = [webhook_id, webhook_token]

        files = fields.pop('files', None)

        query = _helpers.yank_dict(fields, ('wait', 'thread_id'))

        json = fields

        def _resolve(data):
            if data is None:
                return None
            return _model.objects.Message(data)

        return self._request(_http.routes.create_webhook_message, _resolve, path, query = query, json = json, files = files)
    
    class ___get_webhook_message_hint(typing.TypedDict):

        thread_id: typing.Optional[_model.types.Snowflake]

    def get_webhook_message(self,
                            webhook_id   : _model.types.Snowflake,
                            webhook_token: _model.types.Snowflake,
                            message_id   : _model.types.Snowflake,
                            /, 
                            **fields     : typing.Unpack[___get_webhook_message_hint]) -> HTTPMeddle[_model.objects.Message]:

        """
        Use :data:`.http.routes.get_webhook_message`.

        :param thread_id:
            |dsrc| **thread_id**
        """

        path = [webhook_id, webhook_token, message_id]

        query = fields

        def _resolve(data):
            core = _model.objects.Message(data)
            return core

        return self._request(_http.routes.get_webhook_message, _resolve, path, query = query)
    
    class ___update_webhook_message_hint(typing.TypedDict):

        thread_id       : typing.Optional[_model.types.Snowflake | None]
        content         : typing.Optional[_model.types.String | None]
        allowed_mentions: typing.Optional[_model.protocols.AllowedMentions | None]
        components      : typing.Optional[list[_model.protocols.MessageActionRowComponent | _model.protocols.MessageButtonComponent | _model.protocols.MessageTextInputComponent | _model.protocols.MessageSelectMenuComponent] | None]
        files           : typing.Optional[list[io.BytesIO] | None]
        attachments     : typing.Optional[list[_model.protocols.Attachment] | None]

    def update_webhook_message(self,
                               webhook_id   : _model.types.Snowflake,
                               webhook_token: _model.types.Snowflake,
                               /,
                               **fields     : typing.Unpack[___update_webhook_message_hint]) -> HTTPMeddle[_model.objects.Message | None]:
        
        """
        Use :data:`.http.routes.update_webhook_message`.

        :param thread_id:
            |dsrc| **thread_id**
        :param content:
            |dsrc| **content**
        :param components:
            |dsrc| **components**
        :param files:
            |dsrc| **files[n]**
        :param embeds:
            |dsrc| **embeds**
        :param allowed_mentions:
            |dsrc| **allowed_mentions**
        :param attachments:
            |dsrc| **attachments**
        """

        path = [webhook_id, webhook_token]

        files = fields.pop('files', None)

        query = _helpers.yank_dict(fields, ('thread_id',))

        json = fields

        def _resolve(data):
            core = _model.objects.Message(data)
            return core

        return self._request(_http.routes.update_webhook_message, _resolve, path, query = query, json = json, files = files)

    class ___delete_webhook_message_hint(typing.TypedDict):

        thread_id: typing.Optional[_model.types.Snowflake]

    def delete_webhook_message(self,
                               webhook_id   : _model.types.Snowflake,
                               webhook_token: _model.types.Snowflake,
                               message_id   : _model.types.Snowflake,
                               /, 
                               **fields     : typing.Unpack[___delete_webhook_message_hint]) -> HTTPMeddle[None]:

        """
        Use :data:`.http.routes.delete_webhook_message`.

        :param thread_id:
            |dsrc| **thread_id**
        """

        path = [webhook_id, webhook_token, message_id]

        query = fields

        def _resolve(data):
            core = _model.objects.Message(data)
            return core

        return self._request(_http.routes.delete_webhook_message, _resolve, path, query = query)

    # class ___get_gateway_hint(typing.TypedDict):

    #     pass

    # def get_gateway(self, 
    #                 /, 
    #                 **fields: typing.Unpack[___get_gateway_hint]) -> HTTPMeddle[typing.Any]:

    #     """
    #     Use :data:`.http.routes.get_gateway`.
    #     """

    #     path = []

    #     def _resolve(data):
    #         return data

    #     return self._request(_http.routes.get_gateway, _resolve, path)

    # class ___get_gateway_bot_hint(typing.TypedDict):

    #     pass

    # def get_gateway_bot(self, 
    #                     /, 
    #                     **fields: typing.Unpack[___get_gateway_bot_hint]) -> HTTPMeddle[typing.Any]:

    #     """
    #     Use :data:`.http.routes.get_gateway_bot`.
    #     """

    #     path = []

    #     def _resolve(data):
    #         return data

    #     return self._request(_http.routes.get_gateway_bot, _resolve, path)

    class ___get_self_application_information_hint(typing.TypedDict):

        pass

    def get_self_application_information(self, 
                                         /, 
                                         **fields: typing.Unpack[___get_self_application_information_hint]) -> HTTPMeddle[_model.objects.Application]:

        """
        Use :data:`.http.routes.get_self_application_information`.
        """

        path = []

        def _resolve(data):
            core = _model.objects.Application(data)
            return core

        return self._request(_http.routes.get_self_application_information, _resolve, path)
    
    class ___get_self_authorization_information_hint(typing.TypedDict):

        pass

    def get_self_authorization_information(self, 
                                           /, 
                                           **fields: typing.Unpack[___get_self_authorization_information_hint]) -> HTTPMeddle[_model.responses.get_self_authorization_information]:

        """
        Use :data:`.http.routes.get_self_authorization_information`.
        """

        path = []

        def _resolve(data):
            data_application = data['application']
            core_application = _model.objects.Application(data_application)
            data_scopes = data['scopes']
            core_scopes = list(map(_model.types.String, data_scopes))
            data_expires = data['expires']
            core_expires = _model.types.ISO8601Timestamp(data_expires)
            data_user = data.get('user')
            core_user = None if data_user is None else _model.objects.User(data_user)
            core = _model.responses.get_self_authorization_information(core_application, core_scopes, core_expires, core_user)
            return core

        return self._request(_http.routes.get_self_authorization_information, _resolve, path)
    
    class ___get_skus_hint(typing.TypedDict):

        pass

    def get_skus(self,
                 application_id: _model.types.Snowflake,
                 /,
                 **fields: ___get_skus_hint):
        
        """
        Use :data:`.http.routes.get_skus`.
        """

        path = [application_id]

        def _resolve(data):
            return list(map(_model.objects.SKU, data))
        
        return self._request(_http.routes.get_skus, _resolve, path)
        
    class ___get_entitlements_hint(typing.TypedDict):

        user_id      : typing.Optional[_model.types.Snowflake]
        sku_ids      : typing.Optional[list[_model.types.String]]
        before       : typing.Optional[_model.types.Snowflake]
        after        : typing.Optional[_model.types.Snowflake]
        limit        : typing.Optional[_model.types.Integer]
        guild_id     : typing.Optional[_model.types.Snowflake]
        exclude_ended: typing.Optional[_model.types.Boolean]

    def get_entitlements(self,
                         application_id: _model.types.Snowflake,
                         /,
                         **fields: ___get_entitlements_hint):
        
        """
        Use :data:`.http.routes.get_entitlements`.
        """

        path = [application_id]

        try:
            sku_ids = fields['sku_ids']
        except KeyError:
            pass
        else:
            fields['sku_ids'] = ','.join(sku_ids)

        query = fields

        def _resolve(data):
            return list(map(_model.objects.Entitlement, data))

        return self._request(_http.routes.get_entitlements, _resolve, path, query = query)
    
    class ___create_entitlement_hint(typing.TypedDict):

        sku_id    : _model.types.String
        owner_id  : _model.types.Snowflake
        owner_type: _model.enums.EntitlementOwnerType

    def create_entitlement(self,
                           application_id: _model.types.Snowflake,
                           /,
                           **fields: ___create_entitlement_hint):
        
        """
        Use :data:`.http.routes.create_entitlement`.
        """

        path = [application_id]

        json = fields

        def _resolve(data):
            return _model.objects.Entitlement(data)

        return self._request(_http.routes.create_entitlement, _resolve, path, json = json)

    class ___delete_entitlement_hint(typing.TypedDict):

        pass

    def delete_entitlement(self,
                           application_id: _model.types.Snowflake,
                           entitlement_id: _model.types.Snowflake,
                           /,
                           **fields: ___delete_entitlement_hint):
        
        """
        Use :data:`.http.routes.delete_entitlement`.
        """

        path = [application_id, entitlement_id]

        def _resolve(data):
            return None

        return self._request(_http.routes.delete_entitlement, _resolve, path)

    def _create_sentinel(self, Event, check, timeout = None):

        event = asyncio.Event()

        value = NotImplemented

        async def callback(*args, **kwargs):
            if not isinstance(args[0], Event):
                return
            if check and not await check(*args, **kwargs):
                return
            nonlocal value
            value = args[0]
            event.set()

        self._callbacks.append(callback)

        async def sentinel():
            try:
                async with asyncio.timeout(timeout):
                    await event.wait()
            finally:
                self._callbacks.remove(callback)
            return value
        
        task = asyncio.create_task(sentinel())
        
        return task
    
    def wait(self, Event, check = None, /, timeout: int = None) -> asyncio.Task[typing.Any]:

        """
        Setup waiting for a specific event.

        :param Event:
            Any class of the first argument of :paramref:`~.Client.callback`.
        :param check:
            Called the same way as :paramref:`~.Client.callback`. Should return :class:`bool` indicating whether to set the event.
        :param timeout:
            Maximum amount of seconds to wait before setting the event.

        :return:
            The inputs to the matched event.

        .. code-block:: py

            def check(event):
                return event.message.author.id == client.cache.user.id and event.message.content == 'pass'

            task = asyncio.create_task(aiocord.events.CreateMessage, check, timeout = 10)

            await client.create_message(channel_id, content = 'pass')

            event = await task # the corresponding CreateMessage event
        """
        
        return self._create_sentinel(Event, check, timeout)
    
    async def _callback_sentinel(self, sentinel, *args):

        if not (check := sentinel.check) is None:
            if not await check(*args):
                return
        
        sentinel.event.set()

    def _dispatch(self, core_event, copy_event = None, /):

        args = [core_event]

        if not copy_event is None:
            args.append(copy_event)

        tasks = []
        for callback in self._callbacks:
            coro = callback(*args)
            task = asyncio.create_task(coro)
            tasks.append(task)

    async def _handle_gateway_ready(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#ready

        session_id = data['session_id']
        resume_uri = data['resume_gateway_url']

        shard.inform_session(session_id, resume_uri)

        vessel.update(self._cache, data)

        core_event = _events.Ready()

        self._dispatch(core_event)

    async def _handle_gateway_update_application_command_permissions(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#application-command-permissions-update

        data_guild = {}
        data_guild['id'] = data['guild_id']

        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)

        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_application_command_permissions = data

        core_application_command_permissions = _model.objects.GuildApplicationCommandPermission(data_application_command_permissions)

        core_event = _events.UpdateApplicationCommandPermission(
            guild                           = core_guild,
            application_command_permissions = core_application_command_permissions
        )

        self._dispatch(core_event)

    async def _handle_gateway_create_auto_moderation_rule(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#auto-moderation-rule-create

        data_guild = {}
        data_guild['id'] = data['guild_id']

        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)

        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_auto_moderation_rule = data

        core_auto_moderation_rule = _model.objects.AutoModerationRule(data_auto_moderation_rule)

        core_event = _events.CreateAutoModerationRule(
            guild                = core_guild,
            auto_moderation_rule = core_auto_moderation_rule
        )

        self._dispatch(core_event)

    async def _handle_gateway_update_auto_moderation_rule(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#auto-moderation-rule-update

        data_guild = {}
        data_guild['id'] = data['guild_id']

        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)

        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_auto_moderation_rule = data

        core_auto_moderation_rule = _model.objects.AutoModerationRule(data_auto_moderation_rule)

        core_event = _events.UpdateAutoModerationRule(
            guild                = core_guild,
            auto_moderation_rule = core_auto_moderation_rule
        )

        self._dispatch(core_event)

    async def _handle_gateway_delete_auto_moderation_rule(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#auto-moderation-rule-delete

        data_guild = {}
        data_guild['id'] = data['guild_id']

        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)

        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)


        data_auto_moderation_rule = data

        core_auto_moderation_rule = _model.objects.AutoModerationRule(data_auto_moderation_rule)

        core_event = _events.DeleteAutoModerationRule(
            guild                = core_guild,
            auto_moderation_rule = core_auto_moderation_rule
        )

        self._dispatch(core_event)

    async def _handle_gateway_execute_auto_moderation_action(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#auto-moderation-action-execution

        data_guild = {}
        data_guild['id'] = data['guild_id']

        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)

        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_auto_moderation_action = data['action']
        core_auto_moderation_action = _model.objects.AutoModerationAction(data_auto_moderation_action)

        data_auto_moderation_rule = {}
        data_auto_moderation_rule['id'] = data['rule_id']
        data_auto_moderation_rule['trigger_type'] = data['rule_trigger_type']
        core_auto_moderation_rule = _model.objects.AutoModerationRule(data_auto_moderation_rule)
        
        data_user = {}
        data_user['id'] = data['user']

        core_user_id = vessel.keyify(_model.objects.User, data_user)

        try:
            core_guild_member = core_guild.members[core_user_id]
        except KeyError:
            core_user = _model.objects.User(data_user)
        else:
            core_user = core_guild_member.user

        data_channel = {}
        data_channel['id'] = data['channell_id']

        core_channel_id = vessel.keyify(_model.objects.Channel, data_channel)

        try:
            core_channel = core_guild.channels[core_channel_id]
        except KeyError:
            core_channel = _model.objects.Channel(data_channel)

        data_source_message = {}
        
        try:
            data_source_message['id'] = data['message_id']
        except KeyError:
            pass

        try:
            data_source_message['content'] = data['content']
        except KeyError:
            pass

        core_source_message = _model.objects.Message(data_source_message)

        data_system_message = {}
        
        try:
            data_system_message['id'] = data['alert_system_message_id']
        except KeyError:
            pass

        core_system_message = _model.objects.Message(data_system_message)

        data_matched_keyword = data['matched_keyword']
        core_matched_keyword = _model.types.String(data_matched_keyword)

        try:
            data_matched_content = data['matched_content']
        except KeyError:
            core_matched_content = _model.missing
        else:
            core_matched_content = _model.types.String(data_matched_content)

        core_event = _events.ExecuteAutoModerationRule(
            guild                  = core_guild,
            auto_moderation_action = core_auto_moderation_action,
            auto_moderation_rule   = core_auto_moderation_rule,
            user                   = core_user,
            channel                = core_channel,
            source_message         = core_source_message,
            system_message         = core_system_message,
            matched_keyword        = core_matched_keyword,
            matched_content        = core_matched_content
        )

        self._dispatch(core_event)

    async def _handle_gateway_create_channel(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#channel-create

        data_channel = data

        data_guild = {}
        try:
            data_guild['id'] = data['guild_id']
        except KeyError:
            core_guild_id = _model.missing
        else:
            core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)

        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)
            core_channel = _model.objects.Channel(data_channel)
        else:
            core_channel = vessel.add(core_guild.channels, data_channel)
        
        core_event = _events.CreateChannel(
            guild   = core_guild,
            channel = core_channel
        )

        self._dispatch(core_event)

    async def _handle_gateway_update_channel(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#channel-update

        data_channel = data

        core_channel_id = vessel.keyify(_model.objects.Channel, data_channel)

        data_guild = {}
        try:
            data_guild['id'] = data['guild_id']
        except KeyError:
            core_guild_id = _model.missing
        else:
            core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)

        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        try:
            core_channel = core_guild.channels[core_channel_id]
        except KeyError:
            copy_channel = None
            core_channel = _model.objects.Channel(data_channel)
        else:
            copy_channel = copy.copy(core_channel)
            core_channel = vessel.update(core_channel, data_channel)

        copy_event = _events.UpdateChannel(
            guild = core_guild,
            channel = copy_channel
        )

        core_event = _events.UpdateChannel(
            guild   = core_guild,
            channel = core_channel
        )
        
        self._dispatch(core_event, copy_event)

    async def _handle_gateway_delete_channel(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#channel-delete

        data_channel = data

        core_channel_id = vessel.keyify(_model.objects.Channel, data_channel)

        data_guild = {}
        try:
            data_guild['id'] = data['guild_id']
        except KeyError:
            core_guild_id = _model.missing
        else:
            core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)

        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)
            core_channel = _model.objects.Channel(data_channel)
        else:
            core_channel = vessel.pop(core_guild.channels, core_channel_id)

        core_event = _events.DeleteChannel(
            guild  = core_guild,
            channel = core_channel
        )

        self._dispatch(core_event)

    async def _handle_gateway_create_thread(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#thread-create

        data_thread = data

        data_guild = {}
        data_guild['id'] = data['guild_id']

        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)

        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)
            core_thread = _model.objects.Channel(data_thread)
        else:
            core_thread = vessel.add(core_guild.threads, data_thread)

        core_event = _events.CreateThread(
            guild  = core_guild,
            thread = core_thread
        )

        self._dispatch(core_event)

    async def _handle_gateway_update_thread(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#thread-update

        data_thread = data

        core_thread_id = vessel.keyify(_model.objects.Channel, data_thread)

        data_guild = {}
        data_guild['id'] = data['guild_id']

        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)

        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        try:
            core_thread = core_guild.threads[core_thread_id]
        except KeyError:
            copy_thread = None
            core_thread = _model.objects.Channel(data_thread)
        else:
            copy_thread = copy.copy(core_thread)
            core_thread = vessel.update(core_thread, data_thread)

        copy_event = _events.UpdateThread(
            guild = core_guild,
            thread = copy_thread
        )
        
        core_event = _events.UpdateThread(
            guild  = core_guild,
            thread = core_thread
        )

        self._dispatch(core_event, copy_event)

    async def _handle_gateway_delete_thread(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#thread-delete

        data_thread = data

        core_thread_id = vessel.keyify(_model.objects.Channel, data_thread)

        data_guild = {}
        data_guild['id'] = data['guild_id']

        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)

        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)
            core_thread  = _model.objects.Channel(data_thread)
        else:
            core_thread = vessel.pop(core_guild.threads, core_thread_id)

        core_event = _events.DeleteThread(
            guild  = core_guild,
            thread = core_thread
        )

        self._dispatch(core_event)

    async def _handle_gateway_sync_threads(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#thread-list-sync

        data_guild = {}
        data_guild['id'] = data['guild_id']

        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)

        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        try:
            data_channel_ids = data['channel_ids']
        except KeyError:
            data_channel_ids = core_guild.channel.keys()
       
        for data_channel_id in data_channel_ids:
            data_channel = {}
            data_channel['id'] = data_channel_id
            core_channel_id = vessel.keyify(_model.objects.Channel, data_channel)

        data_threads = data['threads']

        copy_threads = copy.copy(core_guild.threads)

        core_threads = vessel.update(core_guild.threads, data_threads)

        data_thread_members = data['members']

        for data_thread_member in data_thread_members:
            data_thread = {'member': data_thread_member}
            core_thread_id = vessel.keyify(_model.objects.ThreadMember, data_thread_member)
            core_thread = core_threads[core_thread_id]
            vessel.update(core_thread, data_thread)

        copy_event = _events.SyncThreads(
            guild   = core_guild,
            threads = copy_threads
        )

        core_event = _events.SyncThreads(
            guild   = core_guild,
            threads = core_threads
        )

        self._dispatch(core_event, copy_event)

    async def _handle_gateway_update_thread_member(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#thread-member-update

        data_thread_member = data

        data_thread = {}
        data_thread['id'] = data['id']

        core_thread_id = vessel.keyify(_model.objects.Channel, data_thread)

        data_guild = {}
        data_guild['id'] = data['guild_id']

        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)

        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        try:
            core_thread = core_guild.threads[core_thread_id]
        except KeyError:
            core_thread = _model.objects.Channel(data_thread)
        
        core_thread_member = core_thread.member

        copy_thread_member = copy.copy(core_thread_member)
        
        core_thread_member = vessel.update(core_thread_member, data_thread_member)

        copy_event = _events.UpdateThreadMember(
            guild         = core_guild,
            thread        = core_thread,
            thread_member = copy_thread_member
        )

        core_event = _events.UpdateThreadMember(
            guild         = core_guild,
            thread        = core_thread,
            thread_member = core_thread_member
        )

        self._dispatch(core_event, copy_event)  

    async def _handle_gateway_update_thread_members(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#thread-members-update

        data_guild = {}
        data_guild['id'] = data['guild_id']

        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)
        
        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_thread = {}
        data_thread['id'] = data['id']

        core_thread_id = vessel.keyify(_model.objects.Channel, data_thread)

        try:
            core_thread = core_guild.threads[core_thread_id]
        except KeyError:
            core_thread = core_guild.threads[core_thread_id]

        data_created_thread_members = data['added_members']

        core_created_thread_members = vessel.Collection(_model.objects.ThreadMember, data_created_thread_members)

        try:
            data_deleted_thread_member_ids = data['removed_member_ids']
        except KeyError:
            data_deleted_thread_members = ()
        else:
            data_deleted_thread_members = ({'id': data_id} for data_id in data_deleted_thread_member_ids)
        
        core_deleted_thread_members = vessel.Collection(_model.objects.ThreadMember, data_deleted_thread_members)

        core_event = _events.UpdateThreadMembers(
            guild                  = core_guild,
            thread                 = core_thread,
            created_thread_members = core_created_thread_members,
            deleted_thread_members = core_deleted_thread_members
        )

        self._dispatch(core_event)

    async def _handle_gateway_update_channel_pins(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#channel-pins-update

        data_guild = {}
        try:
            data_guild['id'] = data['guild_id']
        except KeyError:
            core_guild_id = _model.missing
        else:
            core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)
        
        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_channel = {}
        data_channel['id'] = data['channel_id']

        core_channel_id = vessel.keyify(_model.objects.Channel, data_channel)

        try:
            core_channel = core_guild.channels[core_channel_id]
        except KeyError:
            core_channel = core_guild.channels[core_channel_id]

        data_timestamp = data['last_pin_timestamp']

        if data_timestamp is None:
            core_timestamp = None
        else:
            core_timestamp = _model.types.ISO8601Timestamp(data_timestamp)

        core_event = _events.UpdateChannelPins(
            guild     = core_guild,
            channel   = core_channel,
            timestamp = core_timestamp
        )

        self._dispatch(core_event)

    async def _handle_gateway_create_guild(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#guild-create

        data_guild = data

        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)

        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            Event = _events.CreateGuild
            core_guild = vessel.add(self._cache.guilds, data_guild)
        else:
            Event = _events.AvailableGuild
            core_guild = vessel.update(core_guild, data_guild)
        
        core_event = Event(
            guild = core_guild
        )

        self._dispatch(core_event)

    async def _handle_gateway_update_guild(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#guild-update

        data_guild = data

        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)

        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            copy_guild = _model.missing
            core_guild = _model.objects.Guild(data_guild)
        else:
            copy_guild = copy.copy(core_guild)
            core_guild = vessel.update(core_guild, data_guild)

        copy_event = _events.UpdateGuild(
            guild = copy_guild
        )

        core_event = _events.UpdateGuild(
            guild = core_guild
        )

        self._dispatch(core_event, copy_event)

    async def _handle_gateway_delete_guild(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#guild-delete

        data_guild = data

        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)

        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)
        else:
            core_guild = vessel.update(core_guild, data_guild)

        if core_guild.unavailable:
            Event = _events.UnavailableGuild
        else:
            Event = _events.DeleteGuild
        
        core_event = Event(
            guild = core_guild
        )

        self._dispatch(core_event)

    async def _handle_gateway_create_guild_audit_log_entry(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#guild-audit-log-entry-create
        # NOTE: spec does not specify a "guild_id" key

        data_guild = {}
        data_guild['id'] = data['guild_id']

        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)
        
        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_audit_log_entry = data

        core_audit_log_entry = _model.objects.AuditLogEntry(data_audit_log_entry)

        core_event = _events.CreateGuildAuditLogEntry(
            guild                 = core_guild,
            guild_audit_log_entry = core_audit_log_entry
        )

        self._dispatch(core_event)
    
    async def _handle_gateway_create_guild_ban(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#guild-ban-add

        data_guild = {}
        data_guild['id'] = data['guild_id']

        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)
        
        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_user = data['user']

        core_user = _model.objects.User(data_user)

        core_event = _events.CreateGuildBan(
            guild = core_guild,
            user  = core_user
        )

        self._dispatch(core_event)

    async def _handle_gateway_delete_guild_ban(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#guild-ban-remove

        data_guild = {}
        data_guild['id'] = data['guild_id']

        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)
        
        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_user = data['user'] 

        core_user = _model.objects.User(data_user)

        core_event = _events.DeleteGuildBan(
            guild = core_guild,
            user  = core_user
        )

        self._dispatch(core_event)

    async def _handle_gateway_update_guild_emojis(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#guild-emojis-update

        data_guild = {}
        data_guild['id'] = data['guild_id']

        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)
        
        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_emojis = data['emojis']

        copy_emojis = copy.copy(core_guild.emojis)

        core_emojis = vessel.update(core_guild.emojis, data_emojis, clean = True)

        copy_event = _events.UpdateGuildEmojis(
            guild  = core_guild,
            emojis = copy_emojis
        )

        core_event = _events.UpdateGuildEmojis(
            guild  = core_guild,
            emojis = core_emojis
        )

        self._dispatch(core_event, copy_event)

    async def _handle_gateway_update_guild_stickers(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#guild-stickers-update

        data_guild = {}
        data_guild['id'] = data['guild_id']

        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)
        
        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_stickers = data['stickers']

        copy_stickers = copy.copy(core_guild.stickers)

        core_stickers = vessel.update(core_guild.stickers, data_stickers, clean = True)

        copy_event = _events.UpdateGuildStickers(
            guild    = core_guild,
            stickers = copy_stickers
        )

        core_event = _events.UpdateGuildStickers(
            guild    = core_guild,
            stickers = core_stickers
        )

        self._dispatch(core_event, copy_event)

    async def _handle_gateway_update_guild_integrations(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#guild-integrations-update

        data_guild = {}
        data_guild['id'] = data['guild_id']

        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)
        
        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        core_event = _events.UpdateGuildIntegrations(
            guild = core_guild
        )

        self._dispatch(core_event)

    async def _handle_gateway_create_guild_member(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#guild-member-add

        data_guild = {}
        data_guild['id'] = data['guild_id']

        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)
        
        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_guild_member = data

        core_guild_member = vessel.add(core_guild.members, data_guild_member)

        core_event = _events.CreateGuildMember(
            guild        = core_guild,
            guild_member = core_guild_member
        )

        self._dispatch(core_event)

    async def _handle_gateway_delete_guild_member(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#guild-member-remove

        data_guild = {}
        data_guild['id'] = data['guild_id']

        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)
        
        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_guild_member = {}
        data_guild_member['user'] = data['user']

        core_guild_member_id = vessel.keyify(_model.objects.GuildMember, data_guild_member)

        try:
            core_guild_member = vessel.pop(core_guild.members, core_guild_member_id)
        except LookupError:
            core_guild_member = _model.objects.GuildMember(data_guild_member)

        core_event = _events.DeleteGuildMember(
            guild        = core_guild,
            guild_member = core_guild_member
        )

        self._dispatch(core_event)

    async def _handle_gateway_update_guild_member(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#guild-member-update

        data_guild = {}
        data_guild['id'] = data['guild_id']

        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)
        
        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_guild_member = {}
        data_guild_member['user'] = data['user']

        core_guild_member_id = vessel.keyify(_model.objects.GuildMember, data_guild_member)

        try:
            core_guild_member = core_guild.members[core_guild_member_id]
        except KeyError:
            copy_guild_member = None
            core_guild_member = _model.objects.GuildMember(data_guild_member)
        else:
            copy_guild_member = copy.copy(core_guild_member)
            core_guild_member = vessel.update(core_guild_member, data_guild_member)

        copy_event = _events.UpdateGuildMember(
            guild        = core_guild,
            guild_member = copy_guild_member
        )

        core_event = _events.UpdateGuildMember(
            guild        = core_guild,
            guild_member = core_guild_member
        )

        self._dispatch(core_event, copy_event)

    async def _handle_gateway_receive_guild_members(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#guild-members-chunk

        core_index = data['chunk_index']
        core_count = data['chunk_count']

        data_guild = {}
        data_guild['id'] = data['guild_id']

        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)

        try:
            core_indexes = self._guild_members_chunk_indexes[core_guild_id]
        except KeyError:
            core_indexes = self._guild_members_chunk_indexes[core_guild_id] = set(range(core_count))

        core_indexes.discard(core_index)
        
        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_guild_members = data['members']

        copy_guild_members = copy.copy(core_guild.members)
        core_guild_members = vessel.update(core_guild.members, data_guild_members)

        copy_guild_presences = copy.copy(core_guild.presences)
        
        try:
            data_guild_presences = data['presences']
        except KeyError:
            core_guild_presences = _model.missing
        else:
            core_guild_presences = vessel.update(core_guild.presences, data_guild_presences)

        copy_event = _events.ReceiveGuildMembers(
            guild           = core_guild,
            guild_members   = copy_guild_members,
            guild_presences = copy_guild_presences,
            chunk_index     = core_index,
            chunk_indexes   = core_indexes
        )

        core_event = _events.ReceiveGuildMembers(
            guild           = core_guild,
            guild_members   = core_guild_members,
            guild_presences = core_guild_presences,
            chunk_index     = core_index,
            chunk_indexes   = core_indexes
        )

        self._dispatch(core_event, copy_event)

    async def _handle_gateway_create_guild_role(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#guild-role-create

        data_guild = {}
        data_guild['id'] = data['guild_id']

        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)
        
        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_guild_role = data['role']

        core_guild_role = vessel.add(core_guild.roles, data_guild_role)

        core_event = _events.CreateGuildRole(
            guild      = core_guild,
            guild_role = core_guild_role
        )

        self._dispatch(core_event)

    async def _handle_gateway_update_guild_role(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#guild-role-update

        data_guild = {}
        data_guild['id'] = data['guild_id']

        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)
        
        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_guild_role = data['role']

        core_guild_role_id = vessel.keyify(_model.objects.Role, data_guild_role)

        try:
            core_guild_role = core_guild.roles[core_guild_role_id]
        except KeyError:
            copy_guild_role = None
            core_guild_role = _model.objects.Role(data_guild_role)
        else:
            copy_guild_role = copy.copy(core_guild_role)
            core_guild_role = vessel.update(core_guild_role, data_guild_role)

        copy_event = _events.UpdateGuildRole(
            guild = core_guild,
            guild_role = copy_guild_role
        )

        core_event = _events.UpdateGuildRole(
            guild      = core_guild,
            guild_role = core_guild_role
        )

        self._dispatch(core_event, copy_event = copy_event)

    async def _handle_gateway_delete_guild_role(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#guild-role-delete

        data_guild = {}
        data_guild['id'] = data['guild_id']

        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)
        
        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_guild_role = {}
        data_guild_role['id'] = data['role_id']

        core_guild_role_id = vessel.keyify(_model.objects.Role, data_guild_role)

        try:
            core_guild_role = vessel.pop(core_guild.roles, core_guild_role_id)
        except LookupError:
            core_guild_role = _model.objects.Role(data_guild_role)

        core_event = _events.DeleteGuildRole(
            guild      = core_guild,
            guild_role = core_guild_role
        )

        self._dispatch(core_event)

    async def _handle_gateway_create_guild_scheduled_event(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#guild-scheduled-event-create

        data_guild = {}
        data_guild['id'] = data['guild_id']

        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)

        data_guild_scheduled_event = data
        
        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)
            core_guild_scheduled_event = _model.objects.GuildScheduledEvent(data_guild_scheduled_event)
        else:
            core_guild_scheduled_event = vessel.add(core_guild.scheduled_events, data_guild_scheduled_event)

        core_event = _events.CreateGuildScheduledEvent(
            guild                 = core_guild,
            guild_scheduled_event = core_guild_scheduled_event
        )

        self._dispatch(core_event)

    async def _handle_gateway_update_guild_scheduled_event(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#guild-scheduled-event-update

        data_guild = {}
        data_guild['id'] = data['guild_id']

        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)
        
        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_guild_scheduled_event = data

        core_guild_scheduled_event_id = vessel.keyify(_model.objects.GuildScheduledEvent, data_guild_scheduled_event)

        try:
            core_guild_scheduled_event = core_guild.guild_scheduled_events[core_guild_scheduled_event_id]
        except LookupError:
            copy_guild_scheduled_event = _model.missing
            core_guild_scheduled_event = _model.objects.GuildScheduledEvent(data_guild_scheduled_event)
        else:
            copy_guild_scheduled_event = copy.copy(core_guild_scheduled_event)
            core_guild_scheduled_event = vessel.update(core_guild_scheduled_event, data_guild_scheduled_event)

        copy_event = _events.UpdateGuildScheduledEvent(
            guild                 = core_guild,
            guild_scheduled_event = copy_guild_scheduled_event
        )

        core_event = _events.UpdateGuildScheduledEvent(
            guild                 = core_guild,
            guild_scheduled_event = core_guild_scheduled_event
        )

        self._dispatch(core_event, copy_event)  

    async def _handle_gateway_delete_guild_scheduled_event(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#guild-scheduled-event-delete

        data_guild = {}
        data_guild['id'] = data['guild_id']

        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)
        
        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_guild_scheduled_event = data

        core_guild_scheduled_event_id = vessel.keyify(_model.objects.GuildScheduledEvent, data_guild_scheduled_event)

        try:
            core_guild_scheduled_event = vessel.pop(core_guild.scheduled_events, core_guild_scheduled_event_id)
        except LookupError:
            core_guild_scheduled_event = _model.objects.GuildScheduledEvent(data_guild_scheduled_event)

        core_event = _events.DeleteGuildScheduledEvent(
            guild                 = core_guild,
            guild_scheduled_event = core_guild_scheduled_event
        )

        self._dispatch(core_event)
    
    async def _handle_gateway_create_guild_scheduled_event_user(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#guild-scheduled-event-user-add

        data_guild = {}
        data_guild['id'] = data['guild_id']

        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)
        
        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_guild_scheduled_event = {}
        data_guild_scheduled_event['id'] = data['guild_scheduled_event_id']

        core_guild_scheduled_event_id = vessel.keyify(_model.objects.GuildScheduledEvent, data_guild_scheduled_event)

        try:
            core_guild_scheduled_event = core_guild.scheduled_events[core_guild_scheduled_event_id]
        except KeyError:
            core_guild_scheduled_event = _model.objects.GuildScheduledEvent(data_guild_scheduled_event)

        data_user = {}
        data_user['id'] = data['user_id']

        data_guild_member = {}
        data_guild_member['user'] = data_user

        core_guild_member_id = vessel.keyify(_model.objects.GuildMember, data_guild_member)

        try:
            core_guild_member = core_guild.members[core_guild_member_id]
        except KeyError:
            core_guild_member = _model.objects.GuildMember(data_guild_member)

        core_event = _events.CreateGuildScheduledEventUser(
            guild                 = core_guild,
            guild_scheduled_event = core_guild_scheduled_event,
            guild_member          = core_guild_member
        )

        self._dispatch(core_event)

    async def _handle_gateway_delete_guild_scheduled_event_user(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#guild-scheduled-event-user-remove

        data_guild = {}
        data_guild['id'] = data['guild_id']

        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)
        
        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_guild_scheduled_event = {}
        data_guild_scheduled_event['id'] = data['guild_scheduled_event_id']

        core_guild_scheduled_event_id = vessel.keyify(_model.objects.GuildScheduledEvent, data_guild_scheduled_event)

        try:
            core_guild_scheduled_event = core_guild.scheduled_events[core_guild_scheduled_event_id]
        except KeyError:
            core_guild_scheduled_event = _model.objects.GuildScheduledEvent(data_guild_scheduled_event)

        data_user = {}
        data_user['id'] = data['user_id']

        data_guild_member = {}
        data_guild_member['user'] = data_user

        core_guild_member_id = vessel.keyify(_model.objects.GuildMember, data_guild_member)

        try:
            core_guild_member = core_guild.members[core_guild_member_id]
        except KeyError:
            core_guild_member = _model.objects.GuildMember(data_guild_member)

        core_event = _events.DeleteGuildScheduledEventUser(
            guild                 = core_guild,
            guild_scheduled_event = core_guild_scheduled_event,
            guild_member          = core_guild_member
        )

        self._dispatch(core_event)

    async def _handle_gateway_create_integration(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#integration-create

        data_guild = {}
        data_guild['id'] = data['guild_id']

        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)
        
        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_integration = data

        core_integration = _model.objects.Integration(data_integration)

        core_event = _events.CreateIntegration(
            guild       = core_guild,
            integration = core_integration
        )

        self._dispatch(core_event)

    async def _handle_gateway_update_integration(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#integration-update

        data_guild = {}
        data_guild['id'] = data['guild_id']

        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)
        
        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_integration = data

        core_integration = _model.objects.Integration(data_integration)

        core_event = _events.UpdateIntegration(
            guild       = core_guild,
            integration = core_integration
        )

        self._dispatch(core_event)

    async def _handle_gateway_delete_integration(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#integration-delete

        data_guild = {}
        data_guild['id'] = data['guild_id']

        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)
        
        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_integration = {}
        data_integration['id'] = data['id']
        data_application = data_integration['application'] = {}
        try:
            data_application['id'] = data['application_id']
        except KeyError:
            pass

        core_integration = _model.objects.Integration(data_integration)

        core_event = _events.DeleteIntegration(
            guild       = core_guild,
            integration = core_integration
        )

        self._dispatch(core_event)

    async def _handle_gateway_create_invite(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#invite-create

        data_guild = {}
        try:
            data_guild['id'] = data['guild_id']
        except KeyError:
            core_guild_id = _model.missing
        else:
            core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)

        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)
        
        data_channel = {}
        data_channel['id'] = data['channel_id']

        if core_guild:
            core_channel_id = vessel.keyify(_model.objects.Channel, data_channel)
            try:
                core_channel = core_guild.channels[core_channel_id]
            except KeyError:
                make_channel = True
            else:
                make_channel = False
        else:
            make_channel = True

        if make_channel:
            core_channel = _model.objects.Channel(data_channel)
            
        data_invite = data

        core_invite = _model.objects.Invite(data_invite)

        core_event = _events.CreateInvite(
            guild   = core_guild,
            channel = core_channel,
            invite  = core_invite
        )

        self._dispatch(core_event)

    async def _handle_gateway_delete_invite(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#invite-delete

        data_guild = {}
        try:
            data_guild['id'] = data['guild_id']
        except KeyError:
            core_guild_id = _model.missing
        else:
            core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)

        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)
        
        data_channel = {}
        data_channel['id'] = data['channel_id']

        if core_guild:
            core_channel_id = vessel.keyify(_model.objects.Channel, data_channel)
            try:
                core_channel = core_guild.channels[core_channel_id]
            except KeyError:
                make_channel = True
            else:
                make_channel = False
        else:
            make_channel = True

        if make_channel:
            core_channel = _model.objects.Channel(data_channel)

        data_invite = {}
        data_invite['code'] = data['code']

        core_invite = _model.objects.Invite(data_invite)

        core_event = _events.DeleteInvite(
            guild   = core_guild,
            channel = core_channel,
            invite  = core_invite
        )

        self._dispatch(core_event)

    async def _handle_gateway_create_message(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#message-create

        data_guild = {}
        try:
            data_guild['id'] = data['guild_id']
        except KeyError:
            core_guild_id = _model.missing
        else:
            core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)

        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_channel = {}
        data_channel['id'] = data['channel_id']
        data_channel['last_message_id'] = data['id']

        core_channel_id = vessel.keyify(_model.objects.Channel, data_channel)

        try:
            core_channel = core_guild.channels[core_channel_id]
        except KeyError:
            core_channel = _model.objects.Channel(data_channel)
        else:
            core_channel = vessel.update(core_channel, data_channel)

        data_message = data

        core_message = _model.objects.Message(data_message)

        core_event = _events.CreateMessage(
            guild   = core_guild,
            channel = core_channel,
            message = core_message
        )

        self._dispatch(core_event)

    async def _handle_gateway_update_message(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#message-update

        data_guild = {}
        try:
            data_guild['id'] = data['guild_id']
        except KeyError:
            core_guild_id = _model.missing
        else:
            core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)

        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_channel = {}
        data_channel['id'] = data['channel_id']

        core_channel_id = vessel.keyify(_model.objects.Channel, data_channel)

        try:
            core_channel = core_guild.channels[core_channel_id]
        except KeyError:
            core_channel = _model.objects.Channel(data_channel)

        data_message = data
        
        core_message = _model.objects.Message(data_message)

        core_event = _events.UpdateMessage(
            guild   = core_guild,
            channel = core_channel,
            message = core_message
        )

        self._dispatch(core_event)

    async def _handle_gateway_delete_message(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#message-delete

        data_guild = {}
        try:
            data_guild['id'] = data['guild_id']
        except KeyError:
            core_guild_id = _model.missing
        else:
            core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)

        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_channel = {}
        data_channel['id'] = data['channel_id']

        core_channel_id = vessel.keyify(_model.objects.Channel, data_channel)

        try:
            core_channel = core_guild.channels[core_channel_id]
        except KeyError:
            core_channel = _model.objects.Channel(data_channel)

        data_message = {}
        data_message['id'] = data['id']
        
        core_message = _model.objects.Message(data_message)

        core_event = _events.DeleteMessage(
            guild   = core_guild,
            channel = core_channel,
            message = core_message
        )

        self._dispatch(core_event)

    async def _handle_gateway_delete_messages(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#message-delete-bulk

        data_guild = {}
        try:
            data_guild['id'] = data['guild_id']
        except KeyError:
            core_guild_id = _model.missing
        else:
            core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)

        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_channel = {}
        data_channel['id'] = data['channel_id']

        core_channel_id = vessel.keyify(_model.objects.Channel, data_channel)

        try:
            core_channel = core_guild.channels[core_channel_id]
        except KeyError:
            core_channel = _model.objects.Channel(data_channel)

        data_messages = []
        for data_message_id in data['ids']:
            data_message = {}
            data_message['id'] = data_message_id
            data_messages.append(data_message)

        core_messages = vessel.Collection(_model.objects.Message, data_messages)

        core_event = _events.DeleteMessages(
            guild    = core_guild,
            channel  = core_channel,
            messages = core_messages
        )

        self._dispatch(core_event)

    async def _handle_gateway_create_message_reaction(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#message-reaction-add

        data_guild = {}
        try:
            data_guild['id'] = data['guild_id']
        except KeyError:
            core_guild_id = _model.missing
        else:
            core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)

        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_user = {}
        data_user['id'] = data['user_id']

        try:
            data_guild_member = data['member']
        except KeyError:
            core_guild_member = _model.missing
        else:
            core_guild_member_id = vessel.keyify(_model.objects.GuildMember, data_guild_member)
            try:
                core_guild_member = core_guild.members[core_guild_member_id]
            except KeyError:
                core_guild_member = _model.objects.GuildMember(data_guild_member)

        if core_guild_member:
            core_user = core_guild_member.user
        else:
            core_user = _model.objects.User(data_user)

        data_channel = {}
        data_channel['id'] = data['channel_id']

        core_channel_id = vessel.keyify(_model.objects.Channel, data_channel)

        try:
            core_channel = core_guild.channels[core_channel_id]
        except KeyError:
            core_channel = _model.objects.Channel(data_channel)

        data_message = {}
        data_message['id'] = data['message_id']
        
        core_message = _model.objects.Message(data_message)

        data_emoji = data['emoji']

        core_emoji = _model.objects.Emoji(data_emoji)

        core_event = _events.CreateMessageReaction(
            guild        = core_guild,
            guild_member = core_guild_member,
            user         = core_user,
            channel      = core_channel,
            message      = core_message,
            emoji        = core_emoji
        )

        self._dispatch(core_event)

    async def _handle_gateway_delete_message_reaction(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#message-reaction-remove

        data_guild = {}
        try:
            data_guild['id'] = data['guild_id']
        except KeyError:
            core_guild_id = _model.missing
        else:
            core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)

        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_user = {}
        data_user['id'] = data['user_id']

        data_guild_member = {}
        data_guild_member['user'] = data_user

        core_guild_member_id = vessel.keyify(_model.objects.GuildMember, data_guild_member)

        try:
            core_guild_member = core_guild.members[core_guild_member_id]
        except KeyError:
            core_guild_member = _model.missing

        if core_guild_member:
            core_user = core_guild_member.user
        else:
            core_user = _model.objects.User(data_user)

        data_channel = {}
        data_channel['id'] = data['channel_id']

        core_channel_id = vessel.keyify(_model.objects.Channel, data_channel)

        try:
            core_channel = core_guild.channels[core_channel_id]
        except KeyError:
            core_channel = _model.objects.Channel(data_channel)

        data_message = {}
        data_message['id'] = data['message_id']
        
        core_message = _model.objects.Message(data_message)

        data_emoji = data['emoji']

        core_emoji = _model.objects.Emoji(data_emoji)

        core_event = _events.DeleteMessageReaction(
            guild        = core_guild,
            guild_member = core_guild_member,
            user         = core_user,
            channel      = core_channel,
            message      = core_message,
            emoji        = core_emoji
        )

        self._dispatch(core_event)

    async def _handle_gateway_delete_all_message_reactions(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#message-reaction-remove-all

        data_guild = {}
        try:
            data_guild['id'] = data['guild_id']
        except KeyError:
            core_guild_id = _model.missing
        else:
            core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)

        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_channel = {}
        data_channel['id'] = data['channel_id']

        core_channel_id = vessel.keyify(_model.objects.Channel, data_channel)

        try:
            core_channel = core_guild.channels[core_channel_id]
        except KeyError:
            core_channel = _model.objects.Channel(data_channel)

        data_message = {}
        data_message['id'] = data['message_id']
        
        core_message = _model.objects.Message(data_message)

        core_event = _events.DeleteAllMessageReactions(
            guild   = core_guild,
            channel = core_channel,
            message = core_message,
        )

        self._dispatch(core_event)

    async def _handle_gateway_delete_all_message_emoji_reactions(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#message-reaction-remove-emoji

        data_guild = {}
        try:
            data_guild['id'] = data['guild_id']
        except KeyError:
            core_guild_id = _model.missing
        else:
            core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)

        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_channel = {}
        data_channel['id'] = data['channel_id']

        core_channel_id = vessel.keyify(_model.objects.Channel, data_channel)

        try:
            core_channel = core_guild.channels[core_channel_id]
        except KeyError:
            core_channel = _model.objects.Channel(data_channel)

        data_message = {}
        data_message['id'] = data['message_id']
        
        core_message = _model.objects.Message(data_message)

        data_emoji = data['emoji']

        core_emoji = _model.objects.Emoji(data_emoji)

        core_event = _events.DeleteAllMessageEmojiReactions(
            guild   = core_guild,
            channel = core_channel,
            message = core_message,
            emoji   = core_emoji
        )

        self._dispatch(core_event)

    async def _handle_gateway_update_presence(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#presence-update

        data_guild = {}
        data_guild['id'] = data['guild_id']
        
        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)

        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_presence = data

        core_presence_id = vessel.keyify(_model.objects.Presence, data_presence)

        try:
            core_presence = core_guild.presences[core_presence_id]
        except KeyError:
            copy_presence = _model.missing
            core_presence = _model.objects.Presence(data_presence)
        else:
            copy_presence = copy.copy(core_presence)
            core_presence = vessel.update(core_presence, data_presence)

        copy_event = _events.UpdatePresence(
            guild    = core_guild,
            presence = copy_presence
        )

        core_event = _events.UpdatePresence(
            guild    = core_guild,
            presence = core_presence
        )

        self._dispatch(core_event, copy_event)

    async def _handle_gateway_create_typing_indicator(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#typing-start

        data_guild = {}
        try:
            data_guild['id'] = data['guild_id']
        except KeyError:
            core_guild_id = _model.missing
        else:
            core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)

        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_user = {}
        data_user['id'] = data['user_id']

        try:
            data_guild_member = data['member']
        except KeyError:
            core_guild_member = _model.missing
        else:
            core_guild_member_id = vessel.keyify(_model.objects.GuildMember, data_guild_member)
            try:
                core_guild_member = core_guild.members[core_guild_member_id]
            except KeyError:
                core_guild_member = _model.objects.GuildMember(data_guild_member)

        if core_guild_member:
            core_user = core_guild_member.user
        else:
            core_user = _model.objects.User(data_user)

        data_channel = {}
        data_channel['id'] = data['channel_id']

        core_channel_id = vessel.keyify(_model.objects.Channel, data_channel)

        try:
            core_channel = core_guild.channels[core_channel_id]
        except KeyError:
            core_channel = _model.objects.Channel(data_channel)

        data_timestamp = data['timestamp']

        core_timestamp = _model.types.Timestamp(data_timestamp)

        core_event = _events.CreateTypingIndicator(
            guild        = core_guild,
            guild_member = core_guild_member,
            user         = core_user,
            channel      = core_channel,
            timestamp    = core_timestamp
        )

        self._dispatch(core_event)

    async def _handle_gateway_update_self_user(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#user-update

        data_user = data

        core_user = self._cache._usr

        copy_user = copy.copy(core_user)

        core_user = vessel.update(self._cache.user, data_user)

        copy_event = _events.UpdateSelfUser(
            user = copy_user
        )

        core_event = _events.UpdateSelfUser(
            user = core_user
        )

        self._dispatch(core_event, copy_event)

    async def _handle_gateway_update_voice_state(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#voice-state-update

        data_guild = {}
        try:
            data_guild['id'] = data['guild_id']
        except KeyError:
            core_guild_id = _model.missing
        else:
            core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)

        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_voice_state = data

        core_voice_state_id = vessel.keyify(_model.objects.VoiceState, data_voice_state)

        try:
            core_voice_state = core_guild.voice_states[core_voice_state_id]
        except KeyError:
            copy_voice_state = _model.missing
            core_voice_state = _model.objects.VoiceState(data_voice_state)
        else:
            copy_voice_state = copy.copy(core_voice_state)
            core_voice_state = vessel.update(core_voice_state, data_voice_state)

        if core_voice_state.channel_id is None:
            del core_guild[core_voice_state_id]

        if core_voice_state.user_id == self._cache.user.id:
            if core_voice_state.channel_id:
                voice = self._voices.get(core_voice_state.guild_id)
            else:
                voice = await self._stop_voice_client(core_voice_state.guild_id)
        else:
            voice = None

        copy_event = _events.UpdateVoiceState(
            guild       = core_guild,
            voice_state = copy_voice_state,
            voice       = None
        )

        core_event = _events.UpdateVoiceState(
            guild       = core_guild,
            voice_state = core_voice_state,
            voice       = voice
        )

        self._dispatch(core_event, copy_event)

    async def _handle_gateway_update_voice_server(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#voice-server-update

        data_guild = {}
        data_guild['id'] = data['guild_id']
        
        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)

        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_token = data['token']
        core_token = _model.types.String(data_token)

        data_uri_protocol = 'wss://'

        data_uri = data['endpoint']
        if not data_uri.startswith(data_uri_protocol):
            data_uri = data_uri_protocol + data_uri
        core_uri = _model.types.String(data_uri)

        core_event = _events.UpdateVoiceServer(
            guild = core_guild,
            token = core_token,
            uri   = core_uri
        )

        self._dispatch(core_event)

    async def _handle_gateway_update_webhooks(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#webhooks-update

        data_guild = {}
        data_guild['id'] = data['guild_id']
        
        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)

        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_channel = {}
        data_channel['id'] = data['channel_id']

        core_channel_id = vessel.keyify(_model.objects.Channel, data_channel)

        try:
            core_channel = core_guild.channels[core_channel_id]
        except KeyError:
            core_channel = _model.objects.Channel(data_channel)

        core_event = _events.UpdateWebhooks(
            guild   = core_guild,
            channel = core_channel
        )

        self._dispatch(core_event)

    async def _handle_gateway_create_interaction(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#interaction-create

        data_interaction = data

        core_interaction = _model.objects.Interaction(data_interaction)

        core_event = _events.CreateInteraction(
            interaction = core_interaction
        )

        self._dispatch(core_event)

    async def _handle_gateway_create_stage_instance(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#stage-instance-create

        data_guild = {}
        try:
            data_guild['id'] = data['guild_id']
        except KeyError:
            core_guild_id = _model.missing
        else:
            core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)

        data_stage_instance = data

        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)
            core_stage_instance = _model.objects.StageInstance(data_stage_instance)
        else:
            core_stage_instance = vessel.add(core_guild.stage_instances, data_stage_instance)

        core_event = _events.CreateInteraction(
            stage_instance = core_stage_instance
        )

        self._dispatch(core_event)

    async def _handle_gateway_update_stage_instance(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#stage-instance-update

        data_guild = {}
        data_guild['id'] = data['guild_id']

        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)
        
        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_stage_instance = data

        core_stage_instance_id = vessel.keyify(_model.objects.StageInstance, data_stage_instance)

        try:
            core_stage_instance = core_guild.stage_instances[core_stage_instance_id]
        except LookupError:
            copy_stage_instance = _model.missing
            core_stage_instance = _model.objects.StageInstance(data_stage_instance)
        else:
            copy_stage_instance = copy.copy(core_stage_instance)
            core_stage_instance = vessel.update(core_stage_instance, data_stage_instance)

        copy_event = _events.UpdateStageInstance(
            stage_instance = copy_stage_instance
        )

        core_event = _events.UpdateStageInstance(
            stage_instance = core_stage_instance
        )

        self._dispatch(core_event, copy_event)  

    async def _handle_gateway_delete_stage_instance(self, shard, data):

        # https://discord.com/developers/docs/topics/gateway-events#stage-instance-delete

        data_guild = {}
        data_guild['id'] = data['guild_id']

        core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)
        
        try:
            core_guild = self._cache.guilds[core_guild_id]
        except KeyError:
            core_guild = _model.objects.Guild(data_guild)

        data_stage_instance = data

        core_stage_instance_id = vessel.keyify(_model.objects.StageInstance, data_stage_instance)

        try:
            core_stage_instance = vessel.pop(core_guild.scheduled_events, core_stage_instance_id)
        except LookupError:
            core_stage_instance = _model.objects.StageInstance(data_stage_instance)

        core_event = _events.DeleteStageInstance(
            guild          = core_guild,
            stage_instance = core_stage_instance
        )

        self._dispatch(core_event)

    async def _handle_gateway_create_entitlement(self, shard, data):

        # https://discord.com/developers/docs/monetization/entitlements#new-entitlement

        core_entitlement = _model.objects.Entitlement(data)

        core_event = _events.CreateEntitlement(
            entitlement = core_entitlement
        )

        self._dispatch(core_event)

    async def _handle_gateway_update_entitlement(self, shard, data):

        # https://discord.com/developers/docs/monetization/entitlements#updated-entitlement

        core_entitlement = _model.objects.Entitlement(data)

        core_event = _events.UpdateEntitlement(
            entitlement = core_entitlement
        )

        self._dispatch(core_event)

    async def _handle_gateway_delete_entitlement(self, shard, data):

        # https://discord.com/developers/docs/monetization/entitlements#deleted-entitlement

        core_entitlement = _model.objects.Entitlement(data)

        core_event = _events.DeleteEntitlement(
            entitlement = core_entitlement
        )

        self._dispatch(core_event)

    async def _handle_voice_enter(self, voice, data):

        data_guild_id = voice.guild_id

        if data_guild_id is None:
            core_guild = _model.missing
        else:
            data_guild = {}
            data_guild['id'] = voice.guild_id
            core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)
            try:
                core_guild = self._cache.guilds[core_guild_id]
            except KeyError:
                core_guild = _model.objects.Guild(data_guild)

        data_user = {}
        data_user['id'] = data['user_id']

        data_guild_member = {}
        data_guild_member['user'] = data_user

        core_guild_member_id = vessel.keyify(_model.objects.GuildMember, data_guild_member)

        try:
            core_guild_member = core_guild.members[core_guild_member_id]
        except KeyError:
            core_user = _model.objects.User(data_user)
        else:
            core_user = core_guild_member.user

        core_event = _events.EnterVoice(
            guild = core_guild,
            user  = core_user
        )

        self._dispatch(core_event)

    async def _handle_voice_leave(self, voice, data):

        data_guild_id = voice.guild_id

        if data_guild_id is None:
            core_guild = _model.missing
        else:
            data_guild = {}
            data_guild['id'] = voice.guild_id
            core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)
            try:
                core_guild = self._cache.guilds[core_guild_id]
            except KeyError:
                core_guild = _model.objects.Guild(data_guild)

        data_user = {}
        data_user['id'] = data['user_id']

        data_guild_member = {}
        data_guild_member['user'] = data_user

        core_guild_member_id = vessel.keyify(_model.objects.GuildMember, data_guild_member)

        try:
            core_guild_member = core_guild.members[core_guild_member_id]
        except KeyError:
            core_user = _model.objects.User(data_user)
        else:
            core_user = core_guild_member.user

        core_event = _events.LeaveVoice(
            guild = core_guild,
            user  = core_user
        )

        self._dispatch(core_event)

    async def _handle_voice_speak(self, voice, data):

        data_guild_id = voice.guild_id

        if data_guild_id is None:
            core_guild = _model.missing
        else:
            data_guild = {}
            data_guild['id'] = voice.guild_id
            core_guild_id = vessel.keyify(_model.objects.Guild, data_guild)
            try:
                core_guild = self._cache.guilds[core_guild_id]
            except KeyError:
                core_guild = _model.objects.Guild(data_guild)

        data_user = {}
        data_user['id'] = data['user_id']

        data_guild_member = {}
        data_guild_member['user'] = data_user

        core_guild_member_id = vessel.keyify(_model.objects.GuildMember, data_guild_member)

        try:
            core_guild_member = core_guild.members[core_guild_member_id]
        except KeyError:
            core_user = _model.objects.User(data_user)
        else:
            core_user = core_guild_member.user

        data_flags = data['speaking']
        core_flags = _model.enums.SpeechFlags(data_flags)

        data_ssrc = data['ssrc']
        core_ssrc = _model.types.Integer(data_ssrc)

        core_event = _events.Speak(
            guild = core_guild,
            user  = core_user,
            flags = core_flags,
            ssrc  = core_ssrc
        )

        self._dispatch(core_event)

    async def _handle(self, name, event, *args):

        handle_name = f'_handle_{name}_{event.name}'

        try:
            handle = getattr(self, handle_name)
        except AttributeError:
            return # warn log

        with vessel.theme(vessel.Object, unique = False):
            await handle(*args)

    async def _handle_gateway(self, name, *args):
        
        try:
            event = _enums.GatewayEvent(name)
        except ValueError:
            return # warn log

        await self._handle('gateway', event, *args)

    def _request_guild_members(self, fields):

        guild_id = fields['guild_id']

        shard = self._get_shard_via_guild_id(guild_id)

        data = fields

        return shard.request_guild_members(data)
    
    class __request_guild_members(typing.TypedDict):

        guild_id : typing.Required[_model.types.Snowflake]
        query    : typing.Optional[_model.types.String]
        limit    : typing.Optional[_model.types.Integer]
        presences: typing.Optional[_model.types.Boolean]
        user_ids : typing.Optional[list[_model.types.Snowflake]]
        nonce    : typing.Optional[_model.types.String]
    
    def request_guild_members(self, **fields: typing.Unpack[__request_guild_members])  -> typing.Awaitable[None]:

        """
        Use :meth:`.gateway.client.Client.request_guild_members` for the respective guild's shard.
        """

        return self._request_guild_members(fields)
    
    def _create_self_voice_state(self, **fields):

        data = fields

        guild_id = data['guild_id']

        shard = self._get_shard_via_guild_id(guild_id)

        return shard.update_voice_state(data)
    
    class __create_self_voice_state_hint(typing.TypedDict):

        guild_id  : typing.Required[_model.types.Snowflake]
        channel_id: typing.Required[_model.types.Snowflake | None]
        self_mute : typing.Required[_model.types.Boolean]
        self_deaf : typing.Required[_model.types.Boolean]

    def create_self_voice_state(self, **fields: typing.Unpack[__create_self_voice_state_hint])  -> typing.Awaitable[None]:

        """
        Use :meth:`.gateway.client.Client.update_voice_state` for the respective guild's shard.

        .. warning::
            This does not create a voice client, use :meth:`.start_voice` for that.
        """

        return self._create_self_voice_state(**fields)
    
    def _update_self_presence(self, **fields):

        data = fields
        
        coros = []
        for shard in self._shards.values():
            coro = shard.update_presence(data) 
            coros.append(coro)

        return asyncio.gather(*coros)
    
    class __update_self_presence_hint(typing.TypedDict):

        since     : typing.Required[_model.types.Integer | None]
        activities: typing.Required[list[_model.protocols.Activity]]
        status    : typing.Required[_model.enums.StatusType]
        afk       : typing.Required[_model.types.Boolean]
    
    def update_self_presence(self, **fields: typing.Unpack[__update_self_presence_hint])  -> typing.Awaitable[None]:

        """
        Use :meth:`.gateway.client.Client.update_presence` for all shards.
        """

        return self._update_self_presence(fields)

    async def _start_gateway(self, intents, present, shard_ids, shard_count):

        gateway_info = await _http.routes.get_gateway_bot(self._http)

        if shard_count is None:
            shard_count = gateway_info['shards']

        if shard_ids is None:
            shard_ids = range(shard_count)

        shard_ids = tuple(shard_ids)

        gateway_url = gateway_info['url']

        gateway_start_info = gateway_info['session_start_limit']

        shard_concurrency = gateway_start_info['max_concurrency']

        shard_ids_group = (shard_ids[index:index+shard_concurrency] for index in range(0, len(shard_ids), shard_concurrency))

        def get_shard(shard_id):
            def shard_handle(name, *args, **kwargs):
                return self._handle_gateway(name, shard, *args, **kwargs)
            shard = _gateway.client.Client(
                shard_handle,
                self._session,
                self._token,
                intents,
                gateway_url, 
                shard_id, 
                shard_count,
                present = present,
                loads = self._loads,
                dumps = self._dumps
            )
            return shard

        for (shard_ids_index, shard_ids) in enumerate(shard_ids_group):
            if shard_ids_index:
                await asyncio.sleep(5)
            shard_event_coros = []
            shard_start_tasks = []
            for shard_id in shard_ids:
                shard = get_shard(shard_id)
                self._shards[shard_id] = shard
                shard_event_coro = shard.event_identify.wait()
                shard_event_coros.append(shard_event_coro)
                shard_start_coro = shard.start()
                shard_start_task = asyncio.create_task(shard_start_coro)
                shard_start_tasks.append(shard_start_task) 
            await asyncio.gather(*shard_event_coros)

    def start(self,
              intents    : None | _enums.Intents                                 = None,
              shard_ids  : None | list[int]                                      = None,
              shard_count: None | int                                            = None,
              present    : None | typing.Callable[[], _model.protocols.Presence] = None) -> typing.Awaitable[None]:
        
        """
        Start shard connections.
        
        :param intents:
            The intents to identify with.
        :param shard_ids:
            The shard ids to connect to. If not specified, the recommended are used.
        :param shard_count:
            The total number of shards for the client. If not specified, the recommended is used.
        :param present:
            A callable that, when called, returns the desired presence.
        """
        
        if intents is None:
            intents = _enums.Intents.default()

        return self._start_gateway(intents, present, shard_ids, shard_count)

    async def _stop_gateway(self):

        voice_stop_coros = []
        for guild_id in self._voices.keys():
            voice_stop_coro = self._stop_voice_client(guild_id)
            voice_stop_coros.append(voice_stop_coro)

        await asyncio.gather(*voice_stop_coros)

        for sentinels in self._sentinels.values():
            for sentinel in sentinels:
                sentinel.task.cancel()
        
        shard_stop_coros = []
        for shard in self._shards.values():
            shard_stop_coro = shard.stop()
            shard_stop_coros.append(shard_stop_coro)

        await asyncio.gather(*shard_stop_coros)

        await self._session.close()

    def stop(self) -> typing.Awaitable[None]:

        """
        Stop all shard connections and their products and close the session.
        """

        return self._stop_gateway()
    
    async def _handle_voice(self, name, *args):
        
        try:
            event = _enums.VoiceEvent(name)
        except ValueError:
            return # warn log

        await self._handle('voice', event, *args)
    
    async def _start_voice(self, guild_id, channel_id):

        async def update_voice_state_check(core, copy):
            return core.voice_state.user_id == self._cache.user.id and core.voice_state.guild_id == guild_id and core.voice_state.channel_id == channel_id

        update_voice_state_task = self._create_sentinel(_events.UpdateVoiceState, update_voice_state_check)

        async def update_voice_server_check(core):
            return core.guild.id == guild_id

        update_voice_server_task = self._create_sentinel(_events.UpdateVoiceServer, update_voice_server_check)

        await self._create_self_voice_state(
            guild_id = guild_id, 
            channel_id = channel_id, 
            self_mute = False, 
            self_deaf = False
        )

        client_event = await update_voice_state_task
        server_event = await update_voice_server_task

        def get_voice():
            def voice_handle(name, *args, **kwargs):
                return self._handle_voice(name, voice, *args, **kwargs)
            voice = _voice.client.Client(
                voice_handle,
                self._session,
                client_event.voice_state.user_id, 
                client_event.voice_state.guild_id, 
                client_event.voice_state.session_id, 
                server_event.token, 
                server_event.uri
            )
            return voice

        voice = get_voice()

        self._voices[guild_id] = voice

        voice_event_coro = voice.event_complete.wait()
        voice_event_task = asyncio.create_task(voice_event_coro)

        voice_start_coro = voice.start()
        voice_start_task = asyncio.create_task(voice_start_coro)

        await voice_event_task # consistency

        return voice
    
    def start_voice(self, 
                    guild_id  : _model.types.Snowflake, 
                    channel_id: _model.types.Snowflake) -> typing.Awaitable[_voice.client.Client]:
        
        """
        Join a voice channel and start the voice connection lifecycle.

        :param guild_id:
            The id of the joining channel's guild.
        :param channel_id:
            The id of the joining channel.
        """
        
        return self._start_voice(guild_id, channel_id)
    
    async def _stop_voice_client(self, guild_id):

        try:
            voice = self._voices.pop(guild_id)
        except KeyError:
            voice = None
        else:
            await voice.stop()

        return voice
    
    async def _stop_voice_server(self, guild_id):

        voice = self._voices.get(guild_id)

        await self._create_self_voice_state(
            guild_id = guild_id, 
            channel_id = None, 
            self_mute = False, 
            self_deaf = False
        )

        return voice
    
    async def _stop_voice(self, force, guild_id):

        if force:
            voice = await self._stop_voice_client(guild_id)
        else:
            voice = await self._stop_voice_server(guild_id)

        return voice
    
    def stop_voice(self, 
                   guild_id: _model.types.Snowflake, 
                   /, *,
                   force   : bool = False) -> typing.Awaitable[_voice.client.Client]:
        
        """
        Stop the voice connection lifecycle and leave the voice channel.

        :param guild_id:
            The id of the leaving channel's guild.
        :param force:
            Whether to **not** send the gateway request for leaving the channel before stopping the voice client.
        """
        
        return self._stop_voice(force, guild_id)
    



        