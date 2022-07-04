import unittest
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Fire'))
import Fire
import json
import rules_bank
import scapy
JSON_FILE = 'code/tests/rules_temp.json'


class TestFire(unittest.TestCase):

    def test_single_rule(self):

        with open(JSON_FILE, 'w') as outfile:
            json.dump(rules_bank.tcp_rule, outfile)

        with open(JSON_FILE, 'r') as infile:
            expected = json.load(infile)
        fire = Fire.Fire(JSON_FILE)
        
        self.assertEqual(fire.get_rules()[0], expected["rules"][0])

    def test_slmp_write_accept(self):
        with open(JSON_FILE, 'w') as outfile:
            json.dump(rules_bank.slmp_write_rule, outfile)

        with open(JSON_FILE, 'r') as infile:
            expected = json.load(infile)
        fire = Fire.Fire(JSON_FILE)
        payload = b'\x50\x00\x00\xff\xff\x03\x00\x0e\x00\x04\x00\x01\x14\x00\x00\x0a\x00\x00\xa8\x01\x00\x14\x00'
        print(payload)
        self.assertFalse(fire.analyze_slmp_message(payload))
        
    def test_slmp_write_reject_upper(self):
        with open(JSON_FILE, 'w') as outfile:
            json.dump(rules_bank.slmp_write_rule, outfile)

        with open(JSON_FILE, 'r') as infile:
            expected = json.load(infile)
        fire = Fire.Fire(JSON_FILE)
        payload = b'\x50\x00\x00\xff\xff\x03\x00\x0e\x00\x04\x00\x01\x14\x00\x00\x0b\x00\x00\xa8\x01\x00\x14\x00'
        print(payload)
        self.assertTrue(fire.analyze_slmp_message(payload))

    def test_slmp_write_reject_lower(self):
        with open(JSON_FILE, 'w') as outfile:
            json.dump(rules_bank.slmp_write_rule, outfile)

        with open(JSON_FILE, 'r') as infile:
            expected = json.load(infile)
        fire = Fire.Fire(JSON_FILE)
        payload = b'\x50\x00\x00\xff\xff\x03\x00\x0e\x00\x04\x00\x01\x14\x00\x00\x01\x00\x00\xa8\x01\x00\x14\x00'
        print(payload)
        self.assertTrue(fire.analyze_slmp_message(payload))

           
        
    def test_slmp_read_accept(self):
        with open(JSON_FILE, 'w') as outfile:
            json.dump(rules_bank.slmp_read_rule, outfile)

        with open(JSON_FILE, 'r') as infile:
            expected = json.load(infile)
        
        fire = Fire.Fire(JSON_FILE)
        payload = b'\x50\x00\x00\xff\xff\x03\x00\x0e\x00\x04\x00\x01\x04\x00\x00\x05\x00\x00\xa8\x02\x00'
        self.assertFalse(fire.analyze_slmp_message(payload))


    def test_slmp_read_reject_upper(self):
        with open(JSON_FILE, 'w') as outfile:
            json.dump(rules_bank.slmp_read_rule, outfile)

        with open(JSON_FILE, 'r') as infile:
            expected = json.load(infile)
        
        fire = Fire.Fire(JSON_FILE)
        payload = b'\x50\x00\x00\xff\xff\x03\x00\x0e\x00\x04\x00\x01\x04\x00\x00\x0b\x00\x00\xa8\x0b\x00'
        self.assertTrue(fire.analyze_slmp_message(payload))

    

    def test_slmp_read_reject_upper_intersect(self):
        with open(JSON_FILE, 'w') as outfile:
            json.dump(rules_bank.slmp_read_rule, outfile)

        with open(JSON_FILE, 'r') as infile:
            expected = json.load(infile)
        
        fire = Fire.Fire(JSON_FILE)
        payload = b'\x50\x00\x00\xff\xff\x03\x00\x0e\x00\x04\x00\x01\x04\x00\x00\x09\x00\x00\xa8\x0b\x00'
        print('dupa')
        self.assertTrue(fire.analyze_slmp_message(payload))


    def test_slmp_read_reject_lower(self):
        with open(JSON_FILE, 'w') as outfile:
            json.dump(rules_bank.slmp_read_rule, outfile)

        with open(JSON_FILE, 'r') as infile:
            expected = json.load(infile)
        
        fire = Fire.Fire(JSON_FILE)
        payload = b'\x50\x00\x00\xff\xff\x03\x00\x0e\x00\x04\x00\x01\x04\x00\x00\x00\x00\x00\xa8\x04\x00'
        self.assertTrue(fire.analyze_slmp_message(payload))

    def test_slmp_read_reject_lower_intersect(self):
        with open(JSON_FILE, 'w') as outfile:
            json.dump(rules_bank.slmp_read_rule, outfile)

        with open(JSON_FILE, 'r') as infile:
            expected = json.load(infile)
        
        fire = Fire.Fire(JSON_FILE)
        payload = b'\x50\x00\x00\xff\xff\x03\x00\x0e\x00\x04\x00\x01\x04\x00\x00\x00\x00\x00\xa8\x06\x00'
        self.assertTrue(fire.analyze_slmp_message(payload))

    
    def test_slmp_read_reject_lower_upper_intersect(self):
        with open(JSON_FILE, 'w') as outfile:
            json.dump(rules_bank.slmp_read_rule, outfile)

        with open(JSON_FILE, 'r') as infile:
            expected = json.load(infile)
        
        fire = Fire.Fire(JSON_FILE)
        payload = b'\x50\x00\x00\xff\xff\x03\x00\x0e\x00\x04\x00\x01\x04\x00\x00\x00\x00\x00\xa8\x0b\x00'
        self.assertTrue(fire.analyze_slmp_message(payload))


    def test_analyze_modbus_message_accept(self):
        with open(JSON_FILE, 'w') as outfile:
            json.dump(rules_bank.modbus_read_holding, outfile)

        fire = Fire.Fire(JSON_FILE)

        transaction_id = [0, 1]
        protocol_identifier = [0, 0]
        next_bytes = [0, 6]
        device_address = [0]
        function_code = [3]
        starting_register = [0, 5]
        quantity = [0, 4]

        message_frame = transaction_id + protocol_identifier + next_bytes + device_address + \
                        function_code + starting_register + quantity

        payload = bytes(message_frame)
        self.assertFalse(fire.analyze_modbus_message(payload))
    
    def test_analyze_modbus_message_endpoints_accept(self):
        with open(JSON_FILE, 'w') as outfile:
            json.dump(rules_bank.modbus_read_holding, outfile)

        fire = Fire.Fire(JSON_FILE)

        transaction_id = [0, 1]
        protocol_identifier = [0, 0]
        next_bytes = [0, 6]
        device_address = [0]
        function_code = [3]
        starting_register = [0, 5]
        quantity = [0, 6] #read registers 5 to 10

        message_frame = transaction_id + protocol_identifier + next_bytes + device_address + \
                        function_code + starting_register + quantity

        payload = bytes(message_frame)
        self.assertFalse(fire.analyze_modbus_message(payload))


    def test_analyze_modbus_upper_limit_breach(self):
        with open(JSON_FILE, 'w') as outfile:
            json.dump(rules_bank.modbus_read_holding, outfile)

        fire = Fire.Fire(JSON_FILE)

        transaction_id = [0, 1]
        protocol_identifier = [0, 0]
        next_bytes = [0, 6]
        device_address = [0]
        function_code = [3]
        starting_register = [0, 5]
        quantity = [0, 10]

        message_frame = transaction_id + protocol_identifier + next_bytes + device_address + \
                        function_code + starting_register + quantity

        payload = bytes(message_frame)
        self.assertTrue(fire.analyze_modbus_message(payload))

    def test_analyze_modbus_lower_limit_breach(self):
        with open(JSON_FILE, 'w') as outfile:
            json.dump(rules_bank.modbus_read_holding, outfile)

        fire = Fire.Fire(JSON_FILE)

        transaction_id = [0, 1]
        protocol_identifier = [0, 0]
        next_bytes = [0, 6]
        device_address = [0]
        function_code = [3]
        starting_register = [0, 0]
        quantity = [0, 10]

        message_frame = transaction_id + protocol_identifier + next_bytes + device_address + \
                        function_code + starting_register + quantity

        payload = bytes(message_frame)
        self.assertTrue(fire.analyze_modbus_message(payload))
    
    def test_analyze_modbus_upper_lower_limit_breach(self):
        with open(JSON_FILE, 'w') as outfile:
            json.dump(rules_bank.modbus_read_holding, outfile)

        fire = Fire.Fire(JSON_FILE)

        transaction_id = [0, 1]
        protocol_identifier = [0, 0]
        next_bytes = [0, 6]
        device_address = [0]
        function_code = [3]
        starting_register = [0, 0]
        quantity = [0, 20]

        message_frame = transaction_id + protocol_identifier + next_bytes + device_address + \
                        function_code + starting_register + quantity

        payload = bytes(message_frame)
        self.assertTrue(fire.analyze_modbus_message(payload))

    def test_analyze_modbus_message_reject(self):
        with open(JSON_FILE, 'w') as outfile:
            json.dump(rules_bank.modbus_read_holding, outfile)

        fire = Fire.Fire(JSON_FILE)

        transaction_id = [0, 1] 
        protocol_identifier = [0, 0]
        next_bytes = [0, 6]
        device_address = [0]
        function_code = [4] # Read input registers 
        starting_register = [0, 0]
        quantity = [0, 4]

        message_frame = transaction_id + protocol_identifier + next_bytes + device_address + \
                        function_code + starting_register + quantity

        payload = bytes(message_frame)
        self.assertTrue(fire.analyze_modbus_message(payload))

    def test_analyze_modbus_packet_with_no_message_accept(self):
        with open(JSON_FILE, 'w') as outfile:
            json.dump(rules_bank.modbus_read_holding, outfile)

        fire = Fire.Fire(JSON_FILE)

        message_frame = []

        payload = bytes(message_frame)
        self.assertFalse(fire.analyze_modbus_message(payload))



    def test_compare_ip_tcp_with_rules_accept(self):
        
        with open(JSON_FILE, 'w') as outfile:
            json.dump(rules_bank.tcp_rule, outfile)

        attributes = {
            "source address": "127.0.0.1",
            "destination address": "127.0.0.2",
            "protocol": "TCP",
            "sport": "1234",  #
            "dport": "5020"
        }
        fire = Fire.Fire(JSON_FILE)
        self.assertFalse(fire.compare_with_rules(attributes))


    def test_rule_with_any_as_attr(self):
        with open(JSON_FILE, 'w') as outfile:
            json.dump(rules_bank.rule_with_any, outfile)
        attributes = {
            "source address": "127.0.0.1",
            "destination address": "127.0.0.2",
            "protocol": "TCP",
            "sport": "124", 
            "dport": "5020"
        }
        fire = Fire.Fire(JSON_FILE)
        self.assertTrue(fire.compare_with_rules(attributes))



    def test_compare_ip_tcp_with_rules_reject_2(self):
        with open(JSON_FILE, 'w') as outfile:
            json.dump(rules_bank.tcp_rule, outfile)

        attributes = {
            "source address": "127.0.0.1",
            "destination address": "127.0.0.2",
            "protocol": "UDP",
            "sport": "1234",  # ANY
            "dport": "5020"
        }
        fire = Fire.Fire(JSON_FILE)
        self.assertTrue(fire.compare_with_rules(attributes))

    def test_compare_modbus_with_rules_reject_1(self):
        with open(JSON_FILE, 'w') as outfile:
            json.dump(rules_bank.modbus_read_holding, outfile)

        attributes = {
            "protocol": "MODBUS",
            "command": "Write Single Register",
            "starting address": "0",
            "quantity": "50"
        }





if __name__ == '__main__':
    unittest.main()
    os.remove(JSON_FILE)
    
    #coverage run --source=. -m unittest discover -s code/tests/
    # coverage report

    # from root directory