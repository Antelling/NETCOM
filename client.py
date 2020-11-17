import Lib

import socket
import sys

s = Lib.CreateConnect(sys.argv[1], sys.argv[2])
Lib.SendMessage(s, "Hello")