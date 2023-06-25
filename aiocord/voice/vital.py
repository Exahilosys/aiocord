import typing
import asyncio
import itertools


__all__ = ('Vital',)


class Vital:

    __slots__ = ('_beat', '_save', '_task', '_dead')

    def __init__(self, beat, save):

        self._beat = beat
        self._save = save

        self._task = None
        self._dead = False

    @property
    def dead(self):

        return self._dead
    
    def _ack(self):

        self._dead = False 

    def ack(self):

        self._ack()

    async def _pulse(self, interval):

        for cycle in itertools.count(0):
            await asyncio.sleep(interval)
            if self._dead:
                await self._save()
            else:
                self._dead = True
                await self._beat()

    def _start(self, interval):

        coro = self._pulse(interval)

        self._task = asyncio.create_task(coro)

    def start(self,
              interval: int):

        self._start(interval)

    def _stop(self):

        if self._task is None:
            return

        self._task.cancel()

        self._task

        self._task = None

    def stop(self) -> None:

        return self._stop()