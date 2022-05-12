import unittest
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

if __name__ == '__main__':

    unittest.main()