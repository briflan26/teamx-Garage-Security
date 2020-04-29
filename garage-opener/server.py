import socket
from request import Request, HTTPMethods
from response import Response, HTTPContentTypes, HTTPResponseCodes
import console
import garage
import settings


class Server:
    BAD_REQUEST = Response(code=HTTPResponseCodes.BAD_REQUEST, content_type=HTTPContentTypes.PLAIN, data='Failure'.encode())
    UNAUTHORIZED = Response(code=HTTPResponseCodes.UNAUTHORIZED, content_type=HTTPContentTypes.PLAIN, data='Failure'.encode())
    METHOD_NOT_ALLOWED = Response(code=HTTPResponseCodes.UNAUTHORIZED, content_type=HTTPContentTypes.PLAIN, data='Failure'.encode())
    SUCCESS = Response(code=HTTPResponseCodes.OK, content_type=HTTPContentTypes.PLAIN, data='Success'.encode())

    def __init__(self, host_ip=None, host_name=None, port=None):
        if host_ip is None:
            if host_name is None:
                host_name = socket.gethostname()
            host_ip = socket.gethostbyname(host_name)
        if port is None:
            port = 7654

        self.socket = socket.socket()
        self.host_ip = host_ip
        self.host_name = host_name
        self.port = port
        self.socket.bind((self.host_ip, self.port))
        self.socket.listen(5)

    def run(self):
        while True:
            client, address = self.socket.accept()
            message = client.recv(4096)
            self.communicate(client, address, message)

    def communicate(self, client, address, message):
        # PARSE REQUEST
        req = Request(msg=message)
        resp = None
        console.info(
            'Received {} request from {} at {} with {} parameters'.format(req.method.name, address[0], req.path,
                                                                          0 if req.params is None else len(
                                                                              req.params.keys())))
        # CHECK TO MAKE SURE POST REQUEST WAS RECEIVED
        if req.method == HTTPMethods.POST:
            # CHECK TO MAKE SURE DATA WAS RECEIVED
            if req.data is not None:
                # CHECK TO MAKE SURE JSON HAS CORRECT FIELDS
                if 'command' in req.data.keys() and 'key' in req.data.keys():
                    console.debug('Received command: {}'.format(req.data['command']))
                    # AUTHENTICATE KEY
                    if req.data['key'] == settings.MASTER_KEY:
                        # CALL APPROPRIATE FUNCTION (OPEN/CLOSE)
                        if req.data['command'] == 0:
                            garage.open_g()
                            resp = self.SUCCESS
                        elif req.data['command'] == 1:
                            garage.close_g()
                            resp = self.SUCCESS
                        else:
                            resp = self.BAD_REQUEST
                    else:
                        resp = self.UNAUTHORIZED
                else:
                    resp = self.BAD_REQUEST
            else:
                resp = self.BAD_REQUEST
        else:
            resp = self.METHOD_NOT_ALLOWED

        # SEND RESPONSE
        client.send(resp.generate())

        # CLOSE CLIENT CONNECTION
        client.close()

