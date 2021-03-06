import console
import json
import uuid
import time
from os.path import join, dirname, abspath


class DataBase:
    def __init__(self, fn):
        self.fn = fn
        try:
            with open(self.fn, 'r') as f:
                db = json.load(f)
                self.users = db['users']
                self.alerts = db['alerts']
        except FileNotFoundError as e:
            console.error('Unable to open database file')
            exit(1)

    def write(self):
        try:
            with open(self.fn, 'w') as f:
                json.dump({'users': self.users, 'alerts': self.alerts}, f, indent=4)
        except FileNotFoundError as e:
            console.error('Unable to open database file')
            exit(1)

    def read(self):
        try:
            with open(self.fn, 'r') as f:
                db = json.load(f)
                self.users = db['users']
                self.alerts = db['alerts']
        except FileNotFoundError as e:
            console.error('Unable to open database file')
            exit(1)

    def alert(self, epoch, timestamp, message):
        self.read()
        if epoch not in self.alerts.keys():
            self.alerts[epoch] = {'time': timestamp, 'message': message}
            self.write()

    def get_alerts(self, t):
        self.read()
        a = dict()
        if len(self.alerts.keys()) > 0:
            for k, v in self.alerts.items():
                if int(k) > t:
                    a[k] = self.alerts[k]
        return a

    def login(self, email, password):
        self.read()
        if email in self.users.keys() and password == self.users[email]['password']:
            # session = os.urandom(32)
            session = str(uuid.uuid4())
            self.users[email]['session'] = {'key': session, 'time': time.time()}
            console.debug('User Database (w/sessions): {}'.format(self.users[email]))
            self.write()
            return session
        else:
            return None

    def logout(self, email, key):
        self.read()
        if email in self.users.keys() and 'session' in self.users[email].keys() and key == self.users[email]['session'][
            'key'] and (time.time() - self.users[email]['session']['time']) < 3600:
            del self.users[email]['session']
            self.write()
            return True
        else:
            return False

    def check_session(self, email, key):
        self.read()
        if email in self.users.keys() and 'session' in self.users[email].keys() and key == self.users[email]['session'][
            'key'] and (time.time() - self.users[email]['session']['time']) < 3600:
            self.users[email]['session']['time'] = time.time()
            self.write()
            return True
        else:
            return False

    def check_access(self, email, key):
        self.read()
        if self.check_session(email, key):
            return self.users[email]['access']
        else:
            return None
