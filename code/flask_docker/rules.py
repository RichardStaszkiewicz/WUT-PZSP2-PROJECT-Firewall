import json

def get_rules():
    with open('rules.json', 'r') as file:
        rules = json.load(file)
    return rules["rules"]
