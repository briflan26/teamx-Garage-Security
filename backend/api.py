import json
import os


def teamx(fn, request, data=None):
    if fn == '/':
        return login(request, data)
    elif fn == '/login':
        return login(request, data)
    elif fn == '/home':
        return home(request, data)
    else:
        return ''.encode(), 404, -1, 0


def load(path):
    try:
        size = os.stat(path).st_size
        with open(path, 'rb') as f:
            data = f.read(size)
        return data, size
    except FileNotFoundError as e:
        print(e)
        return None


def login(request, data=None):
    print("LOGIN PAGE")
    if request == 0:  # GET
        path = '../static/html/login.html'
        data, size = load(path)
        if data is not None:
            return data, 200, 0, size
        else:
            return ''.encode(), 500, -1, 0
    elif request == 1:  # POST
        home_path = '../static/html/home.html'
        if data is None:
            return ''.encode(), 400, -1, 0
        print(data)
        d = json.loads(data)
        print('email: ' + d['email'])
        print('password: ' + d['password'])
        data, size = load(home_path)
        return data, 200, -1, size


def home(request, data=None):
    print("HOME PAGE")
    if request == 0:  # GET
        path = '../static/html/home.html'
        data, size = load(path)
        if data is not None:
            return data, 200, 0, size
        else:
            return ''.encode(), 500, -1, 0
