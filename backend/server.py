import socket
from request import Request
from api import API
import console


class Server:
    def __init__(self, host=None, port=None, project=None):
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
        self.api = API(self.host, self.port)
        self.socket.bind((host, port))
        self.socket.listen(5)

    def run(self):
        # TODO add multi-threading here
        while True:
            client, address = self.socket.accept()
            client.send(self.communicate(client))
            client.close()

    def communicate(self, client):
        req = Request(msg=client.recv(4096))

        console.info('Received {} request at {} with {} parameters'.format(req.method.name, req.path,
                                                                           0 if req.params is None else len(
                                                                               req.params.keys())))

        resp = self.api.route(req)

        console.info('Sent {} {} response'.format(resp.status.value, resp.status.name.replace('_', ' ')))

        return self.api.route(req).generate()
