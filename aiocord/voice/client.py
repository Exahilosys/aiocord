import typing
import aiohttp
import json
import asyncio
import socket
import struct
import nacl.secret

from . import helpers as _helpers
from . import enums   as _enums
from . import errors  as _errors
from . import vital   as _vital
from . import player  as _player


__all__ = ('Client',)


class Client:

    """
    Core means of communication with the Discord Voice API.

    :param callback:
        Used for dispatching events.
    :param session:
        Used for creating websocket connections.
    :param user_id:
        The connecting client's user id.
    :param guild_id:
        The connecting guild's id.
    :param session_id:
        The :ddoc:`voice state </topics/gateway-events#voice-state-update>` session id.
    :param token:
        The :ddoc:`voice server </topics/gateway-events#voice-state-update>` token.
    :param uri:
        The :ddoc:`voice server </topics/gateway-events#voice-state-update>` endpoint.
    :param loads:
        Used for converting json text to objects.
    :param dumps:
        Used for converting json objects to text.
    """

    _version = 4

    __slots__ = (
        '_callback', '_session', '_user_id', '_guild_id', '_session_id', 
        '_token', '_uri', '_loads', '_dumps', '_websocket', '_vital',
        '_event_identify', '_event_complete', '_ssrc', '_address', '_socket',
        '_encrypt', '_sequence', '_timestamp', '_secret', '_codec', '_player'
    )

    def __init__(self, 
                 callback  : typing.Callable[[str, typing.Any], typing.Awaitable[None]],
                 session   : aiohttp.ClientSession, 
                 user_id   : str, 
                 guild_id  : str, 
                 session_id: str, 
                 token     : str, 
                 uri       : str,
                 loads     : typing.Callable[[str], typing.Any] = json.loads,
                 dumps     : typing.Callable[[typing.Any], str] = json.dumps):

        self._callback = callback

        self._session = session

        self._user_id = user_id
        self._guild_id = guild_id
        self._session_id = session_id
        self._token = token

        self._uri = uri

        self._loads = loads
        self._dumps = dumps

        self._websocket = None

        self._vital = _vital.Vital(self._vital_beat, self._vital_save)

        self._event_identify = asyncio.Event()
        self._event_complete = asyncio.Event()

        self._ssrc = None
        self._address = None

        self._socket = None

        self._encrypt = None

        self._sequence = 0
        self._timestamp = 0

        self._secret = None
        self._codec = None

        self._player = _player.Player(self._send_audio)

    @property
    def guild_id(self) -> str:

        """
        The connected guild's id.
        """

        return self._guild_id

    @property
    def event_identify(self) -> asyncio.Event:

        """
        Set after the identify payload has been sent.
        """

        return self._event_identify
    
    @property
    def event_complete(self) -> asyncio.Event:

        """
        Set after the session description has been handled or when resumed.
        """

        return self._event_complete
    
    @property
    def codec(self) -> str:

        """
        The name of the expected codec.
        """

        return self._codec
    
    @property
    def player(self) -> _player.Player:

        """
        The player.
        """

        return self._player

    async def _recv_packet(self, size):

        loop = asyncio.get_event_loop()

        data = await loop.sock_recv(self._socket, size)

        return data
    
    def _send_packet(self, data):

        if self._socket._closed:
            raise _errors.SocketClosed()

        size = self._socket.send(data)

        return size
    
    def _make_packet(self, data):

        header = self._make_packet_header()

        data = self._encrypt(bytes(header), data)

        return header + data
    
    def _make_packet_header(self):

        header = bytearray(12)

        header[0] = 0x80
        header[1] = 0x78

        struct.pack_into('>H', header, 2, self._sequence)
        struct.pack_into('>I', header, 4, self._timestamp)
        struct.pack_into('>I', header, 8, self._ssrc)

        return header
    
    def _send_audio(self, samples, data):

        packet = self._make_packet(data)
        
        self._send_packet(packet)

        self._sequence = _helpers.max_add(self._sequence, 1, 65535)
        self._timestamp = _helpers.max_add(self._timestamp, samples, 4294967295)

    def send_audio(self, samples: int, data: bytes) -> None:

        """
        Send an audio packet.
        
        :param samples:
            The sample count per frame.
        :param data:
            The encoded packet data.
        """

        return self._send_audio(samples, data)

    async def _send(self, code, data):

        info = {'op': code, 'd': data}

        await self._websocket.send_json(info, dumps = self._dumps)

    async def _send_resume(self):

        code = _enums.OpCode.resume

        data = {
            'server_id': self._guild_id,
            'session_id': self._session_id,
            'token': self._token
        }

        await self._send(code, data)

    async def _send_speaking(self, flags):

        code = _enums.OpCode.speaking

        data = {
            'speaking': flags,
            'delay': 0,
            'ssrc': self._ssrc
        }

        await self._send(code, data)

    async def _send_select_protocol(self, ip, port, mode):

        code = _enums.OpCode.select_protocol

        data = {
            'protocol': 'udp',
            'data': {
                'address': ip,
                'port': port,
                'mode': mode
            }
        }

        await self._send(code, data)
        
    async def _send_heartbeat(self):

        loop = asyncio.get_event_loop()

        code = _enums.OpCode.heartbeat

        data = loop.time()

        await self._send(code, data)

    async def _send_identify(self):

        code = _enums.OpCode.identify

        data = {
            'server_id': self._guild_id,
            'user_id': self._user_id,
            'session_id': self._session_id,
            'token': self._token
        }

        await self._send(code, data)

    async def _resume(self):

        self._event_complete.clear()

        await self._disconnect()

        await self._send_resume()

        await self._event_complete.wait()

    async def _vital_save(self):

        await self._resume()

    async def _vital_beat(self):

        await self._send_heartbeat()

    async def _discover_address(self):
        
        size = 74

        packet = bytearray(size)

        struct.pack_into('>H', packet, 0, 1)
        struct.pack_into('>H', packet, 2, 70)
        struct.pack_into('>I', packet, 4, self._ssrc)

        self._send_packet(packet)

        data = await self._recv_packet(size)

        ip_enter = 8
        ip_leave = data.index(0, ip_enter)
        ip = data[ip_enter:ip_leave]
        ip = ip.decode()

        port = struct.unpack_from('>H', data, size - 2)[0]
        
        return ip, port

    async def _connect_udp(self):

        loop = asyncio.get_event_loop()

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        sock.setblocking(False)

        await loop.sock_connect(sock, self._address)

        self._socket = sock

    def _encrypt_xsalsa20_poly1305(self, header, data):

        nonce = bytearray(24)

        nonce[:12] = header

        message = self._secret.encrypt(data, bytes(nonce))

        return message.ciphertext
    
    async def _handle_disconnect(self, info, data):

        name = 'LEAVE'

        await self._callback(name, data)
    
    async def _handle_connect(self, info, data):

        name = 'ENTER'

        await self._callback(name, data)
    
    async def _handle_speaking(self, info, data):

        name = 'SPEAK'

        await self._callback(name, data)
    
    async def _handle_resumed(self, info, data):

        self._event_complete.set()

    async def _handle_session_description(self, info, data):

        mode = data['mode']

        self._encrypt = getattr(self, f'_encrypt_{mode}')

        self._secret = nacl.secret.SecretBox(bytes(data['secret_key']))

        self._codec = data['audio_codec']

        await self._send_speaking(1)

        self._event_complete.set()

    async def _handle_ready(self, info, data):

        self._ssrc = data['ssrc']

        self._address = (data['ip'], data['port'])

        for mode in data['modes']:
            if not hasattr(self, f'_encrypt_{mode}'):
                continue
            break
        else:
            raise RuntimeError('missing supported mode')

        await self._connect_udp()

        ip, port = await self._discover_address()

        await self._send_select_protocol(ip, port, mode)

    async def _handle_heartbeat_ack(self, info, data):

        self._vital.ack()

    async def _handle_hello(self, info, data):
        
        self._vital.start(data['heartbeat_interval'] / 1000)

    async def _listen_TEXT(self, data):

        info = self._loads(data)

        try:
            code = _enums.OpCode(info.pop('op'))
        except ValueError:
            return

        try:
            handle = getattr(self, f'_handle_{code.name}')
        except AttributeError:
            return # warn log
        
        data = info.pop('d', None)
        
        await handle(info, data)

    _close_codes_finish = {None, 1000}

    _close_codes_resume = {4015}

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

    async def _disconnect(self):

        await self._websocket.close(code = 1000)
    
    async def _connect(self):

        query = {
            'v': self._version
        }

        self._websocket = await self._session.ws_connect(self._uri, params = query)

    async def _start(self):

        await self._connect()

        await self._send_identify()

        self._event_identify.set()

        await self._listen()

    def start(self) -> typing.Awaitable[None]:

        """
        Start the :ddoc:`connection lifecycle </topics/voice-connections#connecting-to-voice>`.
        """

        return self._start()
    
    async def _stop(self):

        await self._player.stop()

        self._socket.close()

        self._vital.stop()

        await self._websocket.close()

    def stop(self) -> typing.Awaitable[None]:

        """
        Cancel tasks and close connections.
        """

        return self._stop()
    
