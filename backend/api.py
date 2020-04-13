import json


def teamx(fn, request, data=None):
    if fn == '/':
        return login(request, data)
    else:
        return ''.encode(), 500, -1


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
        data = data.decode('utf-8').replace("'", '"')
        print(data)
        data = json.dumps(data)
        print(data)
        data = json.loads(data)[0]
        print(data)

