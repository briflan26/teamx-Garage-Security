"""
API Endpoint: Logging out and destroying session key from browser
"""


from ep_endpoint import Endpoint
import console
from response import Response, HTTPContentTypes, HTTPResponseCodes
from request import HTTPMethods


class Logout(Endpoint):
    def run(self, db, request):
        if request.method == HTTPMethods.POST:  # POST
            if 'email' in request.params.keys() and 'session' in request.params.keys():
                console.debug('Database: {}'.format(db.users))
                if db.check_session(request.params['email'], request.params['session']):
                    return Response(code=HTTPResponseCodes.OK, content_type=HTTPContentTypes.PLAIN, data='Logged out'.encode())
                else:
                    return Response(code=HTTPResponseCodes.UNAUTHORIZED, content_type=HTTPContentTypes.PLAIN,
                                    data='Authorization Failure'.encode())
            else:
                return Response(code=HTTPResponseCodes.BAD_REQUEST, content_type=HTTPContentTypes.PLAIN,
                                data='Failure'.encode())
        else:
            return Response(code=HTTPResponseCodes.METHOD_NOT_ALLOWED, content_type=HTTPContentTypes.PLAIN,
                            data='Failure'.encode())
