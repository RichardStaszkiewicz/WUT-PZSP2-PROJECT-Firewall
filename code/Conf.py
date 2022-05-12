## @package CONF
## @author PZSP2-22L Firewall Team
## @date 24.04.2022
## @copyright All rights reserved
# Module implements Firewall configuration.

# CONF module implements all funcionalities needed to
# manage the rules and delivers them to the Firewall
# as a json file

from email.policy import default
from numpy import object_
from Rules import Rule
import json
from collections import namedtuple

## MyEncoder is a class needed to pasre all the data into the json file

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        return {k.lstrip('_'): v for k, v in vars(obj).items()}

##
# CONF is a class that contains all created rules and allows users
# to manage them. It is responsible for reading data from and writing
# into a file called Conf_tmp.json.

class Conf:

    ## Constructor responsible for processing json file into a list of rules
    # @param self the object pointer

    def __init__(self) -> None:

        self._list_of_rules = []
        self._id_next = 0

        with open('Conf.json', 'r') as file:
            data = file.read().replace('\n', '')

        all_rules = list(json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values())))
        for single_rule in all_rules:
            rule = Rule(single_rule[0], single_rule[1], single_rule[2], single_rule[3], single_rule[4], single_rule[5], single_rule[6], single_rule[7], single_rule[8], single_rule[9])
            self._list_of_rules.append(rule)
            self._id_next = max(self._id_next, single_rule[0])

    ## Method processing list of rules into json
    # @param self the object pointer

    def conf_to_json(self) -> None:
        Json = "[\n"
        for rule in self._list_of_rules:
            Json += "    "
            jsons = json.dumps(rule, cls=MyEncoder)
            Json += jsons
            Json += ",\n"
        Json = Json[:-2]
        Json += "\n]"
        self.write_config_file(Json)

    ## Method saving json into the file
    # @param self the object pointer
    # @param Json data in json format

    def write_config_file(self, Json) -> None:
        with open('Conf.json', 'w') as file:
            file.write(Json)

    ## Method adding one rule into the config with an unique id
    # @param self the object pointer
    # @param name user's name of the rule
    # @param protocol choice of the protocol
    # @param profile choice of a profile list
    # @param direction choice of direction(s) of the rule
    # @param analysed_param determines what parameter is being checked
    # @param expected_val determines the value of the parameter that is allowed

    def add_rule(self, src, dst, protocol, dport, direction, action):
        rule = Rule(self._id_next + 1, src, dst, protocol, dport, direction, action)
        self._id_next += 1
        self._list_of_rules.append(rule)

    ## Method removing one rule from config using the rule's unique id
    # @param self the object pointer
    # @param id rule's unique id

    def del_rule(self, id):
        for x in self._list_of_rules:
            if x.get_id() == id:
                self._list_of_rules.remove(x)



if __name__ == "__main__":
    conf = Conf()
    conf.add_rule("FW", 1, 3, 0, 5, "f2")
    conf.del_rule(6)
    for x in conf._list_of_rules:
        print(x._id)
    conf.conf_to_json()
