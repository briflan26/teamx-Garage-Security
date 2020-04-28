import socket
from request import Request
from api import API
import console as console
from multiprocessing import Process, Lock
from db import DataBase

import RPi.GPIO as GPIO
import timeGPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
print "LED on"
GPIO.output(18,GPIO.HIGH)
time.sleep(1)
print "LED off"
GPIO.output(18,GPIO.LOW)


class Server:
    def __init__(self, host_ip=None, hostname=None, port=None, project=None):
        self.socket = socket.socket()
        self.db = DataBase('db.json')
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

        #console.info('Sent {} {} response'.format(resp.status.value, resp.status.name.replace('_', ' ')))
        if req != 0:
            GPIO.output(18,GPIO.HIGH)
	    time.sleep(5)
	    GPIO.output(18,GPIO.LOW)

        #client.send(self.api.route(req).generate())
        #Do we want something sent to notify the request was received and confirm action was taken?
        client.close()
