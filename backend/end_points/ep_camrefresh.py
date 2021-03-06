"""
API Endpoint: Camera notifications from Raspberry Pi
"""

from end_points.ep_endpoint import Endpoint
import console
from http_x.response_x import Response, HTTPContentTypes, HTTPResponseCodes
from http_x.request_x import HTTPMethods
import json


class CameraAlertRefresh(Endpoint):
    def run(self, db, request):
        if request.method == HTTPMethods.GET:  # GET
            if request.params is not None and 'email' in request.params.keys() and 'session' in request.params.keys() and 'epoch' in request.params.keys():
                console.debug('Refresh from {} : {}, {}'.format(request.params['email'], request.params['session'], request.params['epoch']))
                alerts = db.get_alerts(int(request.params['epoch']))
                data = dict()
                if len(alerts.keys()) == 0:
                    data['status'] = 1
                else:
                    data['alerts'] = alerts
                    data['status'] = 0
                data = json.dumps(data).encode()
                # TODO add another field that has the epoch time to be used for comparisons in the JS code - whats the
                #  latest notification received?
                return Response(code=HTTPResponseCodes.OK, content_type=HTTPContentTypes.JSON, data=data)
            else:
                return Response(code=HTTPResponseCodes.BAD_REQUEST, content_type=HTTPContentTypes.PLAIN,
                                data='Failure'.encode())
        else:
            return Response(code=HTTPResponseCodes.METHOD_NOT_ALLOWED, content_type=HTTPContentTypes.PLAIN,
                            data='Failure'.encode())
