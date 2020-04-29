"""
API Endpoint: Camera notifications from Raspberry Pi
"""

from ep_endpoint import Endpoint
import console
from response import Response, HTTPContentTypes, HTTPResponseCodes
from request import HTTPMethods


class SecurityCameraAlert(Endpoint):
    def run(self, db, request):
        if request.method == HTTPMethods.POST:  # POST
            if request.data is None or 'epoch' not in request.data.keys() or 'time' not in request.data.keys() \
                    or 'message' not in request.data.keys():
                return Response(code=HTTPResponseCodes.BAD_REQUEST, content_type=HTTPContentTypes.PLAIN,
                                data='Failure'.encode())
            else:
                console.debug("Alert - {}: {}".format(request.data['time'], request.data['message']))
                db.alert(request.data['epoch'], request.data['time'], request.data['message'])
                return Response(code=HTTPResponseCodes.OK, content_type=HTTPContentTypes.PLAIN,
                                data='Processed'.encode())
        else:
            return Response(code=HTTPResponseCodes.METHOD_NOT_ALLOWED, content_type=HTTPContentTypes.PLAIN,
                            data='Failure'.encode())
