## @package FIRE
## @author PZSP2-22L Firewall Team
## @date 03.06.2022
## @copyright All rights reserved
# Module simulating Modbus client.

# Basic Modbus client to test connection and FIRE filtering
# with pymodbus library

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.framer.socket_framer import ModbusSocketFramer
from pymodbus.factory import ClientDecoder
import sys
decoder = ClientDecoder()
client = ModbusClient('127.0.0.1', port=5020, framer=ModbusSocketFramer)
starting_register = sys.argv[1] 
quantity = sys.argv[2]
try:
    client.write_registers(starting_register, quantity * [15])
    rr = client.read_holding_registers(starting_register, quantity)
    for i in range(starting_register, starting_register + quantity):
        print(f"Adres rejestru: {i}, wartość rejestru {rr.registers[i - starting_register]}")
except Exception:
    print("Brak dostępu do podanych rejestrów")



