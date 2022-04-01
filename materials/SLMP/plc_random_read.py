#!/usr/bin/python2

from struct import *
import socket
import SLMP
import sys

PLC_IP = '127.0.0.1'
PLC_PORT = 1280 #1280
BUFFER_SIZE = 100

if len(sys.argv)<2:
    print "At least one register number needed"
    exit()

request = SLMP.prepare_random_read_message(sys.argv[1:],0xa8)


print "Request packet"
print SLMP.binary_array2string(request)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((PLC_IP, PLC_PORT))
s.send(request)

response = s.recv(BUFFER_SIZE)

print "Response packet"
print SLMP.binary_array2string(response)

s.close()

response_data = response[9:]

result, = unpack("<H", response_data[0:2])

if (result != 0):
    print "PLC reported error"
    exit()


print "PLC reported no error"
print "Received values"

print "Register no: Register value"

i = 2

for n in range(len(sys.argv)-1):
    value, = unpack("<H", response_data[i:i+2])
    print "%d: %d" % (int(sys.argv[1+n]), value)
    i = i + 2

