from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext, ModbusSequentialDataBlock
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.server.asynchronous import StartTcpServer, StartUdpServer

from pymodbus.version import version


def run_server():
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [10]*101),
        co=ModbusSequentialDataBlock(0, [10]*101),
        hr=ModbusSequentialDataBlock(0, [10]*101),
        ir=ModbusSequentialDataBlock(0, [10]*101))

    context = ModbusServerContext(slaves=store, single=True)
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
    identity.ProductName = 'Pymodbus Server'
    identity.ModelName = 'Pymodbus Server'
    identity.MajorMinorRevision = version.short()

    StartTcpServer(context, identity=identity, address=("", 5020))


if __name__ == "__main__":
    print("Zawartość holding registers serwera MODBUS:")
    for i in range(1, 101):
        print(f"Adres rejestru: {i}, wartość rejestru: 10")
    run_server()
