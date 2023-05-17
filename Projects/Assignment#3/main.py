import socket
import struct


# Unpack Ethernet Frame
def parse_header(raw_data):
    destination, source, protocol = struct.unpack('! 6s 6s H', raw_data[:14])
    return get_mac_addr(destination), get_mac_addr(source), socket.htons(protocol), raw_data[14:]


# Return MAC Address
def get_mac_addr(bytes_addr):
    bytes_addr = map('{:02x}'.format, bytes_addr)
    mac_address = ':'.join(bytes_addr).upper()
    return mac_address


def get_ipv4_packet(data):
    first_byte = data[0]
    version = first_byte >> 4
    header_length = (first_byte & 15) * 4
    ttl, proto, src, dest = struct.unpack('! 8x B B 2x 4s 4s', data[:20])
    return version, header_length, ttl, proto, get_ip_address(src), get_ip_address(dest), data[header_length:]


def get_ip_address(address):
    return '.'.join(map(str, address))


def main():
    # Socket is a Python Library to create Raw socket.
    # Socket is something that opens up the interface to play with network in local or foreign level
    # socket has several Param -
    # family - A socket interface which family we should consider. Essentially indicates in which layer our socket should work.
    # type - Means what type of data it should collect. In our case it will be Raw data.
    # proto - Which protocol to be captured. 3 Means Ethernet Protocol. We need IPv4 and MAC address (ARP)
    conn = socket.socket(family=socket.AF_PACKET, type=socket.SOCK_RAW, proto=socket.ntohs(3))
    while True:
        # 65535 = How many bytes of data should be captured in a single network call.
        # raw_data = Raw Byte Object, address = source address
        raw_data, address = conn.recvfrom(65535)
        # Method to get mac address, protocol, rest of the information
        dest_mac, src_mac, proto, data = parse_header(raw_data=raw_data)
        # Method to get IP version, header_length, Time To Live, Source and Dest MAC, Data
        version, header_length, ttl, proto, start_ip, dest_ip, data = get_ipv4_packet(data=data)
        print("\n========= L2 Frame ==============")
        print("Source Mac: ", src_mac)
        print("Destination Mac: ", dest_mac)
        print("Protocol: ", proto)
        print("========= L3 Frame ==============")
        print("Version: ", version)
        print("Header Length: ", header_length)
        print("Source IP: ", start_ip)
        print("Destination IP: ", dest_ip)
        print("=========================================\n")


if __name__ == '__main__':
    main()
