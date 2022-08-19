import hashlib
import json
import os
import random
import string

SALT_LEN = 8

def get_user(login, filepath):
    with open(filepath, "r") as passwd_file:
        data = json.load(passwd_file)
        for user in data["users"]:
            if user["login"] == login:
                return user
        return {}


def is_password_correct(login, password, filepath):
    user = get_user(login, filepath)
    h = hashlib.sha384()
    
    if user:
        h.update(password.encode())
        h.update(user['salt'].encode())

    try:
        return h.hexdigest() == user['password']
    except KeyError:
        return False


def register_user(login, password, filepath):
    data = {}
    with open(filepath, "r") as passwd_file:
        data = json.load(passwd_file)

    for user in data['users']:
        if user['login'] == login:
            return False

    salt = ''.join(random.choices(string.ascii_uppercase + string.digits, k=SALT_LEN))
    h = hashlib.sha384()
    h.update(password.encode())
    h.update(salt.encode())

    data['users'].append(
        {'login': login, 'password': h.hexdigest(), 'salt': salt})

    with open(filepath, "w") as passwd_file:
        json.dump(data, passwd_file)
    return True
