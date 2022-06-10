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


rule_with_any = {
    "rules":
        [
            {
            "id": 1,
            "name": "true",
            "is_active": "ANY",
            "source address": "ANY",
            "destination address": "ANY",
            "protocol": "ANY",
            "sport": "ANY", 
            "dport": "ANY"

            }
        ]
}

unfinished_rule = {
    "rules":
        [
            {
            "id": 1,
            "name": "ANY",
            "is_active": "ANY",
            "source address": "ANY",
            "destination address": "ANY",
            "protocol": "ANY",
            "sport": "ANY", 
            "dport": "ANY"
            }
        ]
    }

tcp_rule= {
    "rules":
        [
            {
            "id": 1,
            "name": "Accept incoming TCP with SLMP payload",
            "is_active": "true",
            "source address": "127.0.0.1",
            "destination address": "127.0.0.2",
            "protocol": "TCP",
            "sport": "1234", 
            "dport": "5020"

            }
        ]
    }

modbus_read_holding = {
    "rules":
        [
            {
            "command": "Read Holding Registers",
            "id": 123,
            "is_active": "true",
            "name": "Accept MODBUS TCP reads from 205 to 220 on single registers",
            "protocol": "MODBUS",
            "start_register": "5",
            "end_register": "10"       
            }

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

