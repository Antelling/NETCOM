import socket, sys
import Lib

sock = Lib.CreateConnect("", 2000, server=True)

sock.listen(1)
connection, client_address = sock.accept()

try:
    for msg in Lib.RecvMessage(connection):
        print("<MSG>: ", msg)
except KeyboardInterrupt:
    print("closing server...")
    Lib.ClientClose(connection)
    print("bye")
