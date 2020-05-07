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
    # text
    PLAIN = 'text/plain'
    HTML = 'text/html'
    CSS = 'text/css'

    # application
    JS = 'application/javascript'
    JSON = 'application/json'
    WOFF = 'application/x-font-woff'
    WOFF2 = 'application/x-font-woff'
    TTF = 'application/x-font-ttf'
    EOT = 'application/vnd.ms-fontobject'

    # image
    JPG = 'image/jpg'
    JPEG = 'image/jpeg'
    ICO = 'image/x-icon'
    SVG = 'image/svg+xml'


class Response:
    def __init__(self, http='HTTP/1.0', code=None, content_type=None, data=None, raw=None):
        if raw is not None:
            self.version = None
            self.status = None
            self.data = None
            self.content_type = None
            self.parse(raw)
        else:
            self.version = http
            self.status = code
            self.content_type = content_type
            self.data = data

    def parse(self, raw):
        utf_raw = raw.decode('utf-8')
        console.debug('RAW RESPONSE:  ' + utf_raw)

        self.version = utf_raw[0:8]
        console.debug("VERSION: " + self.version)
        s = int(utf_raw[9:12])
        self.status = HTTPResponseCodes(s)

        # for s in HTTPResponseCodes:
        #     i = 9 + len(s.name)
        #     if utf_raw[9:i] == s.name and utf_raw[i+1:i+5] == str(s.value):
        #         self.status = s

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
