import socket
from request import Request
from api import API


class Server:
    def __init__(self, host=None, port=None, project=None):
        self.api = API()
        self.socket = socket.socket()
        if host is None:
            host = socket.gethostname()
        self.host = host
        if port is None:
            port = 8000
        self.port = port
        if project is None:
            project = '..'
        self.project = project
        self.socket.bind((host, port))
        self.socket.listen(5)

    def run(self):
        # TODO add multi-threading here
        while True:
            csocket, address = self.socket.accept()
            csocket.send(self.receive(csocket))
            csocket.close()

    def receive(self, client):
        req = Request(msg=client.recv(4096))

        print('[INFO] Received {} request at {}'.format(req.method.name, req.path))

        return self.api.route(req)
