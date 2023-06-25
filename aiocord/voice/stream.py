import typing
import struct
import asyncio

from . import errors as _errors


__all__ = ('Stream',)


class Stream:

    _prefix = b'OggS'
    _header_format = '<xBQIIIB'
    _header_size = struct.calcsize(_header_format)

    __slots__ = ('_read', '_queue', '_partial', '_task', '_event_fill')

    def __init__(self, read):

        self._read = read

        self._queue = asyncio.Queue()

        self._partial = b''

        self._task = None
        
        self._event_fill = asyncio.Event()

    async def _join(self):

        await self._event_fill.wait()

        await self._queue.join()

    def join(self) -> typing.Awaitable[None]:

        return self._join()

    async def _fill_next(self):

        prefix = await self._read(4)

        if not prefix == self._prefix:
           raise _errors.StreamPrefixMissing()

        header = await self._read(self._header_size)

        *_, segments_count = struct.unpack(self._header_format, header)

        segments_table = await self._read(segments_count)

        data_sizes = struct.unpack('B' * segments_count, segments_table)

        data = await self._read(sum(data_sizes))

        data = self._partial + data

        data_offset = 0
        packet_size = 0

        for data_size in data_sizes:
            packet_size += data_size
            if not data_size < 255:
                continue
            packet = data[data_offset:data_offset+packet_size]
            self._queue.put_nowait(packet)
            data_offset += packet_size
            packet_size = 0

        self._partial = data[data_offset:]

    async def _fill(self):

        while True:
            try:
                more = await self._fill_next()
            except _errors.StreamPrefixMissing:
                break
            self._event_fill.set()
            
    async def _get(self, wait):
        
        if wait:
            packet = await self._queue.get()
        else:
            try:
                packet = self._queue.get_nowait()
            except asyncio.QueueEmpty:
                raise _errors.StreamComplete()

        return packet
    
    def get(self, wait: bool) -> typing.Awaitable[None]:

        return self._get(wait)

    def _start(self):

        self._event_fill.clear()

        coro = self._fill()
        task = asyncio.create_task(coro)

        self._task = task

    def start(self):

        return self._start()

    def _stop(self):

        self._task.cancel()

    def stop(self):

        return self._stop()