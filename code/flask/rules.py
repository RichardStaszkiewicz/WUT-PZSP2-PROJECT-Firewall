import json

def get_rules():
    with open('./data/rules.json', 'r') as file:
        rules = json.load(file)
    return rules["rules"]
