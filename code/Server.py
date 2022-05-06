import struct

from pyModbusTCP.client import ModbusClient
import time

from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext, ModbusSequentialDataBlock
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.pdu import ModbusRequest, ModbusResponse, ModbusExceptions
from pymodbus.server.asynchronous import StartTcpServer
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.client.common import ModbusClientMixin
from pymodbus.transaction import ModbusSocketFramer as ModbusFramer
from pymodbus.version import version
from pymodbus.compat import int2byte, byte2int

def run_server():
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [17]*100),
        co=ModbusSequentialDataBlock(0, [17]*100),
        hr=ModbusSequentialDataBlock(0, [17]*100),
        ir=ModbusSequentialDataBlock(0, [17]*100))

    context = ModbusServerContext(slaves=store, single=True)
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
    identity.ProductName = 'Pymodbus Server'
    identity.ModelName = 'Pymodbus Server'
    identity.MajorMinorRevision = version.short()

    StartTcpServer(context, identity=identity, address=("", 5080))

if __name__ == "__main__":
    run_server()

