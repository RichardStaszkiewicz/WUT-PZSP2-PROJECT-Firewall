import unittest

from attr import attributes
import Rules


class TestRules(unittest.TestCase):
    
    sample_rule = Rules.Rule(101, 192, 196, "MODBUS", 80, 0, 11, 100, "IN", "MAX")
    
    def test_empty_rule(self):
        pass

    def test_get_id(self):
        self.assertEqual(self.sample_rule.get_id(), 101)
    
    def test_get_src(self):
        self.assertEqual(self.sample_rule.get_src(), 192)
    
    def test_get_dst(self):
        self.assertEqual(self.sample_rule.get_dst(), 196)
    
    def test_get_protocol(self):
        self.assertEqual(self.sample_rule.get_protocol(), "MODBUS")
    
    def test_get_dport(self):
        self.assertEqual(self.sample_rule.get_dport(), 80)
    
    def test_get_function_code(self):
        self.assertEqual(self.sample_rule.get_function_code(), 0)
    
    def test_get_starting_address(self):
        self.assertEqual(self.sample_rule.get_starting_address(), 11)
    
    def test_get_register_quantity(self):
        self.assertEqual(self.sample_rule.get_register_quantity(), 100)
    
    def test_get_direction(self):
        self.assertEqual(self.sample_rule.get_direction(), "IN")
       
    def test_get_action(self):
        self.assertEqual(self.sample_rule.get_action(), "MAX")

    def test_set_id(self):
        self.sample_rule.set_id(1)
        self.assertEqual(self.sample_rule.get_id(), 1)
    
    def test_set_src(self):
        self.assertEqual(self.sample_rule.get_src(), 192)
    
    def test_set_dst(self):
        self.assertEqual(self.sample_rule.get_dst(), 196)
    
    def test_set_protocol(self):
        self.assertEqual(self.sample_rule.get_protocol(), "MODBUS")
    
    def test_set_dport(self):
        self.assertEqual(self.sample_rule.get_dport(), 80)
    
    def test_set_function_code(self):
        self.assertEqual(self.sample_rule.get_function_code(), 0)
    
    def test_set_starting_address(self):
        self.assertEqual(self.sample_rule.get_starting_address(), 11)
    
    def test_set_register_quantity(self):
        self.assertEqual(self.sample_rule.get_register_quantity(), 100)
    
    def test_set_direction(self):
        self.assertEqual(self.sample_rule.get_direction(), "IN")
       
    def test_set_action(self):
        self.assertEqual(self.sample_rule.get_action(), "MAX")

if __name__ == '__main__':
    unittest.main()
