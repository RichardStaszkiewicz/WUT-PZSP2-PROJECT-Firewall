from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.framer.socket_framer import ModbusSocketFramer
from pymodbus.factory import ClientDecoder
decoder = ClientDecoder()
client = ModbusClient('127.0.0.2', port=5080, framer=ModbusSocketFramer)

rr = client.read_holding_registers(0, 99)
print(rr.registers)



