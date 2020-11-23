import Lib

import socket
import sys

def nickname():
	true = "true"
	while true == "true":
		for msg in Lib.RecvMessage(s):
			print "Please input a nickname"
			Message = raw_input()
			Lib.SendMessage(s, "NICK %s" %(Message))
	for msg in Lib.RecvMessage(connection):
		if msg != "READY":
			true = "true"
		else:
			true = "False"
	
	
	

s = Lib.CreateConnect(sys.argv[1],sys.argv[2])
Lib.SendMessage(s, "Hello")
for msg in Lib.RecvMessage(s):
    if msg == "NICK":
		nickname()
