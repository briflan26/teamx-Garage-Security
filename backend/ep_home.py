"""
API Endpoint: Requesting the Garage Security Home page
"""


from ep_endpoint import Endpoint
import console
import settings
from response import Response, HTTPResponseCodes, HTTPContentTypes
from request import HTTPMethods
from load import load_static

HOME_P = '/static/html/home.html'


class Home(Endpoint):
    def run(self, db, request):
        if request.method == HTTPMethods.GET:  # GET
            if 'email' in request.params.keys() and 'session' in request.params.keys():
                console.debug('Session Exists: {}'.format(db.users[request.params['email']]))
                if db.check_session(request.params['email'], request.params['session']):
                    console.debug('Session is valid.')
                    return load_static(settings.PROJECT_DIR + HOME_P)
                else:
                    console.debug('Session is invalid.')
                    return Response(code=HTTPResponseCodes.UNAUTHORIZED, content_type=HTTPContentTypes.PLAIN,
                                    data='Authorization Failure'.encode())
            else:
                return Response(code=HTTPResponseCodes.BAD_REQUEST, content_type=HTTPContentTypes.PLAIN,
                                data='Failure'.encode())
        else:
            return Response(code=HTTPResponseCodes.METHOD_NOT_ALLOWED, content_type=HTTPContentTypes.PLAIN,
                            data='Failure'.encode())
