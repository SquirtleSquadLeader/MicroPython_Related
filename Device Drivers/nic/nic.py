import struct, socket, network, time, uasyncio, _thread
from secrets import Secret

"""
Dont forget to make your own secrets
"""
class NIC:
    def __init__(self):
        # Initialize WLAN
        wlan = network.WLAN(network.STA_IF) 
        network_in_range_FLAG = False
        wlan_ifconfig = []
        wlan_ip = ''
        wlan_subnetmask = '' 

        # Activates the WLAN
        wlan.active(True) 

        # Perform a WiFi Access Points scan , returns list of tuples
        accessPoints_list_of_tuples = wlan.scan() 

        # Define desired network connection
        my_network = Secret()
        ssid = my_network.ssid
        passkey = my_network.password
        place_in_list = False

        # Check if network in range
        for counter in range(0, len(accessPoints_list_of_tuples)):
            if ssid in accessPoints_list_of_tuples[counter][0]:
                network_in_range_FLAG = True
                place_in_list = int(counter)
                print(ssid,"is in range")

        # Establish WLAN connection
        if not wlan.isconnected() and network_in_range_FLAG is True:
            wlan.connect(ssid, passkey)
            print("Waiting for connection...")
            while not wlan.isconnected():
                time.sleep(1)
                print("Trying to connect...")

        # Print connection details to console
        wlan_ifconfig = list(wlan.ifconfig())
        wlan_ip = wlan_ifconfig[0]
        wlan_subnetmask = wlan_ifconfig[1]
        print("Connection to", ssid, "established.")
        print("IP Address:", wlan_ip, "     Subnet Mask:", wlan_subnetmask)

        # Create UDP socket object
        self.udp_Tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def transmit(self, data, ip_address:str='192.168.1.18', port:int=12345):
        address = (ip_address, port)
        self.udp_Tx.sendto(data, address)

    def udp_transmit_test(self):
        # Destination address details
        dest_addr = '192.168.1.18'
        dest_port = 12345
        counter = 0
        # Transmit data to destination
        while counter < 1_000:
            try:
                # Create data string and encode it for transmission
                data = str(counter).encode()
                self.udp_Tx.sendto(data, (dest_addr, dest_port))
                counter = counter + 1                  
            except:
                print("Sending error...")
                pass
