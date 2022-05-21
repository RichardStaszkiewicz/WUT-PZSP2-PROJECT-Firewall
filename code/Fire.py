## @package FIRE
## @author PZSP2-22L Firewall Team
## @date 10.04.2022
## @copyright All rights reserved
# Module implements Firewall executive.

# Basing on NetFilter the messages are being filtered
# on application layer after being judged by a configuration
# rules.
from copy import deepcopy
from dataclasses import replace
from itertools import count
import logging

from netfilterqueue import NetfilterQueue
from scapy.layers.inet import IP, TCP, UDP, Ether
from Logger import Logger
from Rules import Rule
import json

MODBUS_SERVER_PORT = 5020
SLMP_SERVER_PORT = 1280



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
        f.close()
    

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
        
        drop = self.compare_with_rules(attributes)

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
                payload = bytes(tran_pkt.payload)
                print("PAYLOAD SIZE:",len(payload))
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
        print("\n\nCAPTURED PACKET:  ", attributes)
        for rule in self.rules: 
            match = True
            missed_attr_count = 0

            print("\nRULE:", rule, "\n Attr comparison:")
           
            for attr in attributes:
                if attr in rule:
                    print("-   ",attr, "=", attributes[attr], "RULE", rule[attr])
                    
                    if rule[attr] != 'ANY':
                        if rule[attr] == "MAX":
                            match = int(attributes['quantity']) < int(rule['quantity'])
                        elif rule[attr] == "EQUAL":
                            match = int(attributes['quantity']) == int(rule['quantity'])
                        elif rule[attr] == "MIN":
                            match = int(attributes['quantity']) > int(rule['quantity'])
                        else:
                            match = (rule[attr] == attributes[attr])
                   
                    if not match:
                        print("DID NOT MATCH")
                        break
           
                else:
                    missed_attr_count += 1
                   
            
            # jesli zaden atrybut nie pasowal do rulesa, to znaczy, ze ten rules nie przepusci pakietu
            if missed_attr_count == len(attributes):
                print("All attributes missed")
                match = False
            
            # Jesli przy danym rulesie jest match, to przerwij comparison i przepusc 
            if match:
                drop = False
                print("PACKET DROP:", drop)
                return drop
        

               
        print("\n\nPACKET DROP:", drop)

        #jesli przelecimy przez wszystkie rulesy/ rules= [] to wtedy drop
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
            b'\x01\x04' : 'Read',
            b'\x01\x14' : 'Write',
            # '0403' : 'Device Read Random',
            # '1402' : 'Device Write Random',
            # '0406' : 'Device Read (Batch)', #block
            # '1406' : 'Device Write (Batch)' #block'
        }

        # To Do:
        # Variable length
        subcommand_names = {
            b'\x00' : "Read from bit dev in 16 point units"
            # 1 : "Read from bit dev in 1 point units",
            # 3 : "Read from bit dev in 1 point units",
            # 2 : "Read from word devices in 1 word units"
        }
        attributes = {}
     
        if len(payload) > 0:
            
            print("PAYLOAD", payload.__str__())
            

            command = payload[11:13]
            subcommand = payload[13:14]
            head_dev_no =  payload[14:17]
            dev_code = payload[17:19]
            no_of_dev_pts = payload[19:21]


            attributes = {
                    'protocol': 'SLMP',
                    'command': function_codes2names[command],
                    'subcommand': subcommand_names[subcommand],

                }

            print("COMMAND:", command, "subcommand:", subcommand,"         ", head_dev_no,  "          ",dev_code, "          ", no_of_dev_pts )            
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

#     nfqueue = NetfilterQueue()
#     nfqueue.bind(1, fire.analyze_headers)

    try:
        nfqueue.run()
        fd = nfqueue.get_fd()
        print(type(fd))
    except KeyboardInterrupt:
        print('')
    nfqueue.unbind()
