## @package RULE
## @author PZSP2-22L Firewall Team
## @date 24.04.2022
## @copyright All rights reserved
# Module implements data of single rule in Firewall.

# Basing on the provided data from users rule is created
# and used by CONF module to create the white list.

## Documentation of RULE
#
# RULE is a class containing all information about a single 
# firewall filtration rule.
class Rule:

    ## Constructor
    # @param self the object pointer
    # @param id rule's unique id
    # @param name user's name of the rule
    # @param protocol choice of the protocol
    # @param profile choice of a profile list
    # @param direction choice of direction(s) of the rule
    # @param analysed_param determines what parameter is being checked
    # @param expected_val determines the value of the parameter that is allowed


    def __init__(self, id, name, protocol, profile, direction, analysed_param, expected_val) -> None:
        self._id = id
        self._name = name
        self._protocol = protocol
        self._profile = profile
        self._direction = direction
        self._analysed_param = analysed_param
        self._expected_val = expected_val

    ## Getter method
    # @param self the object pointer
    def get_id(self):
        return self._id
    
    ## Getter method
    # @param self the object pointer
    def get_name(self):
        return self._name

    ## Getter method
    # @param self the object pointer
    def get_protocol(self):
        return self._protocol

    ## Getter method
    # @param self the object pointer
    def get_profile(self):
        return self._profile

    ## Getter method
    # @param self the object pointer
    def get_direction(self):
        return self._direction

    ## Getter method
    # @param self the object pointer
    def get_analysed_param(self):
        return self._analysed_param

    ## Getter method
    # @param self the object pointer
    def get_expected_val(self):
        return self._expected_val

    ## Setter method
    # @param self the object pointer
    def set_id(self, id):
        self._id = id
    
    ## Setter method
    # @param self the object pointer
    # @param name user's name of the rule
    def set_name(self, name):
        self._name = name

    ## Setter method
    # @param self the object pointer
    # @param protocol choice of the protocol
    def set_protocol(self, protocol):
        self._protocol = protocol

    ## Setter method
    # @param self the object pointer
    # @param profile choice of a profile list
    def set_profile(self, profile):
        self._profile = profile

    ## Setter method
    # @param self the object pointer
    # @param direction choice of direction(s) of the rule
    def set_direction(self, direction):
        self._direction = direction

    ## Setter method
    # @param self the object pointer
    # @param analysed_param determines what parameter is being checked
    def set_analysed_param(self, analysed_param):
        self._analysed_param = analysed_param

    ## Setter method
    # @param self the object pointer
    # @param expected_val determines the value of the parameter that is allowed
    def set_expected_val(self, expected_val):
        self._expected_val = expected_val
