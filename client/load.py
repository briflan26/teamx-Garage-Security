from response import Response, HTTPResponseCodes, HTTPContentTypes
import os
import console


def load_static(path):
    response = Response()
    try:
        size = os.stat(path).st_size
        with open(path, 'rb') as f:
            response.data = f.read(size)
        response.status = HTTPResponseCodes.OK
        if path.lower().endswith('.html'):
            response.content_type = HTTPContentTypes.HTML
        elif path.lower().endswith('.css'):
            response.content_type = HTTPContentTypes.CSS
        elif path.lower().endswith('.js'):
            response.content_type = HTTPContentTypes.JAVASCRIPT
        else:
            response.content_type = HTTPContentTypes.PLAIN
    except (OSError, FileNotFoundError):
        console.error('Unable to read the requested file at {}'.format(path))
        response.status = HTTPResponseCodes.NOT_FOUND
        response.content_type = HTTPContentTypes.PLAIN
        response.data = 'Failure'.encode()

    return response
