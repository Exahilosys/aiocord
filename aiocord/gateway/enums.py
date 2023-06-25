import enum


__all__ = ('OpCode',)


class OpCode(enum.IntEnum):

    """
    All possible send/receive opcodes.
    """

    dispatch               = 0
    heartbeat              = 1
    identify               = 2
    update_presence        = 3
    update_voice_state     = 4
    resume                 = 6
    reconnect              = 7
    request_guild_members  = 8
    invalid_session        = 9
    hello                  = 10
    heartbeat_ack          = 11

