import socket
import sys

def CreateConnect(host, port, server=False):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if(server):
        port = socket.htons(port)
        s.bind((host, port))
    else:
        addrinfo = socket.getaddrinfo(host, port, socket.AF_INET, socket.SOCK_STREAM)
        family, socktype, proto, canonname, sockaddr = addrinfo[0]
        ip, port = sockaddr
        port = socket.htons(port)
        s.connect((ip, port))
    return s

def SendMessage(sock, message):
    message = bytes(message + '\n', "utf-8")
    try :
        sock.sendall(message) #Send the whole string
    except socket.error:
        print('Message failed to send') #Send failed
        sys.exit()
    return

# readlines function from Dr.Fyre's sumPython example
# pulled from https://synack.me/blog/using-python-tcp-sockets
# retrieved 11/15/2020
# renamed to RecvMessage for group use
def RecvMessage(sock, recv_buffer=4096, delim='\n'):
    buffer = ''
    data = True
    while data:
        data = sock.recv(recv_buffer)
        buffer += data.decode("utf-8") 

        while buffer.find(delim) != -1:
            line, buffer = buffer.split('\n', 1)
            yield line
    return


def ClientClose(sock):
    SendMessage(sock, 'BYE')
    sock.close()
    return
