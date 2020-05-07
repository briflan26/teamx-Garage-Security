"""
API Endpoint: Update image stream for client+
"""

from end_points.ep_endpoint import Endpoint
import console
from http_x.response_x import Response, HTTPContentTypes, HTTPResponseCodes
from http_x.request_x import HTTPMethods
import glob
import settings
from os.path import join


class CameraStreamRefresh(Endpoint):
    def run(self, db, request):
        if request.method == HTTPMethods.GET:  # GET
            if request.params is not None and 'email' in request.params.keys() and 'session' in request.params.keys():
                console.debug('Stream Refresh from {} : {}'.format(request.params['email'], request.params['session']))
                if db.check_session(request.params['email'], request.params['session']):
                    fn, ft = self.get_fn()
                    data = open(fn, 'rb').read()
                    console.debug('Sending {}'.format(fn))
                    return Response(code=HTTPResponseCodes.OK, content_type=ft, data=data)
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
    def get_fn():
        d = sorted(glob.glob(join(settings.STREAM_DIR, '*.jpg')))
        return d[-1], HTTPContentTypes.JPG
