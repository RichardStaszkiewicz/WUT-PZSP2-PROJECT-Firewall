## @package FIRE
## @author PZSP2-22L Firewall Team
## @date 10.04.2022
## @copyright All rights reserved
# Module implements Firewall executive.

# Basing on NetFilter the messages are being filtered
# on application layer after being judged by a configuration
# rules.
import logging

from netfilterqueue import NetfilterQueue
from scapy.layers.inet import IP, TCP, UDP
from Logger import Logger
from threading import Thread
import subprocess
import json
import time

MODBUS_SERVER_PORT = 5020
SLMP_SERVER_PORT = 1280
FIFO_PATH = "./dataFlow"
updateFlag = 0

def ip_proto(ip_pkt):
    proto_field = ip_pkt.get_field('proto')
    return proto_field.i2s[ip_pkt.proto].upper()

def fifo_thread():
    global updateFlag
    while(True):
        with open(FIFO_PATH) as fifo:
            fifo.read() 
        updateFlag = 1

def create_thread():
    subprocess.call("./RunFifoScript.sh")


## Documentation of FIRE
#
# FIRE is an class containing all firewall executive functionalities
class Fire(object):
    ## Keeps all rules required for filtering
    rules = []

    ## Constructor
    # @param self The object pointer

    def __init__(self,rules_file) -> None:
        self.logger = Logger("../logs/events.log")
        self.rules_file = rules_file
        Thread(target=create_thread).start()
        time.sleep(5)
        Thread(target=fifo_thread).start()


    ## Method reading rules from config file
    # @param self The object pointer
    #
    def update_rules(self) -> None:
        f = open(self.rules_file)
        data = json.load(f)
        self.rules = data["rules"]
        f.close()
    

    def get_rules(self):
        return self.rules

    ## Method analyzing packets in terms of TCP/IP rules
    # @param self The object pointer
    # @param pkt Packet recieved from netfilter queue
    def analyze_tcp_ip(self, pkt):
        global updateFlag
        if updateFlag == 1:
            self.update_rules()
            updateFlag = 0
        ip_pkt = IP(pkt.get_payload())
        if ip_pkt.haslayer(TCP):
            tran_pkt = ip_pkt[TCP]
        elif ip_pkt.haslayer(UDP):
            tran_pkt = ip_pkt[UDP]
        else:
            self.reject_packet(pkt, '\nPacket rejected: not a TCP nor UDP packet\n')
            return

        protocol = ip_proto(ip_pkt)
        sport = tran_pkt.sport
        dport = tran_pkt.dport
        attributes = {
            'source_address': ip_pkt.src,
            'destination_address': ip_pkt.dst,
            'protocol': protocol,
            'source_port': str(sport),
            'destination_port': str(dport)
        }
        
        drop = self.compare_with_rules(attributes)
        if not drop:
            if dport == MODBUS_SERVER_PORT:
                payload = bytes(tran_pkt.payload)
                drop = self.analyze_modbus_message(payload)
            elif sport == MODBUS_SERVER_PORT:
                drop = False
            elif dport == SLMP_SERVER_PORT:
                payload = bytes(tran_pkt.payload)
                drop = self.analyze_slmp_message(payload)
            elif sport == SLMP_SERVER_PORT:
                drop = False
        if drop:
            self.reject_packet(pkt, "\nPacket rejected\n" + ip_pkt.show(dump=True))
        else:
            self.accept_packet(pkt, "\nPacket accepted\n" + ip_pkt.show(dump=True))


    ## Method comparing packets with rules
    # @param self The object pointer
    # @param attributes List of packet attributes to compare with rules
    def compare_with_rules(self, attributes):
        drop = True
        for rule in self.rules:
            if rule["is_active"] == "true": 
                match = True
                missed_attr_count = 0
                for attr in attributes:
                    if attr in rule:
                        print("ATTRIBUTE", attributes[attr], rule[attr])

                        if rule[attr] != 'ANY':
                            if attr == "max_value":
                                print("INSIDE MAX")
                                match = int(attributes['max_value']) <= int(rule['max_value'])
                            elif attr == "min_value":
                                print("INSIDE MIN")
                                match = int(attributes['min_value']) >= int(rule['min_value'])
                            else:
                                match = (rule[attr] == attributes[attr])
                        if not match:
                            break
                    else:
                        missed_attr_count += 1
                if missed_attr_count == len(attributes):
                    match = False
                if match:
                    drop = False
                    return drop
        print(attributes, '\n')
        return drop


    ## Method analyzing complete message under firewall rules
    # @param self The object pointer
    # @param payload Data from tcp/udp packet
    def analyze_modbus_message(self, payload):
        function_codes2names = {
            '1': 'Read Coils',
            '2': 'Read Discrete Inputs',
            '3': 'Read Holding Registers',
            '4': 'Read Input Registers',
            '5': 'Write Single Coil',
            '6': 'Write Single Register',
            '15': 'Write Multiple Coils',
            '16': 'Write Multiple Registers',
            '23': 'Read/Write Multiple registers',
        }
        if len(payload) > 7:
            protocol = 'MODBUS'
            function_code = str(int(payload[7]))
            if function_code in {'1', '2', '3', '4'}:
                starting_address = str(int.from_bytes(payload[8:10], 'little'))
                quantity = str(int.from_bytes(payload[11:13], 'little'))
                last_address = str(int(starting_address) + int(quantity) - 1)
                attributes = {
                    'protocol': protocol,
                    'command': function_codes2names[function_code],
                    'min_value': starting_address,
                    'max_value': last_address
                }
            elif function_code in {'5', '6'}:
                output_address = str(int.from_bytes(payload[8:10], 'little'))
                attributes = {
                    'protocol': protocol,
                    'command': function_codes2names[function_code],
                    'output_address': output_address,
                }
            return self.compare_with_rules(attributes)
        else:
            return False

    ## Method analyzing captured SLMP packet message under fire rules
    # @param self The object pointer
    # @param payload Data from tcp/udp packet
    def analyze_slmp_message(self, payload):

