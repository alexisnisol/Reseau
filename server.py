import socket

class Server :
    
    def __init__(self):
        self.counter = 0

    def mainServer(self, port):
        sock = socket.socket() #par défaut, le type est SOCK_STREAM (TCP)
        sock.bind(('0.0.0.0', port))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.listen(10) # écoute les connexions entrantes, 10 connexions max en attente de traitement avant d'être refusées
        while True:
            cli, addr = sock.accept() # accepte une connexion entrante (méthode bloquante).
            #cli est une nouvelle socket pour communiquer avec le client
            sess = Session(self, cli)
            sess.mainSession()

class Session:

    def __init__(self, server, sock):
        self.server = server
        self.socket = sock
        self.file = sock.makefile(mode="rw") #écrire sur un flux de données (fichier) associé à la socket

    def mainSession(self):
        while True:
            line = self.file.readline().strip()
            if line == "get":
                self.file.write(f"val {self.server.counter}\n") #\n important pour indiquer que la ligne est terminée => readline()
                self.file.flush() #force l'envoi des données
            elif line == "quit":
                self.file.write("quit\n")
                self.file.flush()
                break
            elif line == "incr":
                self.server.counter += 1
                self.file.write(f"val {self.server.counter}\n")
                self.file.flush()
            elif line == "decr":
                self.server.counter -= 1
                self.file.write(f"val {self.server.counter}\n")
                self.file.flush()
            elif line.startswith("add"):
                try:
                    self.server.counter += int(line.split(" ")[1])
                    self.file.write(f"val {self.server.counter}\n")
                except:
                    self.file.write("err\n")    
                self.file.flush()
            else:
                self.file.write("err\n")
                self.file.flush()
        
        self.file.close()
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

Server().mainServer(5554)