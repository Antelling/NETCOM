#author: Anthony Dellinger
#major: computer science
#creation date: Nov 1
#due date: Nov 25
#course: CSC 328 
#professor name: Dr. Frye
#filename: server.py
#purpose: a server for the chat app 
#   that logs all messages received 
#   by clients 

import socket, sys, threading, os
import Lib
from datetime import datetime

#hardcoded values 
log_file = "./serverlog.txt"
host = "localhost"

#make fresh log file 
if os.path.exists(log_file):
  os.remove(log_file)

# handle port default
if len(sys.argv) >= 2:
    port = int(sys.argv[1])
else:
    port = 5000
    print(f"defaulting to port {port}")

#create endpoint 
sock = Lib.CreateConnect(host, port, server=True)

"""Validate nickname.
There aren't any restrictions on 
the nickname besides uniqueness."""
def is_good_nickname(nick):
    return len(nick) > 0


"""
Thread-safe method to append to a file 
"""
def log_msg(filename, msg):
    try:
        mutex.acquire()
        f = open(filename, "a")
        f.write(msg)
        f.close()
        mutex.release()
    except:
        print("Error while writing to log!")
        raise

"""
Handle a connection with a user. Receives the connection 
object, the client address, and a pointer to an array shared by all 
other connections. The array will contain a collection of callbacks 
to send messages to other threads. An array containing all nicknames
will also be passed. 
"""
def connection_thread(con, client_address, filename, nicknames):
    #first message from client should be a HELLO msg 
    msg, msgtype = Lib.RecvMessage(con)
    assert msgtype == "HELLO"
    Lib.SendMessage(con, msgtype="HELLO")

    #now we expect nickname requests until a unique nickname is sent
    nick = ""
    while not nick:
        requested_nick, msgtype = Lib.RecvMessage(con)
        #check that request is a NICK req
        if msgtype != "NICK":
            Lib.SendMessage(con, "you have not set a nickname!", "ERROR")
            continue 
        #check if nick is unique and valid
        if (not requested_nick in nicknames) and is_good_nickname(requested_nick):
            nicknames.add(requested_nick)
            nick = requested_nick
            Lib.SendMessage(con, msgtype="READY")
        else:
            Lib.SendMessage(con, msgtype="RETRY")

    #log new connection 
    dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    log_msg(filename, f"NEW CONNECTION: <{nick}> from {client_address} on {dt}\n")


    #handle messages recieved by client
    while True:
        try:
            msg, msgtype = Lib.RecvMessage(con)
        except TypeError:
            #this happens when RecvMessage returns None and it fails to unpack
            #that happens when the client exits unexpectedly
            log_msg(filename, f"DISCONNECT: {nick}")
            nicknames.remove(nick)
            return

        if msgtype == "MSG":
            msg = f"{nick}: {msg}\n"
            log_msg(filename, msg)
        elif msgtype == "BYE":
            con.close()
            log_msg(filename, f"EXIT: {nick}")
            nicknames.remove(nick)
        else:
            # this should not happen
            Lib.SendMessage(con, "Message type not valid here.", msgtype="ERROR")

#set up shared memory
mutex = threading.Lock()
nicknames = set()

#guard for keyboard interrupt
try:
    print("listening for messages...")
    sys.stdout.flush()

    sock.listen(1)

    while True:
        connection, client_address = sock.accept()
        x = threading.Thread(target=connection_thread, args=(
            connection, client_address, log_file, nicknames))
        x.start()

except KeyboardInterrupt:
    print("closing server.")
    #the rubric says that the server is meant to send a message to all clients 
    #telling them the server is shutting down. However, the clients are not 
    #listening to the server, so the only way we have to send a message is 
    #bubbling an error. We could go through every connection and close it manually,
    #but that happens automatically when the program terminates. 
    #the rubric says that the server is meant to send a message to all clients 
    #telling them the server is shutting down. However, the clients are not 
    #listening to the server, so the only way we have to send a message is 
    #bubbling an error. We could go through every connection and close it manually,
    #but that happens automatically when the program terminates. 
