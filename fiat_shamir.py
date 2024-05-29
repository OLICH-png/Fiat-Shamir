import hashlib
import json
import os

class FiatShamirAuth:
    def __init__(self, filename='users.json'):
        self.filename = filename
        self.p = 23  # Пример простого числа p
        self.q = 11  # Пример простого числа q
        self.n = self.p * self.q  # n является частью открытого ключа
        self.load_users()

    def load_users(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                self.users = json.load(file)
        else:
            self.users = {}

    def save_users(self):
        with open(self.filename, 'w') as file:
            json.dump(self.users, file)

    def register(self, username, password):
        if username in self.users:
            raise ValueError("User already exists")
        s = int(hashlib.sha256(password.encode()).hexdigest(), 16) % self.n
        v = pow(s, 2, self.n)
        self.users[username] = {'s': s, 'v': v, 'password': hashlib.sha256(password.encode()).hexdigest()}
        self.save_users()

    def start_auth(self, username, password):
        if username in self.users and self.users[username]['password'] == hashlib.sha256(password.encode()).hexdigest():
            return True
        return False

    def get_v(self, username):
        return self.users[username]['v']

    def verify(self, username, y, e):
        s = self.users[username]['s']
        v = self.users[username]['v']
        if e == 0:
            return pow(y, 2, self.n) == pow(y, 2, self.n)
        elif e == 1:
            return (pow(y, 2, self.n) * v) % self.n == pow(y * s, 2, self.n)
        return False
