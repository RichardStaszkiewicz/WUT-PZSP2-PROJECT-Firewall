# PZSP2 Firewall

Repository of PZSP2 project.

## TL;DR
Raspberry Firewall for SLMP and MODBUS protocols along with interactive Web interface.

## Installation
**Instalation manual as for _1753eed_ commit**

## Server & Client

### SLMP Simulators
SLMP Simulators are accessible in /materials/SLMP directory.
**ATTENTION1** Simulator requires python2

### Modbus Simulators
MODBUS/TCP Simulators are accessible in /code/tests directory.
To use those, one shall execute command **pip install -Ur code/tests/requirements.txt**
**ATTENTION1** Simulator requires python3

## RaspberryPi
In order to set up environment, run as superuser commands:
**sh code/flask/setup_frontend.sh** - the command sets up Configuration module
**pip3 install -Ur code/requirements.txt** - the command sets up Fire module & unit tests

## Running
### Setting up Client
1. Configure static IP
To do so, edit the dhcpcd.conf file or use your OS GUI and set it to 192.168.2.2/24.
2. Configure routing table
To do so, run as superuser script from repository /configuration/ClientSetup.sh.
**ATTENTION!** after running the script you are very likely to loose your internet connection

### Setting up Server
1. Configure static IP
To do so, edit the dhcpcd.conf file or use your OS GUI and set it to 192.168.1.2/24.
2. Configure routing table
To do so, run as superuser script from repository /configuration/ServerSetup.sh.
**ATTENTION!** after running the script you are very likely to loose your internet connection

### Setting up Firewall on RaspberryPi
1. Configure static IP
To do so, edit the dhcpcd.conf file.
Client Interface (Eth0) shall be configured to static IP address of 192.168.2.1/24.
Server Interface (Eth1) shall be configured to static IP address of 192.168.1.1/24.
2. Configure routing table
To do so, run as superuser script on repository /configuration/FirewallSetup.sh from main repository directory.
**ATTENTION!** after running the script you are very likely to loose your internet connection
**ATTENTION!** after running the script, the FIRE module will start automatically

### Enabeling Configuration module on RaspberryPi
1. Running the configuration module
To run Configuration module, run from main repository directory command **python3 code/flask/view.py**
2. Accessing the configuration module
To access configuration module, open in Web Browser the IP:5000 as visible after running previous command.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Test and Deploy

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
