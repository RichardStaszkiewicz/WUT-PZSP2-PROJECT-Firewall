from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.framer.socket_framer import ModbusSocketFramer
from pymodbus.factory import ClientDecoder
decoder = ClientDecoder()
client = ModbusClient('127.0.0.2', port=5080, framer=ModbusSocketFramer)

starting_register = 0
quantity = 100
try:
    rr = client.read_holding_registers(starting_register, quantity)
    for i in range(starting_register, quantity):
        print(f"Adres rejestru: {i}, wartość rejestru {rr.registers[i]}")
except Exception:
    print("Brak dostępu do podanych rejestrów")



