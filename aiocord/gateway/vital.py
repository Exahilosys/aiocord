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

    async def _pulse(self, jitter, interval):

        for cycle in itertools.count(0):
            jit = jitter(cycle) if jitter else 1
            await asyncio.sleep(interval * jit)
            if self._dead:
                await self._save()
            else:
                self._dead = True
                await self._beat()

    def _start(self, jitter, interval):

        coro = self._pulse(jitter, interval)

        self._task = asyncio.create_task(coro)

    def start(self,
              interval: int,
              jitter  : typing.Callable[[int], float] = None) -> None:

        return self._start(jitter, interval)

    async def _stop(self):

        if self._task is None:
            return

        self._task.cancel()

        try:
            await self._task
        except asyncio.CancelledError:
            pass

        self._task = None

    def stop(self) -> typing.Awaitable[None]:

        return self._stop()