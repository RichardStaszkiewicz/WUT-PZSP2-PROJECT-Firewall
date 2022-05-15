rules = [
    {
        'id': 101,
        "name": 'Wszystkie multiple read readujące mniej niz 100',
        'direction': 'IN',
        'protocol': 'MODBUS',
        'Command': 'Device Read Multiple Registers',
        'Start Register': 'Any',
        'Quantity': 100,
        "Comparison": "MAX",
        "is_active": True
    },
    {
        'id': 102,
        "name": 'Wszystkie multiple read readujące mniej niz 100',
        'direction': 'IN',
        'protocol': 'MODBUS',
        'Command': 'Device Read Multiple Registers',
        'Start Register': 'Any',
        'Quantity': 100,
        "is_active": True
    },
]


def get_rules():
    return rules