#    write 55 20 ( wpisz do 54 rejestru wartość 20)                                                                             
#                                            WRITE               MIN_VALUE              MAX VALUE        
# \x00\x00\xff\xff\x03\x00\x0e\x00\x04\x00\  [x01\x14]  \x00\x00\  [0x37]  \x00\x00\xa8\    [x01]     \x00\x14\x00'

#    read 0 20 (20 rejestrów zaczynając od 20)    
#                                                READ             MIN VALUE               MAX VALUE 
# x00\x00\xff\xff\x03\x00\x0c\x00\x04\x00\   [x01\x04] \x00\x00    [\x00]   \x00\x00\xa8\   [x14]      \x00'


        function_codes2names = { 
            b'\x01\x04' : 'Read',
            b'\x01\x14' : 'Write',
            # '0403' : 'Device Read Random',
            # '1402' : 'Device Write Random',
            # '0406' : 'Device Read (Batch)', #block
            # '1406' : 'Device Write (Batch)' #block'
        }
        subcommand_names = {
            b'\x00\x00' : "Read from bit dev in 16 point units"
            # 1 : "Read from bit dev in 1 point units",
            # 3 : "Read from bit dev in 1 point units",
            # 2 : "Read from word devices in 1 word units"
        }
        attributes = {}
     
        if len(payload) > 0:
            command = payload[11:13]
            subcommand = payload[13:15]
            head_dev_no = payload[15:18] # 
            dev_code = payload[18:19]
            no_of_dev_pts = payload[19:21]

            
            max_value = int.from_bytes(payload[19:20], 'little')
            starting_register = int.from_bytes(payload[15:16], 'little') # ponieważ roboczo plc_write/ plc_read zmienia tylko jeden bajt


            if function_codes2names[command] == "Write":
                attributes = {
                        'protocol': 'SLMP',
                        'command': function_codes2names[command],
                        'subcommand': subcommand_names[subcommand],
                        'min_value' : starting_register,
                        'max_value' : starting_register
                    }
            elif function_codes2names[command] == "Read":
                attributes = {
                        'protocol': 'SLMP',
                        'command': function_codes2names[command],
                        'subcommand': subcommand_names[subcommand],
                        'min_value' : starting_register,
                        'max_value' : max_value
                    }

            print(payload,"\n",attributes)
            return self.compare_with_rules(attributes)
        else:
            drop = False
            return drop
        
    











    ## Method forwarding the accepted message packeges onward to a defended subnet
    # @param self The object pointer
    # @param message The network message fulfiling the firewall requirenments to be send onward
    def accept_packet(self, pkt, message):
        self.logger.log(message)
        pkt.accept()

    ## Method rejecting the given message due to some error
    # @param self The object pointer
    # @param message The network message fulfiling the firewall requirenments to be send onward
    def reject_packet(self, pkt, message):
        self.logger.log(message, logging.WARNING)
        pkt.drop()


fire = Fire("rules.json")

if __name__ == "__main__":

#     # IP Tables configuration: (should work imo)
#     # iptables -I INPUT -d 192.168.0.0/24 -j NFQUEUE --queue-num 1

    nfqueue = NetfilterQueue()
    nfqueue.bind(1, fire.analyze_tcp_ip)


    try:
        nfqueue.run()
        fd = nfqueue.get_fd()
        print(type(fd))
    except KeyboardInterrupt:
        print('')
    nfqueue.unbind()





