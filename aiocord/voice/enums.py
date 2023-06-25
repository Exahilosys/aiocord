import enum


__all__ = ('OpCode',)


class OpCode(enum.IntEnum):

    """
    All possible send/receive opcodes.
    """

    identify            = 0
    select_protocol     = 1
    ready               = 2
    heartbeat           = 3
    session_description = 4
    speaking            = 5
    heartbeat_ack       = 6
    resume              = 7
    hello               = 8
    resumed             = 9
    connect             = 18
    disconnect          = 13
