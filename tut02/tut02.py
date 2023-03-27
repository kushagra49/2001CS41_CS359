import scapy.all as scapy
import socket
y=0
def process_ping_request_response(packet):
    filename="PING_Request_Response_2001CS41.pcap"
    global y
    #print(packet)
    #scapy.wrpcap("test.pcap", packet, append=True)
    if(y<2):
        print(packet)
        scapy.wrpcap(filename, packet, append=True)
        y+=1
def stopping(packet):
    global y
    if(y==2):
        return True
    else:
        return False 

def ping_request_response(interface,ip_address):
    filter="host "+ ip_address
    scapy.sniff(iface=interface, store=False, filter=filter, prn=process_ping_request_response, stop_filter=stopping)


a=-1
def tcpstop(packet):
    global a
    if(a==2):
        return True
    else:
        return False

def prcoesstcpclose(packet):
    global a
    global ip_address
    global arr
    filename="TCP_handshake_close_2001CS41.pcap"
    #print(packet)
    if((packet[scapy.IP].src==ip_address or packet[scapy.IP].dst==ip_address) and (packet[scapy.TCP].flags==0x011 or a>=0)):
        x=True
        for y in arr:
            if(y==packet[scapy.TCP].seq):
                x=False
        if(x==True):
            print(packet)
            scapy.wrpcap(filename, packet, append=True)
            a+=1
            arr.append(packet[scapy.TCP].seq)
tcpopencnt=0
arr1=[]
def processtcpopen(packet):
    global ip_address
    global tcpopencnt
    global arr1
    filename="TCP_3_way_handshake_2001CS41.pcap"
    if(tcpopencnt<3 and (packet[scapy.IP].src==ip_address or packet[scapy.IP].dst==ip_address)):
        x=True
        for y in arr1:
            if(y==packet[scapy.TCP].seq):
                x=False
        if(x==True):
            print(packet)
            scapy.wrpcap(filename, packet, append=True)
            tcpopencnt+=1
            arr1.append(packet[scapy.TCP].seq)
ip_address=""
x=0
def process_dns_request_response(packet):
    global x
    global ip_address
    filename="DNS_Request_Response_2001CS41.pcap"
    #scapy.wrpcap(filename, packet, append=True)
    if(x<2 and packet.haslayer(scapy.DNSQR) and packet[scapy.DNSQR].qtype==1 and ("kompas" in str(packet[scapy.DNSQR].qname))):
        print(packet)
        scapy.wrpcap(filename, packet, append=True)
        if(x==1):
            ip_address=packet[scapy.DNSRR].rdata
        x+=1
    if(x==2):
        processtcpopen(packet)
        prcoesstcpclose(packet)



def dns_tcp(interface):
    global ip_address
    filter = "port 53 or port 443"
    scapy.sniff(iface=interface, store=False, filter=filter, prn=process_dns_request_response, stop_filter=tcpstop)

        
# def tcp_open(ip_address,interface):
#     filter="host "+ ip_address
#     filename="TCP_3_way_handshake_2001CS41.pcap"
#     capture=scapy.sniff(iface=interface, filter=filter, count=3)
#     print(capture.summary())
#     scapy.wrpcap(filename,capture)

# def tcp_close(ip_address,interface):
#     filter="host "+ip_address
#     scapy.sniff(iface=interface, filter=filter, prn=prcoesstcp, stop_filter=tcpstop)

arptarget=""
def processarp(packet):
    filename="ARP_request_response_2001CS41.pcap"
    filename1="ARP_2001CS41.pcap"
    global arptarget
    if(packet.haslayer(scapy.ARP) and arptarget=="" and packet[scapy.ARP].op==1):
        arptarget=packet[scapy.ARP].pdst
        print(packet)
        scapy.wrpcap(filename, packet, append=True)
        scapy.wrpcap(filename1, packet, append=True)
def arpstop(packet):
    filename="ARP_request_response_2001CS41.pcap"
    if(packet.haslayer(scapy.ARP) and packet[scapy.ARP].psrc==arptarget):
        print(packet)
        scapy.wrpcap(filename, packet, append=True)        
        return True
    else:
        return False
def arp(interface):
    scapy.sniff(iface=interface, prn=processarp, stop_filter=arpstop)


def ftpstop(packet):
    if(b==2):
        return True
    else:
        return False
arr=[]
b=0
pack=scapy.packet
def prcoessftp(packet):
    global b
    global arr
    filename="FTP_connection_close_2001CS41.pcap"
    #print(packet)
    global pack
    if((packet[scapy.TCP].flags==0x011)or b>=0):
        x=True
        for y in arr:
            if(y==packet[scapy.TCP].seq):
                x=False
        if(x==True):
            if(b==-1):
                print(packet)
                scapy.wrpcap(filename, pack, append=True)
            print(packet)
            scapy.wrpcap(filename, packet, append=True)
            b+=1
            arr.append(packet[scapy.TCP].seq)
    if(packet[scapy.TCP].flags==0x018):
        pack=packet
def ftpconstart(packet):
    global b
    filename="FTP_Connection_start_2001CS41.pcap"
    #print(packet)
    if(b<3):
        print(packet)
        scapy.wrpcap(filename, packet, append=True)
        b+=1
        return False
    elif(b<8):
        if(packet[scapy.TCP].flags==0x018):
            print(pack)
            scapy.wrpcap(filename, packet, append=True)
            b+=1
            return False
    else:
        b=-1
        return True
def ftp(interface,ip_address):
    filter="port 21 and host "+ ip_address
    scapy.sniff(iface=interface,filter=filter,stop_filter=ftpconstart)
    scapy.sniff(iface=interface, filter=filter, prn=prcoessftp, stop_filter=ftpstop)


def sniff(interface):
    #ip_address=socket.gethostbyname(hostname)
    global ip_address
    print("Enter 0 for DNS and TCP, 1 for ARP, 2 for PING, 3 for FTP")
    i=input()
    if(i=="0"):
        print("Search for site in private tab to get its dns query response tcp open and close using kompas.com according to doc")
        dns_tcp(interface)
    elif(i=="1"):
        print("simply waited for arp packets sent periodically")
        arp(interface)
    elif(i=="2"):
        print("Ping 8.8.8.8 to capture")
        ping_request_response(interface,"8.8.8.8")
    elif(i=="3"):
        print("Connect to ftp server (used ftp seed@192.168.64.4 on my machine, code according to it")
        ftp("bridge100","192.168.64.4") #bridge100 is the iface for vm on which ftp server is set, and 192.168.64.3 is the IP
    else:
        print("Invalid Input") 

   

def main():
    interface = "en0"
    sniff(interface)

if __name__ == "__main__":
    main()