import socket, sys
import Lib

sock = Lib.CreateConnect(sys.argv[1], int(sys.argv[2]), server=True)

try:
    print("listening for messages...")

    sys.stdout.flush()
    sock.listen(1)
    connection, client_address = sock.accept()

    for msg in Lib.RecvMessage(connection):
        print("<MSG>: ", msg)

except KeyboardInterrupt:
    print("closing server...")
    Lib.ClientClose(sock)
    print("bye")
