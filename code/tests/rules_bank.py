sample_rule = {
    "rules":
        [
            {
            "id": 1,
            "name": "Accept incoming TCP with SLMP payload",
            "is_active": "true",
            "source_address": "127.0.0.1",
            "destination_address":"127.0.0.1",
            "protocol": "TCP",
            "source_port": "ANY",
            "destination_port": "1280"

            }
        ]
}

sample_modbus_rules = {
    "rules":
        [

        ]
    }



slmp_read_rule = {
    "rules":
        [
        {
        "id": 3,
        "name": "Accept outgoing TCP with SLMP payload",
        "is_active": "true",
        "protocol": "SLMP",
        "command": "Read",
        "subcommand" : "Read from bit dev in 16 point units",
        "start_register": "5",
        "end_register" : "10"
        }
        ]
    }
slmp_write_rule = {
    "rules":
        [
            {
            "id": 3,
            "name": "Accept outgoing TCP with SLMP payload",
            "is_active": "true",
            "protocol": "SLMP",
            "command": "Write",
            "subcommand" : "Read from bit dev in 16 point units",
            "start_register": "5",
            "end_register" : "10"
            }
        ]
    }


