# importing the scapy library
import scapy.all as scapy


# for ping request response, simply captures the first two packets, as I pinged 8.8.8.8, pinging my site didnt work

def ping_request_response(interface, ip_address):
    filter = "host " + ip_address
    filename = "PING_Request_Response_2001CS41.pcap"
    capture = scapy.sniff(iface=interface, filter=filter, count=2)
    print(capture.summary())
    scapy.wrpcap(filename, capture)


a = -1

# function to capture tcp closing handshake, checks for ip_addr, and first packet with FA flag, captures next two packets irrespective of flag
# arr to store seq of tcp packets to avoid retransmitted packet


def prcoesstcpclose(packet):
    global a
    global ip_address
    global arr
    filename = "TCP_handshake_close_2001CS41.pcap"
    if ((packet[scapy.IP].src == ip_address or packet[scapy.IP].dst == ip_address) and (packet[scapy.TCP].flags == 0x011 or a >= 0)):
        x = True
        for y in arr:
            if (y == packet[scapy.TCP].seq):
                x = False
        if (x == True):
            print(packet)
            scapy.wrpcap(filename, packet, append=True)
            a += 1
            arr.append(packet[scapy.TCP].seq)
    if (a == 2):
        return True
    else:
        return False


tcpopencnt = 0
arr1 = []

# captures first 3 tcp packets, again arr1 to avoid duplicate packets, and tcpopencnt to count, filter used ip address in function


def processtcpopen(packet):
    global ip_address
    global tcpopencnt
    global arr1
    filename = "TCP_3_way_handshake_2001CS41.pcap"
    if (tcpopencnt < 3 and (packet[scapy.IP].src == ip_address or packet[scapy.IP].dst == ip_address)):
        x = True
        for y in arr1:
            if (y == packet[scapy.TCP].seq):
                x = False
        if (x == True):
            print(packet)
            scapy.wrpcap(filename, packet, append=True)
            tcpopencnt += 1
            arr1.append(packet[scapy.TCP].seq)


ip_address = ""
x = 0

# dns req response, function, saves 2 packets, and gets ip address from dns response to get tcp handshakes, after 2 packets calls processtcpopen function


def process_dns_request_response(packet):
    global x
    global ip_address
    filename = "DNS_Request_Response_2001CS41.pcap"
    if (x < 2 and packet.haslayer(scapy.DNSQR) and packet[scapy.DNSQR].qtype == 1 and ("kompas" in str(packet[scapy.DNSQR].qname))):
        print(packet)
        scapy.wrpcap(filename, packet, append=True)
        if (x == 1):
            ip_address = packet[scapy.DNSRR].rdata
        x += 1
    if (x == 2):
        processtcpopen(packet)

# function filters tcp and dns packets, due to port numbers,


def dns_tcp(interface):
    global ip_address
    filter = "port 53 or port 443"
    scapy.sniff(iface=interface, store=False, filter=filter,
                prn=process_dns_request_response, stop_filter=prcoesstcpclose)


arptarget = ""

# capture arp request packet, first then store its target, to get the response packet correctly
# arp request response done together, as could conviniently see arp packets on my system
# ping also works to capture


def processarp(packet):
    filename = "ARP_request_response_2001CS41.pcap"
    filename1 = "ARP_2001CS41.pcap"
    global arptarget
    if (packet.haslayer(scapy.ARP) and arptarget == "" and packet[scapy.ARP].op == 1):
        arptarget = packet[scapy.ARP].pdst
        print(packet)
        scapy.wrpcap(filename, packet, append=True)
        scapy.wrpcap(filename1, packet, append=True)

# arp stop to get response of target ip


def arpstop(packet):
    filename = "ARP_request_response_2001CS41.pcap"
    if (packet.haslayer(scapy.ARP) and packet[scapy.ARP].psrc == arptarget):
        print(packet)
        scapy.wrpcap(filename, packet, append=True)
        return True
    else:
        return False

# sniff for arp, call appropriate functions


def arp(interface):
    scapy.sniff(iface=interface, prn=processarp, stop_filter=arpstop)

# function to stop ftp capture


def ftpstop(packet):
    if (b == 2):
        return True
    else:
        return False


# array to avoid duplicate capture of ftp closing handshake
arr = []
b = 0
# store a previous packet of ftp protocol so that when FA is found, ftp goodbye can be written
pack = scapy.packet
# ftp packets appear as tcp PA flagged packets in scapy, filtered accordingly to get 8 packets at start and 4 at end


def prcoessftp(packet):
    global b
    global arr
    filename = "FTP_connection_close_2001CS41.pcap"
    global pack
    if ((packet[scapy.TCP].flags == 0x011) or b >= 0):
        x = True
        for y in arr:
            if (y == packet[scapy.TCP].seq):
                x = False
        if (x == True):
            if (b == -1):
                print(packet)
                scapy.wrpcap(filename, pack, append=True)
            print(packet)
            scapy.wrpcap(filename, packet, append=True)
            b += 1
            arr.append(packet[scapy.TCP].seq)
    if (packet[scapy.TCP].flags == 0x018):
        pack = packet


def ftpconstart(packet):
    global b
    filename = "FTP_Connection_start_2001CS41.pcap"
    if (b < 3):
        print(packet)
        scapy.wrpcap(filename, packet, append=True)
        b += 1
        return False
    elif (b < 8):
        if (packet[scapy.TCP].flags == 0x018):
            print(pack)
            scapy.wrpcap(filename, packet, append=True)
            b += 1
            return False
    else:
        b = -1
        return True


def ftp(interface, ip_address):
    filter = "port 21 and host " + ip_address
    scapy.sniff(iface=interface, filter=filter, stop_filter=ftpconstart)
    scapy.sniff(iface=interface, filter=filter,
                prn=prcoessftp, stop_filter=ftpstop)


def sniff(interface):
    global ip_address
    print("Enter 0 for DNS and TCP, 1 for ARP, 2 for PING, 3 for FTP")
    i = input()
    if (i == "0"):
        print("Search for site in private tab to get its dns query response tcp open and close using kompas.com according to doc")
        dns_tcp(interface)
    elif (i == "1"):
        print("simply waited for arp packets sent periodically")
        arp(interface)
    elif (i == "2"):
        print("Ping 8.8.8.8 to capture")
        ping_request_response(interface, "8.8.8.8")
    elif (i == "3"):
        print(
            "Connect to ftp server (used ftp seed@192.168.64.4 on my machine, code according to it")
        # bridge100 is the iface for vm on which ftp server is set, and 192.168.64.3 is the IP
        ftp("bridge100", "192.168.64.4")
    else:
        print("Invalid Input")


def main():
    interface = "en0"
    sniff(interface)


if __name__ == "__main__":
    main()
