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
from Conf import Conf
from Logger import Logger
from Rules import Rule
import json


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
    def __init__(self) -> None:
        self.logger = Logger("../logs/events.log")

    ## Method analyzing packets in terms of TCP/IP rules
    # @param self The object pointer
    # @param pkt Packet recieved from netfilter queue
    def analyze_headers(self, pkt):
        ip_pkt = IP(pkt.get_payload())
        if ip_pkt.haslayer(TCP):
            tcp_pkt = ip_pkt[TCP]
        elif ip_pkt.haslayer(UDP):
            udp_pkt = ip_pkt[UDP]
        else:
            self.logger.log("\nPacket accepted\n" + ip_pkt.show(dump=True))
            print("\nPacket accepted\n" + ip_pkt.show(dump=True))
            pkt.accept()

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
                self.logger.log("\nPacket rejected\n" + ip_pkt.show(dump=True), logging.WARNING)
                print("\nPacket rejected\n" + ip_pkt.show(dump=True))
                pkt.drop()
        if not drop:
            self.analyze_message(pkt)


    ## Method reading packets from queue until a complete message is formed
    # @param self The object pointer
    # @returns NetMessage object
    def read_message(self, pkt):
        pass

    ## Method analyzing complete message under firewall rules
    # @param self The object pointer
    # @param pkt Packet recieved from netfilter queue
    def analyze_message(self, pkt):
        ip_pkt = IP(pkt.get_payload())
        tcp_pkt = ip_pkt[TCP]
        conf = Conf()
        client_address = '127.0.0.1'
        drop = False
        if ip_pkt.src == client_address:
            message_bytes = bytes(tcp_pkt.payload)
            if message_bytes[:4] == b'\x00\x01\x00\x00':
                function_code = int(message_bytes[7])
                starting_address = int.from_bytes(message_bytes[8:10], 'little')
                quantity = int.from_bytes(message_bytes[11:13], 'little')
                for rule in conf._list_of_rules:
                    if function_code == int(rule.get_function_code()) \
                    and starting_address == int(rule.get_starting_address()) \
                    and quantity > int(rule.get_register_quantity()):
                        drop = True
                        self.logger.log("Packet rejected\n" + ip_pkt.show(dump=True), logging.WARNING)
                        print("\nPacket rejected\n" + ip_pkt.show(dump=True))
                        pkt.drop()
                        break
        if not drop:
            self.logger.log("\nPacket accepted\n" + ip_pkt.show(dump=True))
            print("\nPacket accepted\n" + ip_pkt.show(dump=True))
            pkt.accept()


    ## Method reading rules from config file
    #
    #
    def update_rules(self) -> None:
        f = open('Conf_tmp.json')
        data = json.load(f)
        self.rules.clear()
        for rule in data:
            new_rule = Rule(rule['id'], rule["src"], rule['dst'], rule['protocol'], rule['dport'], rule['direction'], rule['action'])
            self.rules.append(new_rule)


    ## Method forwarding the accepted message packeges onward to a defended subnet
    # @param self The object pointer
    # @param message The network message fulfiling the firewall requirenments to be send onward
    def accept_message(self, message: NetMessage):
        for pkt in NetMessage.packets:
            pkt.accept()

    ## Method rejecting the given message due to some error
    # @param self The object pointer
    # @param message The network message fulfiling the firewall requirenments to be send onward
    def reject_message(self, message: NetMessage, error):
        pass


fire = Fire()

if __name__ == "__main__":

    # IP Tables configuration: (should work imo)
    # iptables -I INPUT -d 192.168.0.0/24 -j NFQUEUE --queue-num 1

    nfqueue = NetfilterQueue()
    nfqueue.bind(1, fire.analyze_headers)

    try:
        nfqueue.run()
        fd = nfqueue.get_fd()
        print(type(fd))
    except KeyboardInterrupt:
        print('')
    nfqueue.unbind()
