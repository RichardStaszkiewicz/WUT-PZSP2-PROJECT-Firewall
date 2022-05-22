import json

def get_rules():
    with open('code/Conf.json', 'r') as file:
        rules = json.load(file)
    return rules
