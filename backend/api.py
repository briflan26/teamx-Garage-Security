import json


def teamx(fn, request, data=None):
    if fn == '/':
        return login(request, data)
    elif fn == '/login':
        return login(request, data)
    else:
        return ''.encode(), 404, -1


def load(path, size=4096):
    try:
        with open(path, 'rb') as f:
            data = f.read(size)
        return data
    except FileNotFoundError as e:
        print(e)
        return None


def login(request, data=None):
    print("LOGIN PAGE")
    if request == 0:  # GET
        path = '../static/html/login.html'
        data = load(path)
        if data is not None:
            return data, 200, 0
        else:
            return ''.encode(), 500, -1
    elif request == 1:  # POST
        if data is None:
            return ''.encode(), 400, -1
        print(data)
        d = json.loads(data)
        print('email: ' + d['email'])
        print('password: ' + d['password'])

        return 'Successful login!'.encode(), 200, -1


