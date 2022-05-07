rules = [
    {
        "id": 1, "name": "ASD", "protocol": 1, "profile": 0,
        "direction": 1, "analysed_param": 0, "expected_val": 0
    },
    {
        "id": 4, "name": "SDASD", "protocol": 2, "profile": 0,
        "direction": 0, "analysed_param": 0, "expected_val": 0
    },
    {
        "id": 5, "name": "FW", "protocol": 1, "profile": 3,
        "direction": 0, "analysed_param": 5, "expected_val": "f2"
    },
    {
        "id": 5, "name": "FW", "protocol": 1, "profile": 3,
        "direction": 0, "analysed_param": 5, "expected_val": "f2"
    },
]


def get_rules():
    for rule in rules:
        rule['is_active'] = True
    return rules
