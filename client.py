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
#Compile and execute: python3 client.py localhost 10000
#the 10000 at the end is optional also the server needs to be
#up before this code is ran
import Lib, socket, sys

# Name: nickname
# Purpose: The purpose of the function is to pick a unused nickname
# Arguments: con which is the socket connection
# Return value: none
def nickname(con):
    message = input("Please input a nickname> ")
    Lib.SendMessage(con, message, msgtype="NICK")
    response, response_type = Lib.RecvMessage(con)
    if response_type != "READY":
        print("Nickname is not allowed by server.")
        nickname(con)

# create socket and start connection 
if len(sys.argv) == 3:
	s = Lib.CreateConnect(sys.argv[1], sys.argv[2])
	Lib.SendMessage(s, msgtype="HELLO")
	res, rest = Lib.RecvMessage(s)
else: 
	s = Lib.CreateConnect(sys.argv[1], 5000)
	Lib.SendMessage(s, msgtype="HELLO")
	res, rest = Lib.RecvMessage(s)
print(res, rest)
assert rest == "HELLO"
print("Connection started successfully. ")

# set nickname 
nickname(s)
print("You are now allowed to send messages to the server if at anytime you want to end please just type BYE in the chat.")
Status = True
#message prompt
while Status:
	user_message = input("--> ")
	if(user_message == "BYE"):
		Status = False
	else:
		Lib.SendMessage(s, user_message)
