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
from scapy.sendrecv import send
from scapy.packet import Raw
# import pdb
# pdb.set_trace()
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
                if set(attributes.keys()).issubset(rule.keys()):
                    match = True
                    for attr in attributes:
                        print("ATTRIBUTE", attributes[attr], rule[attr])
                        if rule[attr] != 'ANY':
                            if attr == "end_register":
                                print("INSIDE MAX")
                                match = int(attributes['end_register']) <= int(rule['end_register'])
                            elif attr == "start_register":
                                print("INSIDE MIN")
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
                attributes.update({'end_register' : start_register + quantity})

        
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
        ip_pkt = IP(pkt.get_payload())
        # response_pkt = IP(dst=ip_pkt.src) / ICMP(type=3, code=13)
        # send(response_pkt)
        tran_pkt = ip_pkt[TCP]
        payload = bytes(tran_pkt.payload)
        print(len(payload))

        ack = IP(src=ip_pkt.dst, dst=ip_pkt.src) / TCP(sport=tran_pkt.dport, dport=tran_pkt.sport, flags='A', seq=1, ack=22)
        ack = rdpcap('materials/PCAP/sample_slmp_server_ack.pcap')[0][IP]
        # send(ack)
        # # rst = IP(src=ip_pkt.dst, dst=ip_pkt.src) / TCP(sport=tran_pkt.dport, dport=tran_pkt.sport, flags='R')
        # # sr1(rst)
        # syn = IP(src=ip_pkt.dst, dst=ip_pkt.src) / TCP(sport=tran_pkt.dport, dport=tran_pkt.sport, flags='S')
        # syn_ack = sr1(syn)
        empty_pkt_to_server = ip_pkt
        empty_pkt_to_server[TCP].remove_payload()
        del empty_pkt_to_server.len
        del empty_pkt_to_server.chksum
        del empty_pkt_to_server[TCP].chksum
        send(empty_pkt_to_server)


        error_response_hex = 'D0 00 00 FF FF 03 00 0B 00 FF 4F 00 FF FF 03 00 01 04 00 00'
        payload_with_error = bytes.fromhex(error_response_hex)

        ack = rdpcap('materials/PCAP/sample_slmp_server_ack.pcap')[0]
        psh_ack = rdpcap('materials/PCAP/sample_slmp_server_psh_ack.pcap')[0]

        tran_time = tran_pkt.options[2][1][0]
        del ack[IP].chksum
        del ack[IP][TCP].chksum
        ack[IP].dst = ip_pkt.src
        ack[IP][TCP].dport = tran_pkt.sport
        ack[IP][TCP].seq = tran_pkt.ack
        ack[IP][TCP].ack = tran_pkt.seq + len(payload)
        ack[IP][TCP].options = [('NOP', None), ('NOP', None), ('Timestamp', (int(tran_time) + 10, int(tran_time)))]

        sendp(ack, iface="lo")

        del psh_ack[IP].len
        del psh_ack[IP].chksum
        del psh_ack[IP][TCP].chksum
        psh_ack[IP].dst = ip_pkt.src
        psh_ack[IP][TCP].dport = tran_pkt.sport
        psh_ack[IP][TCP].seq = tran_pkt.ack
        psh_ack[IP][TCP].ack = tran_pkt.seq + len(payload)
        psh_ack[IP][TCP].options = [('NOP', None), ('NOP', None), ('Timestamp', (tran_time + 10, tran_time))]
        psh_ack[IP][TCP].remove_payload()
        psh_ack[IP][TCP] /= Raw(payload_with_error)
        sendp(psh_ack, iface="lo")
        # time.sleep(1)
        # client_rst = IP(dst=ip_pkt.src, src=ip_pkt.dst) / TCP(sport=tran_pkt.dport, dport=tran_pkt.sport, flags='R')
        # sever_rst = IP(dst=ip_pkt.dst, src=ip_pkt.src) / TCP(sport=tran_pkt.sport, dport=tran_pkt.dport, flags='R')
        # send(client_rst, iface="lo")
        # send(sever_rst, iface="lo")


        # fin_ack_time = tran_pkt.options[2][1][0]

        # fin_ack_too = fin_ack
        # fin_ack_too[IP][TCP].sport, fin_ack_too[IP][TCP].dport = fin_ack_too[IP][TCP].dport, fin_ack_too[IP][TCP].sport
        # fin_ack_too[IP][TCP].seq, fin_ack_too[IP][TCP].ack = fin_ack_too[IP][TCP].ack + 1, fin_ack_too[IP][TCP].seq + 1
        # fin_ack_too[IP][TCP].options = [('NOP', None), ('NOP', None), ('Timestamp', (fin_ack_too + 10, fin_ack_time))]
        # sendp(fin_ack_too, iface="lo")

        #
        # del fin_ack_too[IP].len
        # del fin_ack_too[IP].chksum
        # del fin_ack_too[IP][TCP].chksum

        # ack[IP][TCP].seq = fin.ack
        # ack[IP][TCP].ack = fin.seq + len(payload)
        # ack[IP][TCP].options = [('NOP', None), ('NOP', None), ('Timestamp', (int(tran_time) + 10, int(tran_time)))]

        # payload = bytes(tran_pkt.payload)
        # error_response_hex = 'D0 00 00 FF FF 03 00 0B 00 FF 4F 00 FF FF 03 00 01 04 00 00'
        # payload_with_error = bytes.fromhex(error_response_hex)
        # host = ip_pkt.src
        # port = tran_pkt.sport  # The same port as used by the server
        # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s.bind(('', tran_pkt.dport))
        # s.connect((host, port))
        # s.sendall(payload_with_error)
        # s.close()
        # response_pkt = IP(src=ip_pkt.dst, dst=ip_pkt.src) / TCP(sport=tran_pkt.dport, dport=tran_pkt.sport, flags='PA') / Raw(payload_with_error)
        # sr1(response_pkt)


# D0 00 00 FF FF 03 00 0B 00 FF 4F 00 FF FF 03 00 01 04 00 00 error response


fire = Fire(RULES_PATH)

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