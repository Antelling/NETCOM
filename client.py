#Author:          Alan Michener
#Major:           Computer Science
#Creation Date:   november 17, 2020
#Due Date:        november 24, 2020
#Course:          Csc328
#Professors name: Dr. Frye
#Assignment:      chatserver
#Filename:        client.py
#Purpose:         This connects a client code with server code and begins communication
#Language and version: python version 3.7.7 the one on acad
#Compile and execute: python qotd_AlanMichener.py udp djxmmx.net
#with changing udp to tcp and changing djxmmx.net to another server
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
print("You are not allowed to send messages to the server if at anytime you want to end please just type BYE in the chat.")
try:
#message prompt
    while True:
        user_message = input("--> ")
        Lib.SendMessage(s, user_message)
       
except user_message == "BYE":
    Lib.SendMessage(s, user_message, msgtype="BYE")
