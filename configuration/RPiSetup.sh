#!/bin/sh

# call
# sudo sh RPiSetup.sh [bridge-name]

NAME="${1:-"firewall-bridge"}"

echo instaling python...
apt-get -qq --yes install python3

echo installing iptables...
apt-get -qq --yes install iptables

echo installing bridge-utils...
apt-get -qq -yes install bridge-utils

echo bringing up interfaces...
ip link set dev eth0 up
ip link set dev eth1 up

echo creating bridge, $NAME between eth0 and eth1...
brctl addbr $NAME
ip addr add 192.168.1.55/24 dev $NAME
brctl addif $NAME eth0 eth1

echo Adjusting dhcpcd.conf file...
echo denyinterfaces eth0 eth1 >> /etc/dhcpcd.conf

echo Adjusting interfaces file...
echo auto $NAME >> /etc/network/interfaces
echo iface $NAME inet manual >> /etc/network/interfaces
echo bridge_ports eth0 eth1 >> /etc/network/interfaces

echo "Please remember to enable forwarding by uncommenting net.ipv4.ip_forward=1 in /etc/sysctl.conf file and then reboot" 