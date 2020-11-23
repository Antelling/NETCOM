import Lib

import socket
import sys

def nickname():
	correctnickname = "false"
	while correctnickname == "false":
		print "Please input a nickname"
		Message = raw_input()
		Lib.SendMessage(s, "NICK %s" %(Message))
		for msg in Lib.RecvMessage(connection):
			if msg != "READY":
				correctnickname = "false"
			else:
				correctnickname = "true"
	
	
	

s = Lib.CreateConnect(sys.argv[1],sys.argv[2])
Lib.SendMessage(s, "Hello")
for msg in Lib.RecvMessage(s):
	if msg == "HELLO":
		nickname()
