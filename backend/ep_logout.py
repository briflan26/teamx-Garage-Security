import console
import settings
from load import load_static
from response import Response, HTTPContentTypes, HTTPResponseCodes
from request import HTTPMethods
import json

LOGOUT_P = '/static/html/logout.html'


def logout(db, request):
    if request.method == HTTPMethods.POST:  # POST
        if 'email' in request.params.keys() and 'session' in request.params.keys():
            console.debug('Database: {}'.format(db.users))
            if db.check_session(request.params['email'], request.params['session']):
                return load_static(settings.PROJECT_DIR + LOGOUT_P)
            else:
                return Response(code=HTTPResponseCodes.UNAUTHORIZED, content_type=HTTPContentTypes.PLAIN,
                                data='Authorization Failure'.encode())
        else:
            return Response(code=HTTPResponseCodes.BAD_REQUEST, content_type=HTTPContentTypes.PLAIN,
                            data='Failure'.encode())
    else:
        return Response(code=HTTPResponseCodes.METHOD_NOT_ALLOWED, content_type=HTTPContentTypes.PLAIN,
                        data='Failure'.encode())
