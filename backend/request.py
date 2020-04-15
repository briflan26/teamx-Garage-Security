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
        if self.parse() is None:
            self.path = None
            self.data = None

    def parse(self):
        utf_raw = self.raw.decode('utf-8')
        path_regex = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890/-.'
        params_regex = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890-=&@.'
        console.debug('RAW REQUEST' + utf_raw)

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
            if c not in path_regex:
                break
            self.path += c
            start_i += 1
        console.debug('Checking for ?: ' + utf_raw[start_i])

        if utf_raw[start_i] == '?':
            start_i += 1
            temp_params = ''
            for c in utf_raw[start_i:]:
                if c not in params_regex:
                    break
                temp_params += c
            console.debug('Params: ' + temp_params)

            self.params = dict(k.split('=') for k in temp_params.split('&'))

        else:
            self.params = None
        console.debug('SELF.PARAMS = {}'.format(self.params))

        if self.method == HTTPMethods.POST:
            self.data = ''
            previous_chars = [None, None, None]
            flag = False
            for c in utf_raw:
                if flag:
                    self.data += c
                else:
                    if c == '\n' and previous_chars[0] == '\r' and previous_chars[1] == '\n' and previous_chars[2] == '\r':
                        flag = True
                    else:
                        previous_chars[0] = previous_chars[1]
                        previous_chars[1] = previous_chars[2]
                        previous_chars[2] = c

            try:
                self.data = json.loads(self.data)
            except json.JSONDecodeError:
                console.error('Unable to decode data into a dictionary from HTTP request')
                self.data = None
        else:
            self.data = None

        return True
