import console
import enum
import time


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
            console.error('Unable to generate response.')
            return -1
        else:
            # http version
            response = self.version + ' '

            # response status
            response += '{} {}\r\n'.format(self.status.value, self.status.name.replace('_', ' '))

            # response date
            response += 'Date: {}\r\n'.format(time.ctime())

            # response content type
            response += 'Content-Type: {}\r\n'.format(self.content_type.value)
            console.debug('Content type: {}'.format(self.content_type.value))

            # response content length
            # response += 'Content-Length: {}\r\n'.format(sys.getsizeof(self.data))
            response += 'Content-Length: {}\r\n'.format(len(self.data))

            # MIME Header
            # response += 'X-Content-Type-Options: nosniff\r\n'

            console.debug('RAW RESPONSE HEADER: ' + response.strip())

            response += '\r\n'

            response = response.encode()

            response += self.data

            return response
