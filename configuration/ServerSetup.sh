#!/bin/sh

# Flush all records in routing table
ip route flush table main

# Make records applicable in routing
ip route add default dev enp0s25
ip route add 192.168.2.0/24 via 192.168.2.1 dev enp0s25