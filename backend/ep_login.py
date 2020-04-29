"""
API Endpoint: Logging in from browser and returning a session key
"""


from ep_endpoint import Endpoint
import console
from response import Response, HTTPContentTypes, HTTPResponseCodes
from request import HTTPMethods
import json


class Login(Endpoint):
    def run(self, db, request):
        if request.method == HTTPMethods.POST:  # POST
            if request.data is None or 'email' not in request.data.keys() or 'password' not in request.data.keys():
                return Response(code=HTTPResponseCodes.BAD_REQUEST, content_type=HTTPContentTypes.PLAIN,
                                data='Failure'.encode())
            else:
                console.debug("Login Attempt - {}: {}".format(request.data['email'], request.data['password']))
                session = db.login(request.data['email'], request.data['password'])
                if session is not None:
                    console.debug("Login Successful - {}: {}".format(request.data['email'], session))
                    return Response(code=HTTPResponseCodes.OK, content_type=HTTPContentTypes.JSON,
                                    data=json.dumps({'status': 0, 'session': session}).encode())
                else:
                    console.debug("Login Unsuccessful - {}".format(request.data['email']))
                    return Response(code=HTTPResponseCodes.OK, content_type=HTTPContentTypes.JSON,
                                    data=json.dumps({'status': 1, 'session': 0}).encode())
        else:
            return Response(code=HTTPResponseCodes.METHOD_NOT_ALLOWED, content_type=HTTPContentTypes.PLAIN,
                            data='Failure'.encode())
