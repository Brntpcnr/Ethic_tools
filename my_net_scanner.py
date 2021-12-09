import scapy.all as scapy

#to match mac ve ip adresses we will use arp and we will broadcast with sending signals
#1)creating an arp request, arp packet is the first step
#2)broadcast, broadcasting so sending signals
#3)response, using the response we get

arp_request_packet = scapy.ARP(pdst="10.0.2.1/24")
#scapy.ls(scapy.ARP)
broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
#scapy.ls(scapy.Ether())
combined_packet = broadcast_packet/arp_request_packet
#scapy dilinde bu combined iki paketi birleştirip tek paket haline getirir
(answered_list,unanswered_list) = scapy.srp(combined_packet,timeout=1)
answered_list.summary()
#print(list(answered_list)) bunu da diyebilirsin
