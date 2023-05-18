import socket
import struct


# Unpack Ethernet Frame. Take Raw data as input
# struct.unpack - is a method to unpack a certain amount of data in a defined format
# In our case, the amount first 14 bytes. `raw_data[:14]`.
# Because first 14 byte is MAC header ( More detail: https://upload.wikimedia.org/wikipedia/commons/1/13/Ethernet_Type_II_Frame_format.svg)
# And the format is `! 6s 6s H`
# Here, `!` represents the big-endian which means most significant bit should be the first consideration
# 6s indicates to consider a string of 6 bytes in length.
# H indicates the data should be in a short integer form which takes two bytes only.
# The first byte multiplied by 256 and the second byte will just be added with it.
def parse_header(raw_data):
    destination, source, protocol = struct.unpack('! 6s 6s H', raw_data[:14])
    return get_mac_addr(destination), get_mac_addr(source), socket.htons(protocol), raw_data[14:]


# Returns a formatted MAC Address
# The bytes_addr passed as a parameter when called
# The map() function formats the bytes of bytes_addr using a defined format
# In our case it is - :02x
# It will be formatted as zero-padded, two digit hexadecimal representation
# 02 - 2 digit forward-padded by zero
# x - Hexadecimal based number
# ':.join(...) used to combine all those two digits hexadecimal numbers
def get_mac_addr(bytes_addr):
    bytes_addr = map('{:02x}'.format, bytes_addr)
    mac_address = ':'.join(bytes_addr).upper()
    return mac_address


# Return IP Version, Header Length, TTL, Protocol Info, IP address and data
# data[0] is the first byte of the IP Frame. It consists of 8 bits
# Where first 4 bits are version info and last 4 bits are header length
# To get version we need to remove last 4 bits. Thats why right-shifted by 4 places
# To get the header length Bitwise ANDed to remove first 4 bits.
# Multiplied by 4 because the Header Length is specified as 32 bit words in most of the network protocols
# Next we need to unpack the rest of the information from Data. The format is - `! 8x B B 2x 4s 4s`
# Here, `!` represents the big-endian which means most significant bit should be the first consideration
# 8x - is to skip first 8 Bytes. Why?
# Take a look at this picture - https://upload.wikimedia.org/wikipedia/commons/1/13/Ethernet_Type_II_Frame_format.svg
# We are done with version and Header length
# We are not interested in - TOS, Total Length, Identification, and Fragment offset
# TTL located at - 9th Byte position and protocol is at 10th Byte position
# B B stands for taking two unsigned bytes and unpack them as individual value.
# Next 2 byte Header checksum. We are not interested either. Skip this as well.
# 4s indicates to consider a string of 4 bytes in length for IP address.
def get_ipv4_packet(data):
    first_byte = data[0]
    version = first_byte >> 4
    header_length = (first_byte & 15) * 4
    ttl, proto, src, dest = struct.unpack('! 8x B B 2x 4s 4s', data[:20])
    return version, header_length, ttl, proto, get_ip_address(src), get_ip_address(dest), data[header_length:]


# Returns the address in an IP address format
# This maps the str() function to each element of the address tuple and join them using `.`
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
