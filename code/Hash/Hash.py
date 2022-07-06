import hashlib
import json 
import os
PASSWD_FILE = "./data/passwd.json"



def get_user(login, filepath):
    with open(filepath,"r") as passwd_file:
        data = json.load(passwd_file)
        for user in data["users"]:
            if user["login"] == login:
                return user

def is_password_correct(login,password, filepath): 
    user = get_user(login,filepath)
    salted_password = password+user['salt']
    h = hashlib.sha384()
    h.update(salted_password.encode())
    return h.hexdigest() == user['password']

def register_user(login, password, filepath):
    data = {}
    with open(filepath,"r") as passwd_file:
        data = json.load(passwd_file)
    
    for user in data['users']:
        if user['login'] == login:
            return False

    salt = os.urandom(8)
    salted_password = password + salt
    h = hashlib.sha384()
    h.update(salted_password.encode())
    h.update(salt)

    data['users'].append({'login' : login, 'password' : h.hexdigest(), 'salt' : salt })   
    
    with open(filepath,"w") as passwd_file:
        json.dump(data, passwd_file)
    return True

