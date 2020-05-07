"""
API Endpoint: Upload Camera Image
"""

from end_points.ep_endpoint import Endpoint
import console
import os
import settings
from http_x.response_x import Response, HTTPContentTypes, HTTPResponseCodes
from http_x.request_x import HTTPMethods
from end_points.ep_camstream import CameraStreamRefresh


class SecurityCameraUpload(Endpoint):
    def run(self, db, request):
        if request.method == HTTPMethods.POST:  # POST
            if request.data is None:
                return Response(code=HTTPResponseCodes.BAD_REQUEST, content_type=HTTPContentTypes.PLAIN,
                                data='Failure'.encode())
            else:
                new, _ = CameraStreamRefresh.get_fn()
                fn = os.path.basename(new)
                console.debug('Newest filename = {}'.format(os.path.basename(new)))
                console.debug('Newest number = {}'.format(fn[:-4]))
                num = int(fn[:-4])
                n_fn = os.path.join(settings.STREAM_DIR, str(num + 1) + '.jpg')
                console.debug('Saving to {}...'.format(n_fn))
                if num % 10 == 0:
                    os.remove(settings.STREAM_DIR + str(num - 10) + '.jpg')
                with open(n_fn, 'wb+') as f:
                    f.write(request.data)
                console.debug('Saved file to {}'.format(n_fn))
                return Response(code=HTTPResponseCodes.OK, content_type=HTTPContentTypes.PLAIN,
                                data='Processed'.encode())
        else:
            return Response(code=HTTPResponseCodes.METHOD_NOT_ALLOWED, content_type=HTTPContentTypes.PLAIN,
                            data='Failure'.encode())
