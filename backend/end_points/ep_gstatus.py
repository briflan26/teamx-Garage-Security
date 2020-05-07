"""
API Endpoint: Receive an acknowledgement from the garage door opener about its status
"""

from end_points.ep_endpoint import Endpoint
from http_x.request_x import HTTPMethods
from http_x.response_x import Response, HTTPContentTypes, HTTPResponseCodes
import console


class GarageStatus(Endpoint):
    def run(self, db, request):
        if request.method == HTTPMethods.POST:  # POST
            if request.data is not None and 'status' in request.data.keys() and 'time' in request.data.keys():
                console.debug("Garage Status - {}: {}".format(request.data['time'], request.data['status']))
                return Response(code=HTTPResponseCodes.OK, content_type=HTTPContentTypes.PLAIN,
                                data='Processed'.encode())
            else:
                return Response(code=HTTPResponseCodes.BAD_REQUEST, content_type=HTTPContentTypes.PLAIN,
                                data='Failure'.encode())
        else:
            return Response(code=HTTPResponseCodes.METHOD_NOT_ALLOWED, content_type=HTTPContentTypes.PLAIN,
                            data='Failure'.encode())
