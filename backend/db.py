import json
# import os
import uuid
import time


class DataBase:
    def __init__(self, fn):
        try:
            with open(fn, 'r') as f:
                self.users = json.load(f)
        except FileNotFoundError as e:
            print('[ERROR] Unable to open database file')
            exit(1)

    def login(self, email, password):
        if email in self.users.keys() and password == self.users[email]['password']:
            # session = os.urandom(32)
            session = str(uuid.uuid4())
            self.users[email]['session'] = {'key': session, 'time': time.time()}
            return session
        else:
            return None

    def check_session(self, email, key):
        if email in self.users.keys() and key == self.users[email]['session']['key'] and (
                time.time() - self.users[email]['session']['time']) < 3600:
            self.users[email]['session']['time'] = time.time()
            return True
        else:
            return False

    def check_access(self, email, key):
        if self.check_session(email, key):
            return self.users[email]['access']
        else:
            return None
