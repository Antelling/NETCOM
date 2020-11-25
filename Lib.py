"""
Author:                Connor Kistler
Edited By:             Anthony Dellinger
Major:                 Computer Science - Software Development
Creation Date:         11/13/20
Due Date:              11/24/20
Course:                CSC 328
Professor Name:        Dr. Frye
Assignment:            Chat Application
Filename:              Lib.py
Purpose:               This file is intended to be a library of common functions between the client and server of the
                       chat application to facilitate easy communication between the two ends. Included in this library
                       are functions to create and assign connection objects, as well as to send and receive application
                       messages through the connection.
"""
import socket
import sys
"""
Function Name:     CreateConnect()
Description:       Creates a connection object, assigns it appropriately to the port and either address or hostname
                   depending on which end called the function, then returns the connection object ready for use. For
                   the client this use would be sending messages, for the serve this use is to listen for connecting
                   clients.
Parameters:        host - the given hostname for the server either supplied through command-line or hard coded into the server
                   port - the given port number for the connection either supplied through command-line or hard coded to default
                   server - flag to tell which end is creating a connection, defaults to client side
Return Value:      s - returns the created and assigned connection object ready for use
"""
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

"""
Function Name:     SendMessage()
Description:       Sends a message over the connection to the other end of the application along with a message type.
                   Message is formatted to contain the message type delimited by a | then the message delimited by a \n.
                   Message type is used to delineate between messages used for protocols and standard chat messages.
Parameters:        sock - the connection object to send the message over; SendMessage() assumes the connection object has 
                          already been connected to its counterpart on the other end.
                   message - the message to be sent contained in a string; message formatting occurs inside function
                   msgtype - the type of message being sent, defaulted to a standard chat message
Return Value:      n/a
"""
def SendMessage(sock, message="empty", msgtype="MSG"):
    message = bytes(msgtype + "|" + message + '\n', "utf-8")
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
"""
Function Name:       RecvMessage()
Description:         Receives a message over the connection. Data is loaded into the message buffer and then split to ensure the
                     entire message is preserved. The splits are done based on the set delimiters in the message formatting done
                     in SendMessage() in order to properly identify the message type from the message itself, as well as to know
                     when the message ends. Returns the message and the message type.
Parameters:          sock - the connection object to receive the message from; RecvMessage() assumes the connection object has 
                            already been connected to its counterpart on the other end.
                     recv_buffer - the size of the buffer to read the message into; defaults to a reasonable max size for python
                     delim - the end of message delimiter; defaulted to the delimiter used in message formatting for the end of
                             the message
Return Value:        msg - returns the message itself as a string after split is complete
                     msgtype - returns the message type to decide how to handle the message on the receiving side
"""
def RecvMessage(sock, recv_buffer=4096, delim='\n'):
    buffer = ''
    data = True
    while data:
        data = sock.recv(recv_buffer)
        buffer += data.decode("utf-8") 

        while buffer.find(delim) != -1:
            line, buffer = buffer.split('\n', 1)
            msgtype, msg = line.split("|", 1)
            return msg, msgtype 
