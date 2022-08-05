#!/bin/sh

# Allow IP forwarding in kernel and iptables
# if executed preperation along with REDEME instructions, unnecessary
# echo 1 > /proc/sys/net/ipv4/ip_forward
iptables --flush FORWARD
iptables -P FORWARD ACCEPT

# clear IPTABLES from all unnecessary rules
iptables -F DOCKER-ISOLATION-STAGE-2
iptables -F DOCKER-ISOLATION-STAGE-1
iptables -F DOCKER-USER
iptables -t nat -F OUTPUT
iptables -t nat -F PREROUTING
iptables -t nat -F POSTROUTING
iptables -t nat -F DOCKER

# Configure iptables NFQUEUE
iptables -I FORWARD -d 192.168.1.0/24 -j NFQUEUE --queue-num 1

# Flush historical logs to specialised file
cat logs/events.log >> logs/events.log.historical

# Run Firewall
python3 code/Fire/Fire.py