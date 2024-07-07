import subprocess
import optparse
import random
import re
import sys

def generate_random_mac():
    mac = [0x00, 0x16, 0x3e,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))

def get_current_mac(interface):
    result = subprocess.run(["ifconfig", interface], capture_output=True, text=True)
    mac_address_search = re.search(r"ether ([0-9a-fA-F:]{17})", result.stdout)
    if mac_address_search:
        return mac_address_search.group(1)
    else:
        return None

def change_mac(interface, new_mac):
    result = subprocess.run(["ifconfig", interface, "hw", "ether", new_mac], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error changing MAC address: {result.stderr}")
        return False
    return True

parse_object = optparse.OptionParser()
parse_object.add_option("-i", "--interface", dest="interface", help="Interface to change")
parse_object.add_option("-m", "--mac", dest="mac_address", help="MAC address to change")
parse_object.add_option("-r", "--random", action="store_true", dest="random", help="Generate a random MAC address")
parse_object.add_option("-s", "--show", action="store_true", dest="show", help="Show the current MAC address")

(user_inputs, arguments) = parse_object.parse_args()

user_interface = user_inputs.interface
user_mac_address = user_inputs.mac_address


if user_inputs.show:
    if user_interface:
        current_mac_address = get_current_mac(user_interface)
        if current_mac_address:
            print(f"Current MAC: {current_mac_address}")
        else:
            print("Could not retrieve the current MAC address.")
    else:
        print("Please provide the interface to show the MAC address.")
    sys.exit(0)


if user_inputs.random:
    user_mac_address = generate_random_mac()
    pass

if user_interface:
    current_mac_address = get_current_mac(user_interface)
    if current_mac_address:
        pass
    else:
        print("Could not retrieve the current MAC address.")

if user_interface and user_mac_address:
    subprocess.run(["ifconfig", user_interface, "down"])
    if not change_mac(user_interface, user_mac_address):
        print("Please try another MAC address.")
        sys.exit(1)
    subprocess.run(["ifconfig", user_interface, "up"])

    print("\nMAC changer successful!")
    print("\nInterface:             " + user_interface)
    print(f"Current MAC address:   {current_mac_address}")
    print("New MAC address:       " + user_mac_address)

else:
    print("Please provide both interface and MAC address (or use the --random option to generate a random MAC address).")
