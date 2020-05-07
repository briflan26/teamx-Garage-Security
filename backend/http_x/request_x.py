import console
import enum
import json


class HTTPMethods(enum.Enum):
    GET = 1
    POST = 2
    HEAD = 3
    PUT = 4
    DELETE = 5
    CONNECT = 6
    OPTIONS = 7
    TRACE = 8
    PATCH = 9
    UNKNOWN = 0


class Request:
    def __init__(self, msg):
        self.raw = msg
        self.method = None
        self.path = None
        self.params = None
        self.data = None
        self.content_type = None
        if self.parse() is None:
            self.path = None
            self.data = None

    def parse(self):
        head = None
        data = None
        previous_chars = [None, None, None]
        console.debug('REQUEST: \n{}'.format(self.raw))
        for idx in range(len(self.raw)):
            c = chr(self.raw[idx])
            if c == '\n' and previous_chars[0] == '\r' and previous_chars[1] == '\n' and previous_chars[2] == '\r':
                head = self.raw[0:idx+1]
                if len(self.raw) > idx + 1:
                    data = self.raw[idx+1:]
                break
            else:
                previous_chars[0] = previous_chars[1]
                previous_chars[1] = previous_chars[2]
                previous_chars[2] = c

        utf_raw = head.decode('utf-8')
        path_regex = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890/-.'
        params_regex = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890-=&@.'
        console.debug('RAW REQUEST\n' + utf_raw)

        if utf_raw[0:3] == 'GET':
            self.method = HTTPMethods.GET
            start_i = 3
        elif utf_raw[0:4] == 'POST':
            self.method = HTTPMethods.POST
            start_i = 4
        elif utf_raw[0:4] == 'HEAD':
            self.method = HTTPMethods.HEAD
            start_i = 4
        elif utf_raw[0:3] == 'PUT':
            self.method = HTTPMethods.PUT
            start_i = 3
        elif utf_raw[0:6] == 'DELETE':
            self.method = HTTPMethods.DELETE
            start_i = 6
        elif utf_raw[0:7] == 'CONNECT':
            self.method = HTTPMethods.CONNECT
            start_i = 7
        elif utf_raw[0:7] == 'OPTIONS':
            self.method = HTTPMethods.OPTIONS
            start_i = 7
        elif utf_raw[0:5] == 'TRACE':
            self.method = HTTPMethods.TRACE
            start_i = 5
        else:
            self.method = HTTPMethods.UNKNOWN
            return None

        start_i += 1  # account for the space between method and path
        self.path = ''
        for c in utf_raw[start_i:]:
            c = c
            if c not in path_regex:
                break
            self.path += c
            start_i += 1
        console.debug('Checking for ?: ' + utf_raw[start_i])

        if utf_raw[start_i] == '?':
            start_i += 1
            temp_params = ''
            for c in utf_raw[start_i:]:
                c = c
                if c not in params_regex:
                    break
                temp_params += c
            console.debug('Params: ' + temp_params)

            self.params = dict(k.split('=') for k in temp_params.split('&'))

        else:
            self.params = None
        console.debug('SELF.PARAMS = {}'.format(self.params))

        if self.method == HTTPMethods.POST and data is not None:
            self.data = None
            try:
                self.data = json.loads(data)
            except (json.JSONDecodeError, UnicodeDecodeError):
                console.error('Unable to decode data into a dictionary from HTTP request')
                self.data = data
        else:
            self.data = None

        return True
