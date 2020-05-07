from http_x.response_x import Response, HTTPResponseCodes, HTTPContentTypes
import os
import console


def load_static(path):
    response = Response()
    path = os.path.abspath(path)
    try:
        size = os.stat(path).st_size
        with open(path, 'rb') as f:
            response.data = f.read(size)
        response.status = HTTPResponseCodes.OK
        response.content_type = None
        for t in HTTPContentTypes:
            if path.lower().endswith(t.name.lower()):
                response.content_type = t
        if response.content_type is None:
            response.content_type = HTTPContentTypes.PLAIN
    except (OSError, FileNotFoundError):
        console.error('Unable to read the requested file at {}'.format(path))
        response.status = HTTPResponseCodes.NOT_FOUND
        response.content_type = HTTPContentTypes.PLAIN
        response.data = 'Failure'.encode()

    return response
