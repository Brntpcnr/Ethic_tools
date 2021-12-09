import scapy.all as scapy
from scapy_http import http

def listen_packets(interface):

    scapy.sniff(iface=interface,store=False,prn=analyze_packets) #sniff listens the coming packets, kinda sniffs it actually. Store false saves the packets we get 
    #prn=callback function, means I will listen the coming packets, to which function should I send them to

def analyze_packets(packet):
    #packet.show()
    if packet.haslayer(http.HTTPRequest):  #the 3 lines below this makes us directly work with layers(katman)
        if packet.haslayer(scapy.Raw):
            print(packet[scapy.Raw].load)

listen_packets("eth0")

