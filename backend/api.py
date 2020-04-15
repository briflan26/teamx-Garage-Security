import console
import settings
import os
from load import load_static
from db import DataBase
from request import HTTPMethods
from response import Response, HTTPResponseCodes, HTTPContentTypes
from ep_home import home
from ep_index import index
from ep_login import login


class API:
    def __init__(self, host, port):
        self.db = DataBase('db.json')
        self.host = host
        self.port = port
        self.map = {
            '/': index,
            '/login': login,
            '/home': home
        }
        self.gen_map = {
            '/static/js/constants.js': self.gen_constants
        }

    def route(self, request):
        if request.path in self.map.keys():  # endpoint exists
            return self.map[request.path](self.db, request)
        elif request.path in self.gen_map.keys():
            return self.gen_map[request.path](request)
        else:  # endpoint does not exist
            return self.default(request)

    @staticmethod
    def default(request):
        if request.method == HTTPMethods.GET:
            return load_static(settings.PROJECT_DIR + request.path)
        else:
            return Response(code=HTTPResponseCodes.METHOD_NOT_ALLOWED, content_type=HTTPContentTypes.PLAIN,
                            data='Failure'.encode())

    def gen_constants(self, request):
        if request.method == HTTPMethods.GET:
            return Response(code=HTTPResponseCodes.OK, content_type=HTTPContentTypes.JAVASCRIPT,
                            data='const hostname = "{}";\nconst port = {};\n'.format(self.host, self.port).encode())
        else:
            return Response(code=HTTPResponseCodes.METHOD_NOT_ALLOWED, content_type=HTTPContentTypes.PLAIN,
                            data='Failure'.encode())



