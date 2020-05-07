"""
API Endpoint: Retrieve the index page
"""


from end_points.ep_endpoint import Endpoint
import settings
from http_x.load_x import load_static
from http_x.response_x import Response, HTTPContentTypes, HTTPResponseCodes
from http_x.request_x import HTTPMethods

LOGIN_P = '/static/html/login.html'


class Index(Endpoint):
    def run(self, db, request):
        if request.method == HTTPMethods.GET:  # GET
            return load_static(settings.PROJECT_DIR + LOGIN_P)
        else:
            return Response(code=HTTPResponseCodes.METHOD_NOT_ALLOWED, content_type=HTTPContentTypes.PLAIN,
                            data='Failure'.encode())

