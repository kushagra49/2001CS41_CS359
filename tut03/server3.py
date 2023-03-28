import socket			
import select 

socket_list=[]
sock_write=[]
socket_status={}
socket_input={}

def get_input(c):
    if(socket_status[c]==0):
        input=c.recv(1024).decode()
        print("Client",c.getpeername(),input)
        socket_input[c]=input
    else:
        cont=c.recv(1024).decode()
        socket_input[c]=cont
        
def send_output(c):
    if(socket_status[c]==0):
        try:
            inp=socket_input[c]
        except:
            return
        try:
            ans=str(eval(inp))
        except:
            ans="Invalid input format"
        print("Response",c.getpeername(),ans)
        c.send(ans.encode())
        socket_status[c]=1
        del socket_input[c]
    else:
        try:
            cont=socket_input[c]
        except:
            return
        if(cont=="n"):
            print("Connection closed with client", c.getpeername())
            socket_list.remove(c)
            c.close()
            sock_write.remove(c)
        elif(cont=="y"):
            c.send('Thank you for connecting\nProvide your input: '.encode())
            socket_status[c]=0
            del socket_input[c]
def rcv_connection(s):
    c,addr=s.accept()
    c.send('Thank you for connecting\nProvide your input: '.encode())
    print ('Got connection from', addr )
    socket_list.append(c)
    sock_write.append(c)
    socket_status[c]=0
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		
    print ("Socket successfully created")
    port = 12345	
    s.bind(('', port))		
    print ("socket binded to %s" %(port))
    s.listen()
    socket_list.append(s)
    print("Socket is listening..")
    while(True):
        read,write,err=select.select(socket_list,sock_write,[],0)
        for x in read:
            if(x==s):
                rcv_connection(s)
            else:
                get_input(x)
        for x in write:
            send_output(x)
            
                
                

                
if __name__ == "__main__":
    main()
