import Lib, socket, sys

def nickname():
    message = input("Please input a nickname")
    Lib.SendMessage(s, message, type="NICK")
    response, response_type = Lib.RecvMessage(connection)
    if response_type != "NICKSET":
        print("Nickname is not allowed by server.")
        nickname()

# create socket and start connection 
s = Lib.CreateConnect(sys.argv[1], sys.argv[2])
Lib.SendMessage(s, msgtype="HELLO")
res, rest = Lib.RecvMessage(s)
assert rest == "HELLO"
print("connection started successfully. ")

# set nickname 
nickname()

#message prompt
while True:
    user_message = input("--> ")
    Lib.SendMessage(s, user_message)