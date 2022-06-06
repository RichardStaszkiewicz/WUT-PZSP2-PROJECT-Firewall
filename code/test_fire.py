
import unittest
import Fire
import json


class TestFire(unittest.TestCase):

    sample_rule = {
        "rules":
            [
                {
                    "id": 101,
                    "name": "Wszystkie multiple read readujące mniej niż 100",
                    "direction": "IN",
                    "protocol": "MODBUS",
                    "Command": "Device Read Mutiple Registers",
                    "Start Register": "Any",
                    "Quantity": 100,
                    "Comparison": "MAX"
                }
            ]
    }

    sample_modbus_rules = {
        "rules":
            [
                {
                    "id": 1,
                    "name": "Allow all writes on register 9",
                    "direction": "IN",
                    "protocol": "MODBUS",
                    "command": "Write Single Register",
                    "starting address": "ANY",
                    "quantity": "ANY",
                },
                {
                    "id": 2,
                    "name": "Wszystkie multiple read readujące mniej niż 100",
                    "direction": "IN",
                    "protocol": "MODBUS",
                    "command": "Read Holding Registers",
                    "starting address": "ANY",
                    "quantity": "4",
                    "comparison": "MAX"
                }
            ]
        }

    sample_slmp_rule = {
        "rules":
            [
                {
                    "id": 1,
                    "name": "Accept All",
                    "profile": 0,
                    "direction": "IN",
                    "protocol": "SLMP",
                    "Command": "Read",
                    "Head Device": "ANY",

                }
            ]
        }



    def test_single_rule(self):

        with open('../data/unittest.json', 'w') as outfile:
            json.dump(self.sample_rule, outfile)

        with open('../data/unittest.json', 'r') as infile:
            expected = json.load(infile)
        fire = Fire.Fire("../data/unittest.json")

        print(fire.get_rules())
        self.assertEqual(fire.get_rules()[0], expected["rules"][0])


    def test_analyze_modbus_message_accept(self):
        print("MODBUS ACCEPT")
        with open('../data/unittest.json', 'w') as outfile:
            json.dump(self.sample_modbus_rules, outfile)

        fire = Fire.Fire("../data/unittest.json")

        transaction_id = [0, 1]
        protocol_identifier = [0, 0]
        next_bytes = [0, 6]
        device_address = [0]
        function_code = [3]
        starting_register = [0, 0]
        quantity = [0, 4]

        message_frame = transaction_id + protocol_identifier + next_bytes + device_address + \
                        function_code + starting_register + quantity

        payload = bytes(message_frame)
        self.assertFalse(fire.analyze_modbus_message(payload))

    def test_analyze_modbus_message_reject(self):
        with open('../data/unittest.json', 'w') as outfile:
            json.dump(self.sample_modbus_rules, outfile)

        fire = Fire.Fire("../data/unittest.json")

        transaction_id = [0, 1]
        protocol_identifier = [0, 0]
        next_bytes = [0, 6]
        device_address = [0]
        function_code = [4]
        starting_register = [0, 0]
        quantity = [0, 4]

        message_frame = transaction_id + protocol_identifier + next_bytes + device_address + \
                        function_code + starting_register + quantity

        payload = bytes(message_frame)
        self.assertTrue(fire.analyze_modbus_message(payload))


    def test_analyze_modbus_packet_with_no_message_accept(self):
        with open('../data/unittest.json', 'w') as outfile:
            json.dump(self.sample_modbus_rules, outfile)

        fire = Fire.Fire("../data/unittest.json")

        message_frame = []

        payload = bytes(message_frame)
        self.assertFalse(fire.analyze_modbus_message(payload))



    def test_compare_ip_tcp_with_rules_accept(self):
        tcp_rule = {
            "rules": [
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

        with open('../data/unittest.json', 'w') as outfile:
            json.dump(tcp_rule, outfile)

        attributes = {
            "source address": "127.0.0.1",
            "destination address": "127.0.0.2",
            "protocol": "TCP",
            "sport": "1234",  # ANY
            "dport": "5020"
        }
        fire = Fire.Fire("../data/unittest.json")
        self.assertFalse(fire.compare_with_rules(attributes))


    def test_compare_ip_tcp_with_rules_reject_1(self):
        tcp_rule = {
            "rules": [
                {
                    "id": 5,
                    "name": "Accept MODBUS TCP from 127.0.0.1 to 127.0.0.1",
                    "profile": 0,
                    "direction": "IN",
                    "protocol": "TCP",
                    "source address": "127.0.0.1",
                    "destination address": "127.0.0.1",
                    "sport": "ANY",
                    "dport": "5020"
                }
            ]
        }

        with open('../data/unittest.json', 'w') as outfile:
            json.dump(tcp_rule, outfile)

        attributes = {
            "source address": "127.0.0.1",
            "destination address": "127.0.0.2",
            "protocol": "TCP",
            "sport": "1234",  # ANY
            "dport": "5020"
        }
        fire = Fire.Fire("../data/unittest.json")
        self.assertTrue(fire.compare_with_rules(attributes))


    def test_compare_ip_tcp_with_rules_accept_2(self):
        tcp_rule = {
            "rules": [
                {
                    "id": 5,
                    "name": "Accept any 127.0.0.1 traffic",
                    "profile": 0,
                    "direction": "IN",
                    "protocol": "TCP",
                    "source address": "127.0.0.1",
                    "destination address": "127.0.0.1",
                    "sport": "ANY",
                    "dport": "ANY"
                }
            ]
        }

        with open('../data/unittest.json', 'w') as outfile:
            json.dump(tcp_rule, outfile)

        attributes = {
            "source address": "127.0.0.1",
            "destination address": "127.0.0.1",
            "protocol": "TCP",
            "sport": "1234",  # ANY
            "dport": "5555"   # ANY
        }
        fire = Fire.Fire("../data/unittest.json")
        self.assertFalse(fire.compare_with_rules(attributes))


    def test_compare_ip_tcp_with_rules_reject_2(self):
        tcp_rule = {
            "rules": [
                {
                    "id": 5,
                    "name": "Accept MODBUS TCP from 127.0.0.1 to 127.0.0.2",
                    "profile": 0,
                    "direction": "IN",
                    "protocol": "UDP",
                    "source address": "127.0.0.1",
                    "destination address": "127.0.0.2",
                    "sport": "ANY",
                    "dport": "5020"
                }
            ]
        }

        with open('../data/unittest.json', 'w') as outfile:
            json.dump(tcp_rule, outfile)

        attributes = {
            "source address": "127.0.0.1",
            "destination address": "127.0.0.2",
            "protocol": "TCP",
            "sport": "1234",  # ANY
            "dport": "5020"
        }
        fire = Fire.Fire("../data/unittest.json")
        self.assertTrue(fire.compare_with_rules(attributes))


    def test_compare_modbus_with_rules_accept(self):
        modbus_rule = {
            "rules": [
                {
                    "id": 11,
                    "name": "Allow all writes on all registers",
                    "direction": "IN",
                    "protocol": "MODBUS",
                    "command": "Write Single Register",
                    "starting address": "ANY",
                    "quantity": "ANY",
                }
            ]
        }

        with open('../data/unittest.json', 'w') as outfile:
            json.dump(modbus_rule, outfile)

        attributes = {
            "protocol": "MODBUS",
            "command": "Write Single Register",
            "starting address": "0",
            "quantity": "50"
        }

        fire = Fire.Fire("../data/unittest.json")
        self.assertFalse(fire.compare_with_rules(attributes))


    def test_compare_modbus_with_rules_reject_1(self):
        modbus_rule = {
            "rules": [
                {
                    "id": 11,
                    "name": "Allow all reads on all registers",
                    "direction": "IN",
                    "protocol": "MODBUS",
                    "command": "Read Single Register",
                    "starting address": "ANY",
                    "quantity": "ANY",
                }
            ]
        }

        with open('../data/unittest.json', 'w') as outfile:
            json.dump(modbus_rule, outfile)

        attributes = {
            "protocol": "MODBUS",
            "command": "Write Single Register",
            "starting address": "0",
            "quantity": "50"
        }

        fire = Fire.Fire("../data/unittest.json")
        self.assertTrue(fire.compare_with_rules(attributes))

        def test_compare_modbus_with_rules_reject_2(self):
            modbus_rule = {
                "rules": [
                    {
                        "id": 11,
                        "name": "Allow all writes on register 9",
                        "direction": "IN",
                        "protocol": "MODBUS",
                        "command": "Write Single Register",
                        "starting address": "51",
                        "quantity": "ANY",
                    }
                ]
            }

            with open('../data/unittest.json', 'w') as outfile:
                json.dump(modbus_rule, outfile)

            attributes = {
                "protocol": "MODBUS",
                "command": "Write Single Register",
                "starting address": "0",
                "quantity": "50"
            }

            fire = Fire.Fire("../data/unittest.json")
            self.assertTrue(fire.compare_with_rules(attributes))


if __name__ == '__main__':
    unittest.main()
