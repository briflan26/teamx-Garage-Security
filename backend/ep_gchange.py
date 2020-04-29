"""
API Endpoint: Camera notifications from Raspberry Pi
"""

from ep_endpoint import Endpoint
import console
from response import Response, HTTPContentTypes, HTTPResponseCodes
from request import HTTPMethods
import socket
import settings
import json


class GarageStatusChange(Endpoint):
    def run(self, db, request):
        if request.method == HTTPMethods.POST:  # POST
            if request.data is not None and 'status' in request.data.keys() and 'email' in request.data.keys() \
                    and 'session' in request.data.keys():
                if db.check_session(request.data['email'], request.data['session']):
                    console.debug("Garage Status Updating to {}".format(request.data['status']))
                    if request.data['status'] == 0:
                        s = self.open()
                    elif request.data['status'] == 1:
                        s = self.close()
                    else:
                        return Response(code=HTTPResponseCodes.BAD_REQUEST, content_type=HTTPContentTypes.PLAIN,
                                        data='Failure'.encode())
                    if s:
                        return Response(code=HTTPResponseCodes.OK, content_type=HTTPContentTypes.PLAIN,
                                        data='Success'.encode())
                    else:
                        return Response(code=HTTPResponseCodes.INTERNAL_SERVER_ERROR,
                                        content_type=HTTPContentTypes.PLAIN, data='Failure'.encode())
                else:
                    return Response(code=HTTPResponseCodes.UNAUTHORIZED, content_type=HTTPContentTypes.PLAIN,
                                    data='Failure'.encode())
            else:
                return Response(code=HTTPResponseCodes.BAD_REQUEST, content_type=HTTPContentTypes.PLAIN,
                                data='Failure'.encode())
        else:
            return Response(code=HTTPResponseCodes.METHOD_NOT_ALLOWED, content_type=HTTPContentTypes.PLAIN,
                            data='Failure'.encode())

    def open(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            console.debug("Socket successfully created")
        except socket.error as err:
            console.error("socket creation failed with error {}".format(err))

        s.connect((settings.GARAGE_DOOR_IP_ADDRESS, settings.GARAGE_DOOR_PORT))

        console.debug("the socket has successfully connected to {}".format(settings.GARAGE_DOOR_IP_ADDRESS))

        data = self.build(cmd=0)

        s.send(data)

        console.debug(data.decode('utf-8'))

        console.debug("Successfully sent message")

        resp = Response(raw=s.recv(4096))
        console.debug("RESPONSE: {}".format(resp.status))

        if resp.status == HTTPResponseCodes.OK:
            s.close()
            return True
        else:
            s.close()
            return False

    def close(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            console.debug("Socket successfully created")
        except socket.error as err:
            console.error("socket creation failed with error {}".format(err))

        s.connect((settings.GARAGE_DOOR_IP_ADDRESS, settings.GARAGE_DOOR_PORT))

        console.debug("the socket has successfully connected to {}".format(settings.GARAGE_DOOR_IP_ADDRESS))

        data = self.build(cmd=1)

        s.send(data)

        console.debug(data.decode('utf-8'))

        console.debug("Successfully sent message")

        resp = Response(raw=s.recv(4096))

        if resp.status == HTTPResponseCodes.OK:
            s.close()
            return True
        else:
            s.close()
            return False

    @staticmethod
    def build(method='POST', path='/garage/door/ras_pi', cmd=None):
        method = method
        path = path
        data = dict()
        data['key'] = settings.MASTER_KEY
        if cmd is None:
            data['command'] = 0
        else:
            data['command'] = cmd

        return (method + ' ' + path + '\r\n\r\n' + json.dumps(data)).encode()
