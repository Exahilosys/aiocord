import typing
import vessel
import datetime

from . import enums as _enums


__all__ = (
    'String', 'Boolean', 'Integer', 'Decimal', 'List', 'Dict',
    'Timestamp', 'ISO8601Timestamp', 'Snowflake'
)


Object = vessel.Object


Collection = vessel.Collection


String = str


Boolean = bool


Integer = int


Decimal = float


List = list


Dict = dict


class Timestamp(Integer):

    """
    A `Unix Timestamp <https://www.unixtimestamp.com>`_.
    """

    __slots__ = ()

    @property
    def datetime(self) -> datetime.datetime:

        """
        The datetime object representation.
        """

        return datetime.datetime.fromtimestamp(self, tz = datetime.timezone.utc)
    
    def mention(self, style: _enums.TimestampStyle = None):

        """
        Get the mention.

        :param style:
            The visual representation type.
        """

        from . import _mentions

        return _mentions.timestamp(self, style = style)


class ISO8601Timestamp(String):

    """
    |dsrc|
    :ddoc:`ISO8601 Date/Time </reference#iso8601-datetime>`
    """

    __slots__ = ()

    @property
    def datetime(self) -> datetime.datetime:

        """
        The datetime object representation.
        """

        return datetime.datetime.fromisoformat(self)
    

class Snowflake(String):

    """
    |dsrc|
    :ddoc:`Snowflakes </reference#snowflakes>`
    """

    __slots__ = ()

    @property
    def timestamp(self, epoch = 1420070400000) -> Timestamp:

        """
        The internal timestamp.
        """

        return Timestamp(((int(self) >> 22) + epoch) / 1000)