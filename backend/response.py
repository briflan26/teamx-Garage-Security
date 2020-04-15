import enum
import time
import os
import sys


class HTTPResponseCodes(enum.Enum):
    OK = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    SERVICE_UNAVAILABLE = 503


class HTTPContentTypes(enum.Enum):
    PLAIN = 'text/plain'
    HTML = 'text/html'
    CSS = 'text/css'
    JAVASCRIPT = 'application/javascript'
    JSON = 'application/json'


class Response:
    def __init__(self, http='HTTP/1.0', code=None, content_type=None, data=None):
        self.version = http
        self.status = code
        self.content_type = content_type
        self.data = data

    def generate(self):
        if self.status is None or self.content_type is None or self.data is None:
            print('[ERROR] Unable to generate response.')
            return -1
        else:
            # http version
            response = self.version + ' '

            # response status
            if self.status == HTTPResponseCodes.OK:
                response += '{} {}\r\n'.format(HTTPResponseCodes.OK, HTTPResponseCodes.OK.name.replace('_', ' '))
            elif self.status == HTTPResponseCodes.BAD_REQUEST:
                response += '{} {}\r\n'.format(HTTPResponseCodes.BAD_REQUEST,
                                               HTTPResponseCodes.BAD_REQUEST.name.replace('_', ' '))
            elif self.status == HTTPResponseCodes.UNAUTHORIZED:
                response += '{} {}\r\n'.format(HTTPResponseCodes.UNAUTHORIZED,
                                               HTTPResponseCodes.UNAUTHORIZED.name.replace('_', ' '))
            elif self.status == HTTPResponseCodes.FORBIDDEN:
                response += '{} {}\r\n'.format(HTTPResponseCodes.FORBIDDEN,
                                               HTTPResponseCodes.FORBIDDEN.name.replace('_', ' '))
            elif self.status == HTTPResponseCodes.NOT_FOUND:
                response += '{} {}\r\n'.format(HTTPResponseCodes.NOT_FOUND,
                                               HTTPResponseCodes.NOT_FOUND.name.replace('_', ' '))
            elif self.status == HTTPResponseCodes.METHOD_NOT_ALLOWED:
                response += '{} {}\r\n'.format(HTTPResponseCodes.METHOD_NOT_ALLOWED,
                                               HTTPResponseCodes.METHOD_NOT_ALLOWED.name.replace('_', ' '))
            elif self.status == HTTPResponseCodes.INTERNAL_SERVER_ERROR:
                response += '{} {}\r\n'.format(HTTPResponseCodes.INTERNAL_SERVER_ERROR,
                                               HTTPResponseCodes.INTERNAL_SERVER_ERROR.name.replace('_', ' '))
            elif self.status == HTTPResponseCodes.NOT_IMPLEMENTED:
                response += '{} {}\r\n'.format(HTTPResponseCodes.NOT_IMPLEMENTED,
                                               HTTPResponseCodes.NOT_IMPLEMENTED.name.replace('_', ' '))
            elif self.status == HTTPResponseCodes.SERVICE_UNAVAILABLE:
                response += '{} {}\r\n'.format(HTTPResponseCodes.SERVICE_UNAVAILABLE,
                                               HTTPResponseCodes.SERVICE_UNAVAILABLE.name.replace('_', ' '))

            # response date
            response += 'Date: {}\r\n'.format(time.ctime())

            # response content type
            response += 'Content-Type: {}\r\n'.format(self.content_type)

            # response content length
            response += 'Content-Length: {}\r\n'.format(sys.getsizeof(self.data))

            # MIME Header
            # response += 'X-Content-Type-Options: nosniff\r\n'

            response += '\r\n'

            response = response.encode()

            response += self.data

            # print('\r\n[INFO] HTTP RESPONSE: ')
            # print(response)
            # print('\r\n')

            return response
