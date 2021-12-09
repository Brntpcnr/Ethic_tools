import scapy.all as scapy
import optparse

def get_user_input():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-i","--ipadress",dest="ip_adress",help="Enter IP Adress")

    (user_input,arguments) = parse_object.parse_args()

    if not user_input.ip_adress:
        print("Enter IP Adress")

    return user_input

def scan_my_network(ip):
    arp_request_packet = scapy.ARP(pdst=ip)
    #scapy.ls(scapy.ARP)
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    #scapy.ls(scapy.Ether())
    combined_packet = broadcast_packet/arp_request_packet
    #scapy dilinde bu combined iki paketi birleştirip tek paket haline getirir
    (answered_list,unanswered_list) = scapy.srp(combined_packet,timeout=1)
    answered_list.summary()
    #print(list(answered_list)) bunu da diyebilirsin
user_ip_adress = get_user_input()
scan_my_network(user_ip_adress.ip_adress)