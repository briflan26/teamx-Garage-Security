import socket
import sys
import time
import json


def build(method='POST', path='/security/camera/alert', msg=None):
    method = method
    path = path
    data = dict()
    data['time'] = time.ctime()
    data['epoch'] = int(time.time() * 1000)
    if msg is None:
        data['message'] = 'Motion Detected'
    else:
        data['message'] = msg

    return (method + ' ' + path + '\r\n\r\n' + json.dumps(data)).encode()


def alert(host_ip=None, hostname=None, port=None, data=None):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket successfully created")
    except socket.error as err:
        print("socket creation failed with error {}".format(err))

    if host_ip is None:
        if hostname is None:
            print("Error: Need to include either a hostname or host ip")
            sys.exit()
        else:
            try:
                host_ip = socket.gethostbyname(hostname)
            except socket.gaierror:
                # this means could not resolve the host
                print("there was an error resolving the host")
                sys.exit()
    if port is None:
        port = 80

    s.connect((host_ip, port))

    print("the socket has successfully connected to {}".format(host_ip))

    if data is None:
        data = build()

    s.send(data)

    s.close()


def main():
    alert(host_ip='192.168.0.190')


if __name__ == '__main__':
    main()
