## @package FIRE
## @author PZSP2-22L Firewall Team
## @date 03.06.2022
## @copyright All rights reserved
# Module simulating Modbus client.

# Basic Modbus client to test connection and FIRE filtering
# with pymodbus library

from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext, ModbusSequentialDataBlock
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.server.asynchronous import StartTcpServer, StartUdpServer

from pymodbus.version import version


def run_server():
    store = ModbusSlaveContext()

    context = ModbusServerContext(slaves=store, single=True)
    identity = ModbusDeviceIdentification()
    identity.MajorMinorRevision = version.short()

    StartTcpServer(context, identity=identity, address=("", 5020))

if __name__ == "__main__":
    run_server()
