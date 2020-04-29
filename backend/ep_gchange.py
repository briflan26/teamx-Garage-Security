"""
API Endpoint: Camera notifications from Raspberry Pi
"""

from ep_endpoint import Endpoint
import console
from response import Response, HTTPContentTypes, HTTPResponseCodes
from request import HTTPMethods


class GarageStatusChange(Endpoint):
    def run(self, db, request):
        if request.method == HTTPMethods.POST:  # POST
            if request.data is not None and 'status' in request.data.keys() and 'email' in request.data.keys() \
                    and 'session' in request.data.keys():
                if db.check_session(request.data['email'], request.data['session']):
                    console.debug("Garage Status Updating to {}".format(request.data['status']))
                    if request.data['status'] == 0:
                        s = self.open()
                    elif request.data['status'] == 1:
                        s = self.close()
                    else:
                        return Response(code=HTTPResponseCodes.BAD_REQUEST, content_type=HTTPContentTypes.PLAIN,
                                        data='Failure'.encode())
                    if s:
                        return Response(code=HTTPResponseCodes.OK, content_type=HTTPContentTypes.PLAIN,
                                        data='Success'.encode())
                    else:
                        return Response(code=HTTPResponseCodes.INTERNAL_SERVER_ERROR,
                                        content_type=HTTPContentTypes.PLAIN, data='Failure'.encode())
                else:
                    return Response(code=HTTPResponseCodes.UNAUTHORIZED, content_type=HTTPContentTypes.PLAIN,
                                    data='Failure'.encode())
            else:
                return Response(code=HTTPResponseCodes.BAD_REQUEST, content_type=HTTPContentTypes.PLAIN,
                                data='Failure'.encode())
        else:
            return Response(code=HTTPResponseCodes.METHOD_NOT_ALLOWED, content_type=HTTPContentTypes.PLAIN,
                            data='Failure'.encode())

    @staticmethod
    def open():
        return True

    @staticmethod
    def close():
        return True
