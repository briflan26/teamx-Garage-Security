import console
import json
import uuid
import time


class DataBase:
    def __init__(self, fn):
        self.fn = fn
        try:
            with open(fn, 'r') as f:
                self.users = json.load(f)
        except FileNotFoundError as e:
            console.error('Unable to open database file')
            exit(1)

    def write(self):
        try:
            with open(self.fn, 'w') as f:
                json.dump(self.users, f, indent=4)
        except FileNotFoundError as e:
            console.error('Unable to open database file')
            exit(1)

    def read(self):
        try:
            with open(self.fn, 'r') as f:
                self.users = json.load(f)
        except FileNotFoundError as e:
            console.error('Unable to open database file')
            exit(1)

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

