import json
import os
from db import DataBase
from request import HTTPMethods
from response import Response, HTTPResponseCodes, HTTPContentTypes


class API:
    LOGIN_P = '/static/html/login.html'
    HOME_P = '/static/html/home.html'
    PROJET_DIR = '..'

    def __init__(self, host, port):
        self.db = DataBase('db.json')
        self.host = host
        self.port = port
        self.map = {
            '/': self.index,
            '/login': self.login,
            '/home': self.home
        }
        self.gen_map = {
            '/static/js/constants.js': self.gen_constants
        }

    def route(self, request):
        if request.path in self.map.keys():  # endpoint exists
            return self.map[request.path](request).generate()
        elif request.path in self.gen_map.keys():
            return self.gen_map[request.path](request).generate()
        else:  # endpoint does not exist
            return self.default(request).generate()

    def default(self, request):
        if request.method == HTTPMethods.GET:
            return self.load_static(API.PROJET_DIR + request.path)
        else:
            return Response(code=HTTPResponseCodes.METHOD_NOT_ALLOWED, content_type=HTTPContentTypes.PLAIN,
                            data='Failure'.encode())

    @staticmethod
    def load_static(path):
        response = Response()
        try:
            size = os.stat(path).st_size
            with open(path, 'rb') as f:
                response.data = f.read(size)
            response.status = HTTPResponseCodes.OK
            if path.lower().endswith('.html'):
                response.content_type = HTTPContentTypes.HTML
            elif path.lower().endswith('.css'):
                response.content_type = HTTPContentTypes.CSS
            elif path.lower().endswith('.js'):
                response.content_type = HTTPContentTypes.JAVASCRIPT
            else:
                response.content_type = HTTPContentTypes.PLAIN
        except (OSError, FileNotFoundError):
            print('[ERROR] Unable to read the requested file at {}'.format(path))
            response.status = HTTPResponseCodes.NOT_FOUND
            response.content_type = HTTPContentTypes.PLAIN
            response.data = 'Failure'.encode()

        return response

    def gen_constants(self, request):
        return Response(code=HTTPResponseCodes.OK, content_type=HTTPContentTypes.JAVASCRIPT,
                        data='const hostname = "{}";\nconst port = {};\n'.format(self.host, self.port).encode())

    def index(self, request):
        if request.method == HTTPMethods.GET:  # GET
            return self.load_static(API.PROJET_DIR + API.LOGIN_P)
        else:
            return Response(code=HTTPResponseCodes.METHOD_NOT_ALLOWED, content_type=HTTPContentTypes.PLAIN,
                            data='Failure'.encode())

    def login(self, request):
        if request.method == HTTPMethods.POST:  # POST
            if request.data is None or 'email' not in request.data.keys() or 'password' not in request.data.keys():
                return Response(code=HTTPResponseCodes.BAD_REQUEST, content_type=HTTPContentTypes.PLAIN,
                                data='Failure'.encode())
            else:
                print("[INFO] Login Attempt - {}: {}".format(request.data['email'], request.data['password']))
                session = self.db.login(request.data['email'], request.data['password'])
                if session is not None:
                    print("[INFO] Login Successful - {}: {}".format(request.data['email'], session))
                    return Response(code=HTTPResponseCodes.OK, content_type=HTTPContentTypes.JSON,
                                    data=json.dumps({'status': 0, 'session': session}).encode())
                else:
                    print("[INFO] Login Unsuccessful - {}".format(request.data['email']))
                    return Response(code=HTTPResponseCodes.OK, content_type=HTTPContentTypes.JSON,
                                    data=json.dumps({'status': 1, 'session': 0}).encode())
        else:
            return Response(code=HTTPResponseCodes.METHOD_NOT_ALLOWED, content_type=HTTPContentTypes.PLAIN,
                            data='Failure'.encode())

    def home(self, request):
        if request.method == HTTPMethods.GET:  # GET
            if 'email' in request.params.keys() and 'session' in request.params.keys():
                print('[DEBUG] Database: {}'.format(self.db.users))
                if self.db.check_session(request.params['email'], request.params['session']):
                    return self.load_static(API.PROJET_DIR + API.HOME_P)
                else:
                    return Response(code=HTTPResponseCodes.UNAUTHORIZED, content_type=HTTPContentTypes.PLAIN,
                                    data='Authorization Failure'.encode())
            else:
                return Response(code=HTTPResponseCodes.BAD_REQUEST, content_type=HTTPContentTypes.PLAIN,
                                data='Failure'.encode())
        else:
            return Response(code=HTTPResponseCodes.METHOD_NOT_ALLOWED, content_type=HTTPContentTypes.PLAIN,
                            data='Failure'.encode())
