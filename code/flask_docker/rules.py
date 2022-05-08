rules = [
    {
        'id': 101,
        "name": 'Accept multiple read less than 100',
        'direction': 'IN',
        'protocol': 'MODBUS',
        'Command': 'Device Read Multiple Registers',
        'Start Register': 'Any',
        'Quantity': 100,
        "Comparison": "MAX"
    },
    {
        'id': 100,
        "name": 'Accept All',
        'direction': 'IN',
        'protocol': 'IP/TCP',
        'Source': 'all',
        'Destination': 'All',
        'Destination Port': 'All'

    },
]


def get_rules():
    for rule in rules:
        rule['is_active'] = True
    return rules
