import json

def get_rules():
    with open('lrules.json', 'r') as file:
        rules = json.load(file)
    return rules["rules"]
