import settings
from load import load_static
from request import HTTPMethods
from response import Response, HTTPResponseCodes, HTTPContentTypes
from ep_home import Home
from ep_index import Index
from ep_login import Login
from ep_cam import SecurityCameraAlert
from ep_logout import Logout
from ep_gstatus import GarageStatus
from ep_gchange import GarageStatusChange
from ep_camrefresh import CameraAlertRefresh


class API:
    def __init__(self, db, lock, host, port):
        self.db = db
        self.db_lock = lock
        self.host = host
        self.port = port
        # map of all api endpoints and their respective functions
        self.map = {
            '/': Index,
            '/login': Login,
            '/logout': Logout,
            '/home': Home,
            '/security/camera/alert': SecurityCameraAlert,
            '/garage/status': GarageStatus,
            '/security/camera/refresh': CameraAlertRefresh,
            '/garage/status/change': GarageStatusChange
        }
        self.gen_map = {
            '/static/js/constants.js': self.gen_constants
        }

    def route(self, request):
        if request.path in self.map.keys():  # endpoint exists
            self.db_lock.acquire()
            r = self.map[request.path]().run(self.db, request)
            self.db_lock.release()
            return r
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



