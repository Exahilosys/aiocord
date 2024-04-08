import typing
import asyncio
import time
import itertools

from . import errors as _errors
from . import audio  as _audio


__all__ = ('Player',)


class Player:

    """
    Manages timely sending voice packets.

    :param send:
        Used with ``(samples, data)`` for sending.
    """

    __slots__ = ('_send', '_audio')

    def __init__(self, 
                 send: typing.Callable[[int, bytes], None]):

        self._send = send

        self._audio = None

    @property
    def audio(self) -> _audio.Audio:

        """
        The current audio source.
        """

        return self._audio

    async def _stream(self):
        
        stamp_anchor = time.perf_counter()

        for cycle in itertools.count(1):
            try:
                data = await self._audio.get()
            except _errors.Audio:
                break
            try:
                self._send(self._audio.frame_samples_count, data)
            except _errors.Transmission:
                break
            stamp_actual = time.perf_counter()
            stamp_expect = stamp_anchor + cycle * self._audio.frame_duration
            delay = max(0, stamp_expect - stamp_actual)
            await asyncio.sleep(delay)

    async def _start(self, audio):

        await self._stop()

        await audio.start()

        self._audio = audio

        try:
            await self._stream()
        finally:
            await self._stop()

    def start(self, 
              audio: _audio.Audio) -> typing.Awaitable[None]:
        
        """
        Start sending voice packets.
        
        :param audio:
            Used for reading.

        .. note::
            Will :meth:`~_audio.Audio.close` the source when all packets have been sent.
        """

        return self._start(audio)
    
    async def _stop(self):

        if self._audio is None:
            return

        await self._audio.stop()

    def stop(self) -> typing.Awaitable[None]:

        """
        Close the current audio source.
        """

        return self._stop()
    