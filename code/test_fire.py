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
                    "register": "9"
                },
                {
                    "id": 2,
                    "name": "Wszystkie multiple read readujące mniej niż 100",
                    "direction": "IN",
                    "protocol": "MODBUS",
                    "command": "Read Holding Registers",
                    "starting address": "ANY",
                    "quantity": "5",
                    "comparison": "MAX"
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
        self.assertEqual(fire.get_rules()[0], expected["rules"][0])

    def test_empty_rule(self):
        pass

    def test_multiple_rules(self):
        pass

    def test_analyze_modbus_message_accept(self):
        with open('unittest.json', 'w') as outfile:
            json.dump(self.sample_modbus_rules, outfile)

        fire = Fire.Fire("unittest.json")

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

    def test_analyze_modbus_message_drop(self):
        with open('unittest.json', 'w') as outfile:
            json.dump(self.sample_modbus_rules, outfile)

        fire = Fire.Fire("unittest.json")

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
        with open('unittest.json', 'w') as outfile:
            json.dump(self.sample_modbus_rules, outfile)

        fire = Fire.Fire("unittest.json")

        message_frame = []

        payload = bytes(message_frame)
        self.assertFalse(fire.analyze_modbus_message(payload))




if __name__ == '__main__':
    unittest.main()
