## @package FIRE
## @author PZSP2-22L Firewall Team
## @date 10.04.2022
## @copyright All rights reserved
# Module implements Firewall executive.

import json
# Basing on NetFilter the messages are being filtered
# on application layer after being judged by a configuration
# rules.
import logging
import subprocess
import time
from threading import Thread
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Logger'))
from Logger import Logger

from netfilterqueue import NetfilterQueue
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.sendrecv import send, sendp
from scapy.layers.l2 import Ether, ARP, getmacbyip, STP
from scapy.packet import Raw, Packet

from scapy.utils import rdpcap

MODBUS_SERVER_PORT = 5020
SLMP_SERVER_PORT = 1280
FIFO_PATH = "dataFlow"
RULES_PATH = "./data/rules.json"
updateFlag = 0

def ip_proto(ip_pkt):
    proto_field = ip_pkt.get_field('proto')
    return proto_field.i2s[ip_pkt.proto].upper()

## Thread responsible for incoming data reciving
def fifo_thread():
    global updateFlag
    while(True):
        with open(FIFO_PATH) as fifo:
            fifo.read()
        print("Information: Detected change of rules")
        updateFlag = 1

## Thread responsible for initial data gathering
def create_thread():
    subprocess.call("./code/RunFifoScript.sh")


## Documentation of FIRE
#
# FIRE is an class containing all firewall executive functionalities
class TSval:
    pass


