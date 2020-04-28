import console
import settings
from load import load_static
from response import Response, HTTPContentTypes, HTTPResponseCodes
from request import HTTPMethods

LOGIN_P = '/static/html/login.html'


def index(db, request):
    if request.method == HTTPMethods.GET:  # GET
        return load_static(settings.PROJECT_DIR + LOGIN_P)
    else:
        return Response(code=HTTPResponseCodes.METHOD_NOT_ALLOWED, content_type=HTTPContentTypes.PLAIN,
                        data='Failure'.encode())

