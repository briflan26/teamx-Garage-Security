import socket
import time
import os
from api import teamx


class Server:
    def __init__(self, host='localhost', port=8000, static='..', api=None):
        if api is None:
            self.api = self.default_api
        else:
            self.api = api
        self.socket = socket.socket()
        self.host = host
        self.port = port
        self.static = static
        self.socket.bind((host, port))

    def run(self):
        self.socket.listen(5)
        while True:
            csocket, address = self.socket.accept()
            response = self.process(csocket, address)
            csocket.send(response)
            csocket.close()


    @staticmethod
    def request_type(msg):
        if msg[0:3] == 'GET'.encode():
            return 0
        elif msg[0:4] == 'POST'.encode():
            return 1
        else:
            return -1

    @staticmethod
    def get_fn(msg, request=0):
        fn = ''
        regex = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890/-.'
        if request == 0:
            start = 4
        elif request == 1:
            start = 5
        else:
            return -1

        for c in msg[start:].decode('utf-8'):
            if c not in regex:
                break
            fn += c

        if fn[-4:] == 'html':
            # fn = 'html/' + fn
            t = 0
        elif fn[-3:] == 'css':
            # fn = 'css/' + fn
            t = 1
        elif fn[-2:] == 'js':
            # fn = 'js/' + fn
            t = 2
        else:
            t = 3

        return fn, t

    @staticmethod
    def response_header(status=200, type=-1, length=4096):
        response = 'HTTP/1.0 '
        date = 'Date: {}\r\n'.format(time.ctime())
        if type == 0:
            ctype = 'Content-Type: text/html\r\n'
        elif type == 1:
            ctype = 'Content-Type: text/css\r\n'
        elif type == 2:
            ctype = 'Content-Type: application/javascript\r\n'
        elif type == 3:
            ctype = 'Content-Type: application/json\r\n'
        else:
            ctype = 'Content-Type: text/plain\r\n'

        clen = 'Content-Length: {}\r\n\r\n'.format(length)

        if status == 200:
            response += '200 OK\r\n'
        elif status == 400:
            response += '400 BAD REQUEST\r\n'
        elif status == 404:
            response += '404 NOT FOUND\r\n'
        elif status == 403:
            response += '403 UNAUTHORIZED\r\n'
        else:
            response += '500 SERVER ERROR\r\n'
        response += date
        response += ctype
        response += clen
        print(response)
        return response.encode()

    @staticmethod
    def get_data(msg):
        d = ''
        p = [None, None, None]
        flag = False
        for c in msg.decode('utf-8'):
            if flag:
                d += c
            else:
                if c == '\n' and p[0] == '\r' and p[1] == '\n' and p[2] == '\r':
                    flag = True
                else:
                    p[0] = p[1]
                    p[1] = p[2]
                    p[2] = c

        print(d)
        return d

    @staticmethod
    def default_api(fn, request):
        print("Default api call")
        return ''.encode(), 500, -1

    def process(self, c, a):
        msg = c.recv(4096)
        print(msg)
        if self.request_type(msg) == 0:  # GET
            fn, ft = self.get_fn(msg, 0)

            print("file name: " + fn)
            print("file type: " + str(ft))

            if ft == 3:
                r, s, t = self.api(fn, 0)
                response = self.response_header(status=s, type=t)
                response += r
            else:
                try:
                    with open(self.static + fn, 'rb') as f:
                        f.seek(0, os.SEEK_END)
                        size = f.tell()
                        response = self.response_header(type=ft, length=size)
                        f.seek(0)
                        response += f.read(size)
                except FileNotFoundError as e:
                    print(e)
                    response = self.response_header(status=404, length=0)
        elif self.request_type(msg) == 1:  # POST
            data = self.get_data(msg)
            fn, ft = self.get_fn(msg, 1)
            print("file name: " + fn)
            print("file type: " + str(ft))

            if ft == 3:
                r, s, t = self.api(fn, 1, data)
                response = self.response_header(status=s, type=t)
                response += r
            else:
                response = self.response_header(status=403, length=0)

        else:
            print("PROCESSING OTHER REQUEST")
            response = 'FAILURE'.encode()

        return response


if __name__ == "__main__":
    s = Server(api=teamx)
    print("Starting server...")
    s.run()
