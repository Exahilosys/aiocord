

__all__ = (
    'Base', 'Client', 'Connection', 'Interrupted', 'Transmission', 
    'SocketClosed', 'Player', 'Audio', 'Stream', 'StreamPrefixMissing',
    'StreamComplete'
)


class Base(Exception):

    """
    Base module error.
    """

    __slots__ = ()


class Client(Base):

    """
    Base for client errors.
    """

    __slots__ = ()


class Connection(Client):

    """
    Base for connection-related errors.
    """

    __slots__ = ()


class Interrupted(Connection):

    """
    Received a non-salvageable :ddoc:`close code </topics/opcodes-and-status-codes#voice-voice-close-event-codes>`.
    """

    __slots__ = ()


class Transmission(Client):

    """
    Base for creating and sending audio errors.
    """

    __slots__ = ()


class SocketClosed(Transmission):

    """
    The socket is closed upon sending audio.
    """

    __slots__ = ()


class Player(Base):

    """
    Base for :class:`.player.Player` errors.
    """

    __slots__ = ()


class Audio(Player):

    """
    Base for :class:`.audio.Audio` errors.
    """

    __slots__ = ()


class Stream(Audio):

    """
    Base for :class:`.stream.Stream` errors.
    """

    __slots__ = ()


class StreamPrefixMissing(Stream):

    """
    Got an unexpected audio stream OGG prefix.
    """

    __slots__ = ()


class StreamComplete(Stream):

    """
    The audio OGG stream has been exhausted.
    """

    __slots__ = ()