class Fire(object):
    ## Keeps all rules required for filtering
    rules = []

    ## Constructor
    # @param self The object pointer

    def __init__(self, rules_file) -> None:
        self.rules_file = rules_file
        self.update_rules()
        self.logger = Logger("./logs/events.log")
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
        print("Information: Rules have been updated")
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
            self.reject_packet(pkt, "Not TCP nor UDP package")
            return

        protocol = ip_proto(ip_pkt)
        sport = tran_pkt.sport
        dport = tran_pkt.dport
        attributes = {
            'protocol': protocol,
            'source_address': ip_pkt.src,
            'destination_address': ip_pkt.dst,
            'source_port': str(sport),
            'destination_port': str(dport)
        }

        drop = self.compare_with_rules(attributes)
        if not drop:
            if dport == MODBUS_SERVER_PORT:
                payload = bytes(tran_pkt.payload)
                drop = self.analyze_modbus_message(payload)
                if drop:
                    print("Firewall: MODBUS/TCP Packet dropped - blocked by MODBUS/TCP rules")
            elif sport == MODBUS_SERVER_PORT:
                drop = False
            elif dport == SLMP_SERVER_PORT:
                payload = bytes(tran_pkt.payload)
                drop = self.analyze_slmp_message(payload)
                if drop:
                    print("Firewall: SLMP Packet dropped - blocked by SLMP rules")
                    self.send_slmp_error(pkt)
            elif sport == SLMP_SERVER_PORT:
                drop = False
        else:
            print("Firewall: Packet dropped - blocked by TCP rules")

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
                if set(attributes.keys()).issubset(rule.keys()):
                    match = True
                    for attr in attributes:
                        if rule[attr] != 'ANY':
                            if attr == "end_register":
                                match = int(attributes['end_register']) <= int(rule['end_register'])
                            elif attr == "start_register":
                                match = int(attributes['start_register']) >= int(rule['start_register'])
                            else:
                                match = (rule[attr] == attributes[attr])
                        if not match:
                            break
                    if match:
                        drop = False
                        return drop
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
        }
        if len(payload) > 7:
            protocol = 'MODBUS'
            function_code = str(int(payload[7]))
            start_register = str(int.from_bytes(payload[8:10], 'big'))
            if function_code in {'1', '2', '3', '4', '15', '16'}:
                quantity = str(int.from_bytes(payload[10:12], 'big'))
                end_register = str(int(start_register) + int(quantity) - 1)
            if function_code in {'5', '6'}:
                end_register = start_register
            attributes = {
                'protocol': protocol,
                'command': function_codes2names[function_code],
                'start_register': start_register,
                'end_register': end_register
            }
            return self.compare_with_rules(attributes)
        else:
            return False

    ## Method analyzing captured SLMP packet message under fire rules
    # @param self The object pointer
    # @param payload Data from tcp/udp packet
    def analyze_slmp_message(self, payload):
        print('analysinng SLMP')
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
            head_dev_no = payload[15:18]
            dev_code = payload[18:19]
            no_of_dev_pts = payload[19:21]


            quantity = int.from_bytes(payload[19:20], 'little')
            start_register = int.from_bytes(payload[15:16], 'little') # ponieważ roboczo plc_write/ plc_read zmienia tylko jeden bajt


            attributes = {
                'protocol': 'SLMP',
                'command': function_codes2names[command],
                'subcommand': subcommand_names[subcommand],
                'start_register': start_register,
                'end_register': start_register
            }
            if  function_codes2names[command] == "Read":
                attributes.update({'end_register' : start_register + quantity - 1})


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


    ## Method sending error message to slmp client
    # @param self The object pointer
    def send_slmp_error(self, pkt):
        ip_pkt = IP(pkt.get_payload())

        # Not tested on target
        # There are two possible scenarios:
        #   1. It will be neccessary to resolve MAC addresses of client and server
        #      (maybe by ARP request like below or by getmacbyip)
        #   2. Converting packets to 3rd layer will and os routing will be enough

        # arp_request = ARP(op="who-has", psrc=ip_pkt.dst, pdst=ip_pkt.src)
        # ans = srp(arp_request, timeout=5, iface='lo')[0]
        # clients = []
        #
        # for sent, received in ans:
        #     # for each response, append ip and mac address to `clients` list
        #     clients.append({'ip': received.psrc, 'mac': received.hwsrc})

        ack = rdpcap('materials/PCAP/sample_slmp_server_ack.pcap')[0]
        psh_ack = rdpcap('materials/PCAP/sample_slmp_server_psh_ack.pcap')[0]
        src_mac = "e4:5f:01:2b:66:9a"
        dst_mac = "8c:73:6e:84:0b:00"

        tran_pkt = ip_pkt[TCP]
        received_payload = bytes(tran_pkt.payload)
        tsval = tran_pkt.options[2][1][0]
        tsecr = tran_pkt.options[2][1][1]

        error_response_hex = 'D0 00 00 FF FF 03 00 0B 00 FF 4F 00 FF FF 03 00 01 04 00 00'
        payload_with_error = bytes.fromhex(error_response_hex)

        empty_pkt_to_server = ip_pkt
        empty_pkt_to_server[TCP].remove_payload()
        del empty_pkt_to_server.len
        del empty_pkt_to_server.chksum
        del empty_pkt_to_server[TCP].chksum
        send(empty_pkt_to_server)

        del ack[IP].chksum
        del ack[IP][TCP].chksum
        ack.src = src_mac #  possibly uncomment in target
        ack.dst = dst_mac #  possibly uncomment in target

        ack[IP].src = ip_pkt.dst
        ack[IP].dst = ip_pkt.src
        ack[IP][TCP].dport = tran_pkt.sport
        ack[IP][TCP].seq = tran_pkt.ack
        ack[IP][TCP].ack = tran_pkt.seq + len(received_payload)
        ack[IP][TCP].options = [('NOP', None), ('NOP', None), ('Timestamp', (tsecr + 30, tsval))]

        sendp(ack, iface="eth0") # iface Eth0 on target

        del psh_ack.len
        del psh_ack.chksum
        del psh_ack[TCP].chksum
        psh_ack.src = src_mac#  possibly uncomment in target
        psh_ack.dst = dst_mac # getmacbyip(ip_pkt.src) possibly uncomment in target

        psh_ack[IP].src = ip_pkt.dst
        psh_ack[IP].dst = ip_pkt.src
        psh_ack[IP][TCP].dport = tran_pkt.sport
        psh_ack[IP][TCP].seq = tran_pkt.ack
        psh_ack[IP][TCP].ack = tran_pkt.seq + len(received_payload)
        psh_ack[IP][TCP].options = [('NOP', None), ('NOP', None), ('Timestamp', (tsecr + 30, tsval))]
        psh_ack[IP][TCP].remove_payload()
        psh_ack[IP][TCP] /= Raw(payload_with_error)

        sendp(psh_ack, iface="eth0") # iface Eth0 on target


fire = Fire(RULES_PATH)

if __name__ == "__main__":

    nfqueue = NetfilterQueue()
    nfqueue.bind(1, fire.analyze_tcp_ip)

    try:
        nfqueue.run()
        fd = nfqueue.get_fd()
        print(type(fd))
    except KeyboardInterrupt:
        print('')
    nfqueue.unbind()