import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), 'Hash'))
import Hash


FILEPATH = 'data/passwd.json'

if __name__ == "__main__":

    login = sys.argv[1]
    passwd = sys.argv[2]

    if Hash.register_user(login,passwd, FILEPATH):
        print("Pomyślnie zarejestrowano użytkownika: ", Hash.get_user(login, FILEPATH)['login'])