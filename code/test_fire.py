import unittest

from attr import attributes
import Fire
import json

class TestFire(unittest.TestCase):

    sample_rule = {
    "rules": [
        {
            "id": 101,
            "name": "Wszystkie multiple read readujące mniej niż 100",
            "direction": "IN",
            "protocol": "MODBUS",
            "Command": "Device Read Mutiple Registers",
            "Start Register": "Any",
            "Quantity": 100,
            "Comparison": "MAX"
        },
        {
            "id": 5,
            "name": "Accept MODBUS TCP from 127.0.0.1 to 127.0.0.2",
            "profile": 0,
            "direction": "IN",
            "protocol": "TCP",
            "source address": "127.0.0.1",
            "destination address": "127.0.0.2",
            "sport": "ANY",
            "dport": "5020"
        }
    ]
}


    def test_single_rule(self):
        with open('unittest.json', 'w') as outfile:
            json.dump(self.sample_rule, outfile)

        with open('unittest.json', 'r') as infile:    
            expected = json.load(infile)
        fire = Fire.Fire("unittest.json")
        
        print(fire.get_rules())
        self.assertEqual(fire.get_rules()[0],expected["rules"][0])

    def test_empty_rule(self):
        pass

    def test_multiple_rules(self):
        pass



    def test_compare_ip_tcp_with_rules(self):
        tcp_rule ={
            "id": 5,
            "name": "Accept MODBUS TCP from 127.0.0.1 to 127.0.0.2",
            "profile": 0,
            "direction": "IN",
            "protocol": "TCP",
            "source address": "127.0.0.1",
            "destination address": "127.0.0.2",
            "sport": "ANY",
            "dport": "5020"
        }
        with open('unittest.json', 'w') as outfile:
            json.dump(tcp_rule, outfile)
        fire = Fire.Fire("unittest.json")

        attributes = {
            "source address": "127.0.0.1",
            "destination address": "127.0.0.2",
            "protocol": "TCP",
            "sport": "1234", # ANY
            "dport": "5020"
        }
        fire = Fire.Fire("unittest.json")
        self.assertTrue(fire.compare_with_rules(attributes))


    def compare_modbus_with_rules(self):
        modbus_rule ={
            "id": 11,
            "name": "Allow all writes on register 9",
            "direction": "IN",
            "protocol": "MODBUS",
            "command": "Write Single Register",
            "starting address": "ANY",
            "quantity": "ANY",
            "register": "9"
        }
        with open('unittest.json', 'w') as outfile:
            json.dump(self.sample_rule, outfile)
        fire = Fire.Fire("unittest.json")

        attributes = {
            "protocol": "MODBUS",
            "command": "Write Single Register",
            "starting address": "0",
            "quantity" : "50"
        }

        fire = Fire.Fire("unittest.json")
        self.assertTrue(fire.compare_with_rules(attributes))

    

if __name__ == '__main__':

    unittest.main()

