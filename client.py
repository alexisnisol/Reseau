import socket

def client(host, port):
    sock = socket.socket()
    sock.connect((host, port)) # connexion à un socket distant à une adresse donnée (lié au accept)
    f = sock.makefile(mode="rw")
    
    quitte = False
    while not quitte:
        val = input("tt : ")

        f.write(f"{val}\n")
        f.flush()
        print(f.readline(), end= "")
        if val == "quit":
            quitte = True


    f.close()
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()

client("localhost", 5554)