import json


__all__ = (
     'Base', 'Client', 'Interrupted', 'Request', 'Internal', 'BadRequest',
     'Unauthorized', 'Forbidden', 'NotFound', 'RateLimited'
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


class Interrupted(Client):

     """
     A request was interrupted.
     """

     __slots__ = ()


class Request(Client):

     """
     Received a response with an unsupported status.
     """

     __slots__ = ('_response', '_data')

     def __init__(self, response, data):

          self._response = response
          self._data = data

          message = json.dumps(data, indent = 2)

          super().__init__(message)

     @property
     def response(self):

          return self._response
     
     @property
     def data(self):

          return self._data


class Internal(Request):

     """
     There was an server error.
     """

     __slots__ = ()


class BadRequest(Request):

     """
     The request was badly formatted.
     """
     
     __slots__ = ()


class Unauthorized(Request):

     """
     The request token is missing or invalid.
     """
     
     __slots__ = ()

    
class Forbidden(Request):

     """
     The user is missing the necessary permissions for the request.
     """
     
     __slots__ = ()


class NotFound(Request):

     """
     The target resource could not be found.
     """
     
     __slots__ = ()


class RateLimited(Request):

     """
     There are too many requests being sent.
     """
     
     __slots__ = ()
