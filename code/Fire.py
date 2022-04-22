## @package FIRE
## @author PZSP2-22L Firewall Team
## @date 10.04.2022
## @copyright All rights reserved
# Module implements Firewall executive.

# Basing on NetFilter the messages are being filtered
# on application layer after being judged by a configuration
# rules.
from netfilterqueue import NetfilterQueue
from scapy.all import *

## Documentation of NetMessage
#
# NetMessage is a class storing a composed, readable message
# along with the packages upholding it
from scapy.layers.inet import IP, TCP

from scapy.layers.l2 import Ether


class NetMessage:
    ## Constructor
    # @param self The object pointer
    def __init__(self) -> None:
        pass


## Documentation of FIRE
#
# FIRE is an class containing all firewall executive functionalities
class Fire(object):

    ## Constructor
    # @param self The object pointer
    def __init__(self) -> None:
        pass

    ## Method analyzing packets in terms of TCP/IP rules
    # @param self The object pointer
    # @param pkt Packet recieved from netfilter queue

    def analyze_headers(self, pkt):
        ip_pkt = IP(pkt.get_payload())
        if ip_pkt.haslayer(TCP):
            tcp_pkt = ip_pkt[TCP]
            ip_pkt.remove_payload()
            tcp_pkt.remove_payload()
            ip_pkt /= tcp_pkt
            print(ip_pkt.show(dump=True))

        pkt.accept()

    ## Method reading packets from queue until a complete message is formed
    # @param self The object pointer
    # @returns NetMessage object
    def read_message(self):
        pass

    ## Method analyzing complete message under firewall rules
    # @param self The object pointer
    # @message NetMessage object consisting of intercepted packets
    def analyze_message(self, message: NetMessage):
        pass

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


if __name__ == "__main__":

    # IP Tables configuration: (should work imo)
    # iptables -I INPUT -d 192.168.0.0/24 -j NFQUEUE --queue-num 1

    fire = Fire()
    nfqueue = NetfilterQueue()
    nfqueue.bind(1, fire.analyze_headers)

    try:
        nfqueue.run()
        fd = nfqueue.get_fd()
        print(type(fd))
    except KeyboardInterrupt:
        print('')
    nfqueue.unbind()
