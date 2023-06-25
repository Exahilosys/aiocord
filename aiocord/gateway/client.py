import typing
import json
import aiohttp
import collections
import zlib
import random
import os
import asyncio

from . import helpers as _helpers
from . import errors  as _errors
from . import enums   as _enums
from . import vital   as _vital


__all__ = ('Client',)


_Info = collections.namedtuple('Info', 'id count')


class Client:

    """
    Core means of communication with the Discord Gateway API.

    :param callback:
        Used for dispatching events.
    :param session:
        Used for creating websocket connections.
    :param token:
        Used for authentication during 
        :ddoc:`identify </topics/gateway-events#identify>`
        and
        :ddoc:`resume </topics/gateway-events#identify>`.
    :param intents:
        Used for signaling which events to allow through during
        :ddoc:`identify </topics/gateway-events#identify>`.
    :param uri:
        Used for creating werbsocket connections. Must be fetched from
        `Get Gateway:ddoc: Bot </topics/gateway#get-gateway-bot>`.
    :param info_id:
        The id of the shard.
    :param info_count:
        The total amount of shards.
    :param encoding:
        The desired
        :ddoc:`encoding </topics/gateway#encoding-and-compression>`.
        Can be :code:`'json'` or :code:`'etf'`, and by chosing either, 
        :paramref:`.loads` and :paramref:`.dumps` should be adjusted accordingly.
    :param present:
        Used for fetching the initial presence to send during 
        :ddoc:`identify </topics/gateway-events#identify>`.
    :param loads:
        Used for converting json text to objects.
    :param dumps:
        Used for converting json objects to text.
    """

    _version = 10
    _zlib_suffix = b'\x00\x00\xff\xff'

    __slots__ = (
        '_session', '_token', '_intents', '_uri', '_info', '_websocket', 
        '_buffer', '_flator', '_vital', '_sequence', '_callback', '_encoding',
        '_present', '_session_id', '_resume_uri', '_event_identify', '_event_complete',
        '_loads', '_dumps'
    )

    def __init__(self, 
                 callback  : typing.Callable[[str, typing.Any], typing.Awaitable[None]],
                 session   : aiohttp.ClientSession, 
                 token     : str,
                 intents   : int,
                 uri       : str, 
                 info_id   : int, 
                 info_count: int, 
                 encoding  : str                                                = 'json',
                 present   : None | typing.Callable[[], typing.Awaitable[dict]] = None,
                 loads     : typing.Callable[[str], typing.Any]                 = json.loads,
                 dumps     : typing.Callable[[typing.Any], str]                 = json.dumps):

        self._callback = callback

        self._session = session

        self._token = token
        self._intents = intents
        self._uri = uri
        self._info = _Info(info_id, info_count)

        self._websocket = None

        self._buffer = bytearray()
        self._flator = zlib.decompressobj()

        self._vital = _vital.Vital(self._vital_beat, self._vital_save)
        self._sequence = None

        self._encoding = encoding

        self._present = present

        self._session_id = None
        self._resume_uri = None
        
        self._event_identify = asyncio.Event()
        self._event_complete = asyncio.Event()

        self._loads = loads
        self._dumps = dumps

    @property
    def info(self):

        return self._info
    
    @property
    def event_identify(self):

        return self._event_identify
    
    @property
    def event_complete(self):

        return self._event_complete
    
    def _inform_session(self, session_id, resume_uri):

        self._session_id = session_id
        self._resume_uri = resume_uri

    def inform_session(self, 
                       session_id: str, 
                       resume_uri: str):

        """
        Update the session information.

        :param session_id:
            The session id. Can be found as :code:`'session_id'` in the 
            :ddoc:`ready </topics/gateway#ready-event>` event.
        :param resume_uri:
            Used for resuming the session. Can be found as :code:`'resume_gateway_url'` in the 
            :ddoc:`ready </topics/gateway#ready-event>` event.
        """

        self._inform_session(session_id, resume_uri)
    
    async def _send(self, code, data):

        info = {'op': code, 'd': data}

        await self._websocket.send_json(info, dumps = self._dumps)

    async def _send_request_guild_members(self, data):
        
        code = _enums.OpCode.request_guild_members

        await self._send(code, data)

    async def request_guild_members(self, data):

        """
        |dsrc| 
        :ddoc:`Request Guild Members </topics/gateway-events#request-guild-members>`
        """

        await self._send_request_guild_members(data)

    async def _send_update_voice_state(self, data):

        code = _enums.OpCode.update_voice_state

        await self._send(code, data)

    def update_voice_state(self, data) -> typing.Awaitable[None]:
        
        """
        |dsrc| 
        :ddoc:`Update Voice State </topics/gateway-events#update-voice-state>`
        """

        return self._send_update_voice_state(data)

    async def _send_update_presence(self, data):

        code = _enums.OpCode.update_presence

        await self._send(code, data)

    def update_presence(self, 
                        status    : str, 
                        activities: list[dict], 
                        since     : int | None, 
                        afk       : bool) -> typing.Awaitable[None]:

        """
        |dsrc|
        :ddoc:`Update Presence </topics/gateway-events#update-presence>`
        """

        return self._send_update_presence(since, activities, status, afk)

    async def _send_resume(self):

        code = _enums.OpCode.resume

        data = {
            'token': self._token,
            'session_id': self._session_id,
            'seq': self._sequence
        }

        await self._send(code, data)

    async def _send_heartbeat(self):

        code = _enums.OpCode.heartbeat

        data = self._sequence

        await self._send(code, data)

    async def _send_identify(self):

        code = _enums.OpCode.identify

        system_name = os.name
        module_name = __name__.split('.', 1)[0]

        data = {
            'token': self._token,
            'properties': {
                'os': system_name,
                'browser': module_name,
                'device': module_name
            },
            'shard': self._info,
            'token': self._token,
            'intents': self._intents
        }

        if not (present := self._present) is None:
            data['presence'] = await present()

        await self._send(code, data)

    async def _resume(self):

        self._event_complete.clear()

        await self._connect(self._resume_uri)

        await self._send_resume()

        await self._event_complete.wait()

    async def _vital_beat(self):

        await self._send_heartbeat()

    async def _vital_save(self):

        await self._disconnect()

        await self._resume()

    async def _handle_invalid_session(self, info, data):

        resumeable = info.get('d', False)

        if resumeable:
            await self._resume(); return
        
        resuming = self._websocket._response.url == self._resume_uri

        if resuming:
            await self._restart(); return

        raise _errors.Invalidated()

    async def _handle_reconnect(self, info, data):

        await self._resume()

    async def _handle_dispatch(self, info, data):

        self._event_complete.set()
        
        self._sequence = info['s']

        name = info['t']

        await self._callback(name, data)
    
    async def _handle_heartbeat(self, info, data):

        await self._vital_beat()

    async def _handle_heartbeat_ack(self, info, data):

        self._vital.ack()
    
    async def _handle_hello(self, info, data):

        interval = data['heartbeat_interval'] / 1000

        def jitter(cycle):
            if cycle:
                return 1
            return random.random()

        self._vital.start(interval, jitter = jitter)

        await self._send_identify()

        self._event_identify.set()

    async def _listen_BINARY(self, data):
        
        self._buffer.extend(data)

        if len(data) < 4 or not data.endswith(self._zlib_suffix):
            return
        
        info = self._flator.decompress(self._buffer)

        self._buffer.clear()

        info = info.decode()
        info = self._loads(info)

        code = _enums.OpCode(info.pop('op'))

        try:
            handle = getattr(self, f'_handle_{code.name}')
        except AttributeError:
            return # warn log
        
        data = info.pop('d', None)
    
        await handle(info, data)

    _close_codes_finish = {None, 1000}

    _close_codes_resume = {4000, 4002, 4003, 4005, 4007, 4008, 4009}

    async def _egress(self):

        close_code = self._websocket.close_code

        if close_code in self._close_codes_finish:
            return
        
        for routine in (self._resume,):
            close_codes_name =  f'_clode_codes_{routine.__name__}'
            close_codes = getattr(self, close_codes_name)
            if not close_code in close_codes:
                continue
            break
        else:
            raise _errors.Interrupted()
        
        await routine()

    async def _listen(self):

        async for message in self._websocket:
            try:
                handle = getattr(self, f'_listen_{message.type.name}')
            except AttributeError:
                continue
            await handle(message.data)

    async def _process(self):

        while not self._websocket.closed:
            await self._listen()
            await self._egress()

    async def _restart(self):

        await self._stop()
        await self._start()

    async def _disconnect(self):

        self._event_identify.clear()
        self._event_complete.clear()

        await self._websocket.close(code = 1000)

    async def _connect(self, uri):

        query = {
            'v': self._version,
            'encoding': self._encoding,
            'compress': 'zlib-stream'
        }

        _helpers.clean_query(query)

        self._websocket = await self._session.ws_connect(uri,  params = query)

    async def _start(self):

        await self._connect(self._uri)

        await self._listen()

    def start(self) -> typing.Awaitable[None]:

        """
        Start the :ddoc:`connection lifecycle </topics/gateway#connection-lifecycle>`.
        """

        return self._start()

    async def _stop(self):

        await self._vital.stop()

        await self._disconnect()

    def stop(self) -> typing.Awaitable[None]:

        """
        Cancel tasks and close connections.
        """

        return self._stop()