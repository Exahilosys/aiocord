import typing
import yarl
import aiohttp
import json
import collections
import asyncio
import types

from . import helpers as _helpers
from . import errors  as _errors


__all__ = ('Client',)


class Client:

    """
    Core means of communication with the HTTP Discord API.

    :param session:
        Used to make requests.
    :param loads:
        Used for converting json text to objects.
    :param dumps:
        Used for converting json objects to text.
    :param ignore_rate:
        Whether to NOT handle rate limiting.
    """

    _version = '10'

    _base_url = yarl.URL(f'https://discord.com/api/v{_version}')

    _user_agent = _helpers.get_user_agent()
    
    _Errors = {
        400: _errors.BadRequest,
        401: _errors.Unauthorized,
        403: _errors.Forbidden,
        404: _errors.NotFound,
        429: _errors.RateLimited
    }

    _rate_marks = {}
    _rate_infos = collections.defaultdict(dict)

    _rate_event = asyncio.Event()
    _rate_event.set()

    __slots__ = ('_session', '_token', '_loads', '_dumps', '_ought_handle_rate')

    def __init__(self, 
                 session    : aiohttp.ClientSession,
                 loads      : typing.Callable[[str], typing.Any] = json.loads,
                 dumps      : typing.Callable[[typing.Any], str] = json.dumps,
                 ignore_rate: bool                               = False):

        self._session = session

        self._token = None

        self._loads = loads
        self._dumps = dumps

        self._ought_handle_rate = not ignore_rate

    def _authenticate(self, token):

        self._token = token

    def authenticate(self,
                     token: None | str) -> None:
        
        """
        Set the authentication token.
        """
        
        self._authenticate(token)

    def _get_headers(self):

        headers = {
            'User-Agent': self._user_agent
        }

        if not (token := self._token) is None:
            headers['Authorization'] = token

        return headers

    async def _execute(self, verb, path, query, data, form, files, headers):

        url = self._base_url.with_path(self._base_url.path + path)

        if not query is None:
            _helpers.clean_query(query)

        sub_headers = headers
            
        headers = self._get_headers()

        if not sub_headers is None:
            headers |= sub_headers

        if not files is None:
            if not form is None:
                raise ValueError('"data" and "files" cannot be used togeter')
            form = aiohttp.FormData(files)
            if not data is None:
                form_json = self._dumps(data)
                form.add_field('payload_json', form_json, content_type = 'application/json')
                data = None

        _helpers.clean_headers(headers)

        response = await self._session.request(
            verb, 
            url, 
            params = query, 
            json = data, 
            data = form,
            headers = headers
        )

        text = await response.text()

        try:
            data = self._loads(text)
        except json.JSONDecodeError:
            data = None

        if response.status < 400:
            return (response, data)

        try:
            Error = self._Errors[response.status]
        except KeyError:
            Error = _errors.Request if response.status < 500 else _errors.Internal

        raise Error(response, data)

    async def _request_bare(self, verb, path, *args, **kwargs):

        response, data = await self._execute(verb, path, *args, **kwargs)

        return data
    
    async def _handle_rate_enter(self, identity):

        await self._rate_event.wait()

        try:
            mark = self._rate_marks[identity]
            info = self._rate_infos[self._token][mark]
        except KeyError:
            return
        
        await info.lock.acquire()

    async def _handle_rate_leave_global(self, headers):

        event = self._rate_event

        if not event.is_set():
            return
        
        event.clear()
        
        loop = asyncio.get_event_loop()

        delay = float(headers['Retry-After'])

        def reset():
            event.set()

        loop.call_later(delay, reset)

    async def _handle_rate_leave_local(self, identity, headers):

        mark = headers['X-RateLimit-Bucket']

        self._rate_marks[identity] = mark

        infos = self._rate_infos[self._token]

        limit = int(headers['X-RateLimit-Limit'])

        try:
            info = infos[mark]
        except KeyError:
            lock = asyncio.Semaphore(value = limit)
            info = infos[mark] = types.SimpleNamespace(lock = lock, timer = None)

        flush = int(headers['X-RateLimit-Remaining'])

        while info.lock._value > flush:
            await info.lock.acquire()

        if flush or not info.timer is None:
            return
        
        loop = asyncio.get_event_loop()

        delay = float(headers['X-RateLimit-Reset-After'])

        def reset():
            for _ in range(limit):
                info.lock.release()
            info.timer = None

        info.timer = loop.call_later(delay, reset)

    def _handle_rate_leave(self, identity, headers):

        score = headers.get('X-RateLimit-Scope', 'user')

        if score == 'global':
            return self._handle_rate_leave_global(headers)

        return self._handle_rate_leave_local(identity, headers)
    
    async def _request_safe(self, identity, verb, path, *args, **kwargs):

        while not self._session.closed:
            await self._handle_rate_enter(identity)
            try:
                response, data = await self._execute(verb, path, *args, **kwargs)
            except _errors.RateLimited as error:
                response = error.response
                delay = error.data['retry_after']
            except:
                delay = None; raise
            else:
                delay = 0   ; break
            finally:
                if not delay is None:
                    await self._handle_rate_leave(identity, response.headers)
                    await asyncio.sleep(delay)
        else:
            raise _errors.Interrupted('session closed while executing a request')

        return data
    
    def _request(self, identity, *args, **kwargs):

        if self._ought_handle_rate and not identity is None:
            return self._request_safe(identity, *args, **kwargs)
        
        return self._request_bare(*args, **kwargs)
        
    async def request(self, 
                      verb    :        str,
                      path    :        str,
                      query   : None | dict[str, str | int | bool] = None, 
                      json    : None | typing.Any                  = None, 
                      data    : None | typing.Any                  = None,
                      files   : None | dict[str, bytes]            = None,
                      headers : None | dict[str, str]              = None,
                      identity: None | typing.Any                  = None) -> typing.Any:
        
        """
        Make a request to the API and get the responding data.

        :param verb:
            The HTTP method.
        :param path:    
            The path portion for the url.
        :param query:
            The HTTP query.
        :param json:
            Used to compose the HTTP body.
        :param data:
            Used to compose the HTTP body.
        :param headers:
            The HTTP headers.
        :param identity:
            Used for handling rate limits.
        """

        data = await self._request(identity, verb, path, query, json, data, files, headers)

        return data

 # type: ignore