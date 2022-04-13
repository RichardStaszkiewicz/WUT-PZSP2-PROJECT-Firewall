## @package FIRE
## @author PZSP2-22L Firewall Team
## @date 10.04.2022
## @copyright All rights reserved
# Module implements Firewall executive.

# Basing on NetFilter the messages are being filtered
# on application layer after being judged by a configuration
# rules.


from netfilterqueue import NetfilterQueue


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
class FIRE(object):

    ## Constructor
    # @param self The object pointer
    def __init__(self) -> None:
        pass

    ## Method forwarding the accepted message packeges onward to a defended subnet
    # @param self The object pointer
    # @param message The network message fulfiling the firewall requirenments to be send onward
    def accept_message(self, message : NetMessage):
        for pkt in NetMessage.packets:
            pkt.accept()

    ## Method rejecting the given message due to some error
    # @param self The object pointer
    # @param message The network message fulfiling the firewall requirenments to be send onward
    def reject_message(self, message : NetMessage, error):
        pass

def print_and_accept(pkt):
    print(pkt)
    pkt.accept()

if __name__ == "__main__":
    # IP Tables configuration: (should work imo)
    # iptables -I INPUT -d 192.168.0.0/24 -j NFQUEUE --queue-num 1
    nfqueue = NetfilterQueue()
    nfqueue.bind(1, print_and_accept)
    try:
        nfqueue.run()
    except KeyboardInterrupt:
        print('')
    nfqueue.unbind()