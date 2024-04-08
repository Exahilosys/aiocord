import typing
import asyncio
import subprocess

from . import stream as _stream


__all__ = ('Audio',)


class Audio:

    """
    Manages a FFMPEG subprocess for converting and encoding audio.
    
    :param |dsrc|
        The source of the file, or :code:`'-'` if data is going to be fed later.
    :param executable:
        The path to the FFMPEG executable.
        
    All other parameters should remain as-is according to discord's specification.
    """

    def __init__(self, 
                 source        : str | typing.Literal['-']= '-',
                 executable    : str = 'ffmpeg',
                 codec         : str | None = 'opus',
                 sample_rate   : int = 48000,
                 channels      : int = 2, 
                 bit_depth     : int = 16, 
                 frame_duration: int = 0.02):
        
        self._source = source
        self._executable = executable

        self._sample_rate = sample_rate
        self._channels = channels
        self._bit_depth = bit_depth
        self._frame_duration = frame_duration

        self._codec  = codec
        self._stream = _stream.Stream(self._read)

        self._latent = bytearray()

        self._subprocess = None

    @property
    def sample_rate(self):

        return self._sample_rate
    
    @property
    def channels(self):

        return self._channels
    
    @property
    def frame_duration(self):

        return self._frame_duration

    @property
    def _sample_bytes_count(self):

        return int(self._bit_depth / 8 * self._channels)
    
    @property
    def sample_bytes_count(self):

        return self._sample_bytes_count
    
    @property
    def _frame_samples_count(self):

        return int(self._frame_duration * self._sample_rate)
    
    @property
    def frame_samples_count(self):

        return self._frame_samples_count
    
    @property
    def _frame_bytes_count(self):

        return self._frame_samples_count * self._sample_bytes_count
    
    @property
    def frame_bytes_count(self):

        return self._frame_bytes_count
    
    @property
    def _frame_samples_count(self):

        return int(self._frame_duration * self._sample_rate)
    
    @property
    def frame_samples_count(self):

        return self._frame_samples_count
    
    @property
    def _frame_bytes_count(self):

        return self._frame_samples_count * self._audio.sample_bytes_count
    
    @property
    def frame_bytes_count(self):

        return self._frame_bytes_count
    
    @property
    def join(self):

        return self._stream.join
    
    def _feed(self, data):

        if self._subprocess is None:
            self._latent.extend(data)
        else:
            self._subprocess.stdin.write(data)

    def feed(self, data: bytes) -> None:

        """
        Feed data if :code:`'-'` has been used for the source.

        :param data:
            The data to write to the subprocess.
        """

        return self._feed(data)
    
    async def _read(self, size):

        data = await self._subprocess.stdout.read(size)
        
        return data
    
    async def _get(self):

        wait = self._subprocess.returncode is None

        packet = await self._stream.get(wait)

        return packet
    
    def get(self) -> typing.Awaitable[bytes]:

        """
        Get a single audio packet.
        """

        return self._get()
    
    def _get_ffmpeg_arguments_codec_copy(self):

        arguments = [
            '-c:a', 'copy',
        ]

        return arguments

    def _get_ffmpeg_arguments_codec_opus(self):

        arguments = [
            '-c:a', 'libopus',
            '-b:a', '128K',
            '-frame_duration', f'{int(self._frame_duration * 1000)}',
            '-packet_loss', '0.15',
            '-fec', '1',
            '-cutoff', '20000'
        ]

        return arguments

    def _get_ffmpeg_arguments(self):

        arguments = [
            '-loglevel', 'warning',
            '-i', self._source, 
            '-vn', 
            '-ar', f'{self._sample_rate}', 
            '-ac', f'{self._channels}',
        ]

        if codec := self._codec:
            generate = getattr(self, f'_get_ffmpeg_arguments_codec_{codec}')
            arguments.extend(generate())

        arguments.extend(
            [
                '-f', 'opus',
                'pipe:1'
            ]
        )

        return arguments

    async def _start(self):

        arguments = self._get_ffmpeg_arguments()

        direct = self._source == '-'

        stdin = subprocess.PIPE if direct else None

        self._subprocess = await asyncio.create_subprocess_exec(
            self._executable, *arguments, 
            stdin = stdin, stdout = subprocess.PIPE
        )

        if direct:
            self._subprocess.stdin.write(self._latent)
            self._latent.clear()

        self._stream.start()

    def start(self) -> typing.Awaitable[None]:

        """
        Create the subprocess for feeding and reading data.
        """

        return self._start()
    
    async def _stop(self):

        self._stream.stop()

        try:
            self._subprocess.kill()
        except ProcessLookupError:
            pass
        else:
            await self._subprocess.wait()

    def stop(self) -> typing.Awaitable[None]:

        """
        Stop the reading data and close the subprocess.
        """

        return self._stop()
    
