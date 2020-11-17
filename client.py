import lib

import socket
import sys

if sys.argv[1] == "test" and sys.argv[2] == "2000":
	s = lib.CreateConnect(sys.argv[1],sys.argv[2])
	lib.SendMessage(s, "Hello")
	
else
	print("invalid host and port")