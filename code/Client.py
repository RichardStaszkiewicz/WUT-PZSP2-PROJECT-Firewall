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
decoder = ClientDecoder()
client = ModbusClient('127.0.0.1', port=5020, framer=ModbusSocketFramer)

starting_register = 0
quantity = 100
try:
    for i in range(100):
        client.write_register(i, 15)
    rr = client.read_holding_registers(starting_register, quantity)
    for i in range(starting_register, quantity):
        print(f"Adres rejestru: {i}, wartość rejestru {rr.registers[i]}")
except Exception:
    print("Brak dostępu do podanych rejestrów")



