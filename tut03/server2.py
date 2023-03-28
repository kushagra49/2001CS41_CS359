import socket			
import threading

def calculator(c,addr):

    while(True):	
        c.send('Thank you for connecting\nProvide your input: '.encode())
        input=c.recv(1024).decode()
        print("Client",addr,input)
        try:
            ans=str(eval(input))
        except:
            ans="Invalid input format"
        print("Response",addr,ans)
        c.send(ans.encode())
        cont=c.recv(1024).decode()
        if(cont=="n"):
            print("Connection closed with client", addr)
            c.close()
            break
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		
    print ("Socket successfully created")
    port = 12345	
    s.bind(('', port))		
    print ("socket binded to %s" %(port))
    s.listen()
    print("Socket is listening..")
    while(True):
        c,addr=s.accept()
        print ('Got connection from', addr )
        t1=threading.Thread(target=calculator,args=(c,addr))
        t1.start()
if __name__ == "__main__":
    main()
