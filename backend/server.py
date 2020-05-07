import socket
from http_x.request_x import Request
from http_x.api_x import API
import console as console
from multiprocessing import Process, Lock
from threading import Thread
from database.db import DataBase
import settings
from os.path import join


class Server:
    def __init__(self, host_ip=None, hostname=None, port=None, project=None):
        # self.live = Thread(target=self.stream)
        self.socket = socket.socket()
        self.db = DataBase(settings.DATABASE_FP)
        if host_ip is None:
            host_ip = socket.gethostbyname(socket.gethostname())
            # host = '192.168.1.176'
        self.host_ip = host_ip
        if hostname is None:
            hostname = self.host_ip
        self.hostname = hostname
        if port is None:
            port = 80
        self.port = port
        if project is None:
            project = '..'
        self.project = project
        self.db_lock = Lock()
        self.api = API(self.db, self.db_lock, self.hostname, self.port)
        self.socket.bind((self.host_ip, self.port))
        self.socket.listen(5)
        # self.live.start()

    def stream(self):
        ctr = 0
        s = socket.socket()
        s.bind((self.host_ip, settings.STREAM_PORT))
        s.listen(5)
        while True:
            c, a = s.accept()
            data = c.recv()
            with open(join(settings.STREAM_DIR, str(ctr) + '.jpg'), 'wb+') as f:
                f.write(data)
            if ctr < 5:
                ctr += 1
            else:
                ctr = 0
            c.close()

    def run(self):
        request_queue = list()
        idx = 0
        while True:
            client, address = self.socket.accept()
            request_queue.append(Process(target=self.communicate, args=(client, address, client.recv(4096))))
            request_queue[idx].start()
            idx += 1

    def communicate(self, client, address, msg):
        req = Request(msg=msg)

        console.info(
            'Received {} request from {} at {} with {} parameters'.format(req.method.name, address[0], req.path,
                                                                          0 if req.params is None else len(
                                                                              req.params.keys())))

        resp = self.api.route(req)

        console.info('Sent {} {} response'.format(resp.status.value, resp.status.name.replace('_', ' ')))

        client.send(self.api.route(req).generate())

        client.close()
