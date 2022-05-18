## @package FIRE
## @author PZSP2-22L Firewall Team
## @date 10.04.2022
## @copyright All rights reserved
# Module implements Firewall executive.

# Basing on NetFilter the messages are being filtered
# on application layer after being judged by a configuration
# rules.
from copy import deepcopy
import logging

from netfilterqueue import NetfilterQueue
from scapy.layers.inet import IP, TCP, UDP, Ether
from Logger import Logger
from Rules import Rule
import json

MODBUS_SERVER_PORT = 5020
SLMP_SERVER_PORT = 1280

## Documentation of NetMessage
#
# NetMessage is a class storing a composed, readable message
# along with the packages upholding it


class NetMessage:
    ## Constructor
    # @param self The object pointer
    def __init__(self) -> None:
        pass






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
        self.update_rules()

    ## Method reading rules from config file
    # @param self The object pointer
    #
    def update_rules(self) -> None:
        f = open(self.rules_file)
        data = json.load(f)
        self.rules = data["rules"]
    

    def get_rules(self):
        return self.rules

    ## Method analyzing packets in terms of TCP/IP rules
    # @param self The object pointer
    # @param pkt Packet recieved from netfilter queue
    def analyze_tcp_ip(self, pkt):
        ip_pkt = IP(pkt.get_payload())
        if ip_pkt.haslayer(TCP):
            tran_pkt = ip_pkt[TCP]
            protocol = 'TCP'
        elif ip_pkt.haslayer(UDP):
            tran_pkt = ip_pkt[UDP]
            protocol = 'UDP'
        else:
            self.reject_packet(pkt, '\nPacket rejected\n' + ip_pkt.show(dump=True))
            return

        sport = tran_pkt.sport
        dport = tran_pkt.dport
        attributes = {
            'source address': ip_pkt.src,
            'destination address': ip_pkt.dst,
            'protocol': protocol,
            'sport': str(sport),
            'dport': str(dport)
        }

        drop = self.compare_with_rules_version2(attributes)

        conf = Conf()
        drop = False
        
        for rule in conf._list_of_rules:
            if ip_pkt.src == rule.get_src() \
            and ip_pkt.dst == rule.get_dst() \
            and (ip_pkt.haslayer(TCP) and rule.get_protocol() == 'tcp'
            or ip_pkt.haslayer(UDP) and rule.get_protocol() == 'udp') \
            and (ip_pkt.haslayer(TCP) and str(tcp_pkt.dport) == rule.get_dport()
            or ip_pkt.haslayer(UDP) and str(udp_pkt.dport) == rule.get_dport()):
                drop = True
                pkt.drop()
        if not drop:
            if dport == MODBUS_SERVER_PORT:
                payload = bytes(tran_pkt.payload)
                drop = self.analyze_modbus_message(payload)
            elif sport == MODBUS_SERVER_PORT:
                drop = False
            elif dport == SLMP_SERVER_PORT:
                drop = False
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
            match = True
            if attributes['protocol'] in ['TCP', 'UDP']:
                if rule['protocol'] == attributes['protocol']:
                    if rule['source address'] != 'ANY':
                        if attributes['source address'] != rule['source address']:
                            match = False
                    if match and rule['destination address'] != 'ANY':
                        if attributes['destination address'] != rule['destination address']:
                            match = False
                    if match and rule['dport'] != 'ANY':
                        if attributes['dport'] != rule['dport']:
                            match = False
                    if match and rule['sport'] != 'ANY':
                        if attributes['sport'] != rule['sport']:
                            match = False
                else:
                    match = False
            elif attributes['protocol'] == 'MODBUS':
                if rule['protocol'] == 'MODBUS':
                    if attributes['command'] != rule['command']:
                        match = False
                    if match and rule['starting address'] == 'ANY':
                        if rule['quantity'] != 'ANY':
                            if rule['comparison'] == 'MAX':
                                match = int(attributes['quantity']) < int(rule['quantity'])

                            if rule['comparison'] == 'EQUAL':
                                match = int(attributes['quantity']) == int(rule['quantity'])

                            if rule['comparison'] == 'MIN':
                                match = int(attributes['quantity']) > int(rule['quantity'])

                    if match and rule['starting address'] != 'ANY':
                        rule_start = int(rule['starting address'])
                        request_start = int(attributes['starting address'])
                        if rule['quantity'] != 'ANY':
                            rule_end = rule_start + int(rule['quantity']) - 1
                            rule_range = range(rule_start, rule_end + 1)
                            request_end = request_start + int(attributes['quantity']) - 1
                            if rule['comparison'] == 'MAX':
                                match = request_start in rule_range and request_end < rule_end
                            if rule['comparison'] == 'EQUAL':
                                match = request_start in rule_range and request_end == rule_end
                            if rule['comparison'] == 'MIN':
                                match = request_start in rule_range and request_end > rule_end
                        else:
                            match = request_start >= rule_start
                else:
                    match = False
            # simple rule checking, no final rule structure yet
            elif attributes['protocol'] == 'SLMP':
                if rule['protocol'] == 'SLMP':
                    #if rule['direction'] == attributes['direction']
                    if rule['command'] != attributes['command']:
                        match = False

                
            else:
                match = False
            if match:
                drop = False
                break
        return drop



  

    def compare_with_rules_version2(self, attributes):
        for rule in self.rules:
            print("\n\nRULE:", rule, "\n")
            print("ATTR:",attributes, "\n")

            match = True
            for attr in attributes:
                
                if attr in rule:
                    print("1.   ",attr, "=", attributes[attr])
                    
                    if rule[attr] != 'ANY':
                        if rule[attr] == "MAX":
                            match = int(attributes['quantity']) < int(rule['quantity'])
                        elif rule[attr] == "EQUAL":
                            match = int(attributes['quantity']) == int(rule['quantity'])
                        elif rule[attr] == "MIN":
                            match = int(attributes['quantity']) > int(rule['quantity'])
                        else:
                            match = (rule[attr] == attributes[attr])
                else:
                    print("ANY")
                    match = False

            if match:
                break

        drop = not match
        print("\n\nPACKET DROP:", drop)

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
            function_code = str(int(payload[7]))
            starting_address = str(int.from_bytes(payload[8:10], 'little'))
            quantity = str(int.from_bytes(payload[11:13], 'little'))

            attributes = {
                'protocol': 'MODBUS',
                'command': function_codes2names[function_code],
                'starting address': starting_address,
                'quantity': quantity
            }
            return self.compare_with_rules(attributes)
        else:
            return False


    def analyze_slmp_message(self, payload):
        function_codes2names = { 
            '0401' : 'Read',
            '1401' : 'Write',
            '0403' : 'Device Read Random',
            '1402' : 'Device Write Random',
            '0406' : 'Device Read (Batch)', #block
            '1406' : 'Device Write (Batch)' #block'
        }
        subcommand_names = {
            1 : "Read from bit dev in 1 point units",
            3 : "Read from bit dev in 1 point units",
            0 : "Read from bit dev in 16 point units",
            2 : "Read from word devices in 1 word units"
        }

        req_data_len = str(int(payload[16:20]))
        command = str(int(payload[22:26]))
        subcommand =  str(int(payload[26:30]))

        attributes = {
                'protocol': 'SLMP',
                'command': function_codes2names[command],
                'subcommand': subcommand_names[subcommand]
            }
        
     
        

        return self.compare_with_rules(attributes)
    # 0x50 0x0  - subheader 
    # 0x0 0xff - request dest net/station 
    # 0xff 0x3 - request destination module
    # 0x0 - request destination multidrop No. 
    # 0xc 0x0 - request data length 12 bytes
    # 0x4 0x0 - monitoring timer
    # ^^^ 22 BYTES 
    # 
    #   0x1 0x4                0x0 0x0         0x32 0x0               0x0 0xa8              0x1 0x0                 12 BYTES TOTAL, CORRECT LEN
    # |22-26 READ|   | 26-30 READ IN WORDS|    | HEAD DEV NO.|      | DEV CODE const |    | NO OF DEV POINTS |        



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

#     nfqueue = NetfilterQueue()
#     nfqueue.bind(1, fire.analyze_headers)

    try:
        nfqueue.run()
        fd = nfqueue.get_fd()
        print(type(fd))
    except KeyboardInterrupt:
        print('')
    nfqueue.unbind()
