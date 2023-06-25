

__all__ = (
    'Base', 'Client', 'Connectipn', 'Interrupted', 'Invalidated'
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


class Invalidated(Connection):

    """
    Received a non-salvageable :ddoc:`invalid session </topics/gateway-events#invalid-session>`.
    """

    __slots__ = ()