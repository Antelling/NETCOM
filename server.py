import socket, sys, threading
import Lib

sock = Lib.CreateConnect(sys.argv[1], int(sys.argv[2]), server=True)

"""Validate nickname"""
def is_good_nickname(nick):
    if len(nick) > 0:
        return True

"""
Handle a connection with a user. Receives the connection 
object, the client address, and a pointer to an array shared by all 
other connections. The array will contain a collection of callbacks 
to send messages to other threads. An array containing all nicknames
will also be passed. 
"""
def connection_thread(con, client_address, message_receivers, nicknames):
    #first message from client should be a HELLO msg 
    msg, msgtype = Lib.RecvMessage(con)
    assert msgtype == "HELLO"
    Lib.SendMessage(con, msgtype="HELLO")

    #now we expect nickname requests until a nickname is sent
    nick = ""
    while not nick:
        requested_nick, msgtype = Lib.RecvMessage(con)
        print("requested nickname: ", requested_nick, msgtype)
        assert msgtype == "NICK"
        if (not requested_nick in nicknames) and is_good_nickname(requested_nick):
            print("nickname set. ")
            nicknames.add(requested_nick)
            nick = requested_nick
            Lib.SendMessage(con, msgtype="NICKSET")
        else:
            Lib.SendMessage(con, msgtype="FAIL")

    #set up callback 
    send_msg = lambda msg, t="MSG": Lib.SendMessage(con, msg)
    mutex.acquire() # I don't think I need to do this but don't 
    #know how to check 
    message_receivers.append(send_msg)
    mutex.release()

    #handle messages recieved by client
    while True:
        msg, msgtype = Lib.RecvMessage(con)
        if msgtype == "MSG":
            msg = f"<{nick}>: {msg}"
            mutex.acquire()
            print(msg)
            [mr(msg) for mr in message_receivers]
            mutex.release()
        elif msgtype == "BYE":
            con.close()
        else:
            # this should not happen
            Lib.SendMessage(con, "Malformed message.", msgtype="ERROR")



message_receivers = []
mutex = threading.Lock()
nicknames = set()

try:
    print("listening for messages...")

    sys.stdout.flush()
    sock.listen(1)

    while True:
        connection, client_address = sock.accept()
        print("connection started")
        x = threading.Thread(target=connection_thread, args=(
            connection, client_address, message_receivers, nicknames))
        x.start()
        

except KeyboardInterrupt:
    print("closing server...")
    [mr("server shutdown...", "BYE") for mr in message_receivers]
    print("bye")
