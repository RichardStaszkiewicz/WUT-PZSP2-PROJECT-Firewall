rules = [
    {
        'id': 101,
        "name": 'Wszystkie multiple read readujące mniej niz 100',
        'direction': 'IN',
        'protocol': 'MODBUS',
        'command': 'Device Read Multiple Registers',
        'Start Register': 'Any',
        'quantity': 100,
        "comparison": "MAX",
        "is_active": True
    },
    {
        'id': 102,
        "name": 'Wszystkie multiple read readujące mniej niz 100',
        'direction': 'IN',
        'protocol': 'MODBUS',
        'command': 'Device Read Multiple Registers',
        'Start Register': 'Any',
        'quantity': 100,
        "comparison": "MAX",
        "is_active": True
    },
]


def get_rules():
    return rules
