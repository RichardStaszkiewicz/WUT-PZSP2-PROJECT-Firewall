
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
        
        with open('unittest.json', 'w') as outfile:
            json.dump(self.sample_rule, outfile)

        with open('unittest.json', 'r') as infile:
            expected = json.load(infile)
        fire = Fire.Fire("unittest.json")

        print(fire.get_rules())
        self.assertEqual(fire.get_rules()[0], expected["rules"][0])


    def test_analyze_modbus_message_accept(self):
        print("MODBUS ACCEPT")
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






#     def test_analyze_slmp_packet_accept(self):
#         with open('unittest.json', 'w') as outfile:
#             json.dump(self.sample_slmp_rule, outfile)
#         fire = Fire.Fire("unittest.json")
#  # 0x50 0x0  - subheader 
#     # 0x0 0xff - request dest net/station 
#     # 0xff 0x3 - request destination module
#     # 0x0 - request destination multidrop No. 
#     # 0xc 0x0 - request data length 12 bytes             12-14 bytes
#     # 0x4 0x0 - monitoring timer
#     # ^^^ 22 BYTES 
#     # 
#     #   0x1 0x4                0x0 0x0         0x32 0x0               0x0 0xa8              0x1 0x0                 12 BYTES TOTAL, CORRECT LEN
#     # |22-26 READ|   | 26-30 READ IN WORDS|    | HEAD DEV NO.|      | DEV CODE const |    | NO OF DEV POINTS |        

#         pre_payload = [b'0x50', b'0x0'] #0x0 0xff 0xff 0x3 0x0 0xc 0x0 0x4 0x0' 
#         command = [b'0x4', b'0x1']
#         subcommand = [b'0x0',  b'0x0']
#         head_dev_no = [b'0x32', b'0x0']
#         dev_code = [b'0x0', b'0xa8']
#         dev_pts_no = [b'0x1', b'0x0']


#         payload = pre_payload + command + subcommand + head_dev_no + dev_code + dev_pts_no
#         # payload = bytes(message_frame)

#         self.assertFalse(fire.analyze_slmp_message(payload))


    def test_compare_ip_tcp_with_rules(self):
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

        with open('unittest.json', 'w') as outfile:
            json.dump(tcp_rule, outfile)
        fire = Fire.Fire("unittest.json")

        attributes = {
            "source address": "127.0.0.1",
            "destination address": "127.0.0.2",
            "protocol": "TCP",
            "sport": "1234",  # ANY
            "dport": "5020"
        }
        fire = Fire.Fire("unittest.json")
        self.assertFalse(fire.compare_with_rules(attributes))

    def test_compare_modbus_with_rules(self):
        modbus_rule = {
            "rules": [
                {
                    "id": 11,
                    "name": "Allow all writes on register 9",
                    "direction": "IN",
                    "protocol": "MODBUS",
                    "command": "Write Single Register",
                    "starting address": "ANY",
                    "quantity": "ANY",
                    "register": "9"
                }
            ]
        }

        with open('unittest.json', 'w') as outfile:
            json.dump(modbus_rule, outfile)
        fire = Fire.Fire("unittest.json")

        attributes = {
            "protocol": "MODBUS",
            "command": "Write Single Register",
            "starting address": "0",
            "quantity": "50"
        }

        fire = Fire.Fire("unittest.json")
        self.assertFalse(fire.compare_with_rules(attributes))


if __name__ == '__main__':
    unittest.main()
