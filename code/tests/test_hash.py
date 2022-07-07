import unittest
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Hash'))
import Hash
import json
import hashlib
import pdb 


JSON_FILE = 'code/tests/passwd_temp.json'

sample_json = {
    "users": [
        {   
            "login" : "admin",
            "password" : '527badaab4dabd41d2ae385ef1e9910c4ba4038477c76fb36a04b79f08d9f4d056c2e34a15d8e4d82f94fe0192b35a19',
            "salt" : "1234"
        }
    ]
}


def initialize_test_file(input_data):
    with open(JSON_FILE, 'w') as outfile:
            json.dump(input_data, outfile)


class TestHash(unittest.TestCase):

    def test_get_user(self):
        initialize_test_file(sample_json)
        expected_user = sample_json['users'][0]
        result_user = Hash.get_user('admin',JSON_FILE)
        self.assertEqual(expected_user,result_user)

    def test_get_user2(self):
        test_password = 'nimda'
        result_user = Hash.get_user('admin',JSON_FILE)
        salt = result_user['salt']

        salted_password = test_password+salt
        h = hashlib.sha384()
        
        h.update(salted_password.encode())
        self.assertEqual(result_user['password'], h.hexdigest())
        

    def test_password_correct(self):
        self.assertTrue(Hash.is_password_correct('admin', 'nimda', JSON_FILE))

    def test_register_user_rep(self):
        # initialize_test_file(sample_json)

        self.assertFalse(Hash.register_user('admin', 'password', JSON_FILE))

       
    def test_register_user(self):
        data = {}
        # initialize_test_file(sample_json)
        Hash.register_user("Balbinka", "balbinkahaslo", JSON_FILE)

        with open(JSON_FILE,"r") as passwd_file:
            data = json.load(passwd_file)

        
        self.assertEqual(len(data['users']), 2)
        
    

if __name__ == '__main__':
    unittest.main()