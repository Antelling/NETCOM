import Lib, socket, sys

def nickname(con):
    message = input("Please input a nickname> ")
    Lib.SendMessage(con, message, msgtype="NICK")
    response, response_type = Lib.RecvMessage(con)
    if response_type != "NICKSET":
        print("Nickname is not allowed by server.")
        nickname(con)

# create socket and start connection 
s = Lib.CreateConnect(sys.argv[1], sys.argv[2])
Lib.SendMessage(s, msgtype="HELLO")
res, rest = Lib.RecvMessage(s)
print(res, rest)
assert rest == "HELLO"
print("connection started successfully. ")

# set nickname 
nickname(s)

#message prompt
while True:
    user_message = input("--> ")
    Lib.SendMessage(s, user_message)