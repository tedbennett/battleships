from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


class Server:
    def __init__(self):
        self.clients = {}
        self.addresses = {}
        self.start_server()

    def start_server(self):
        SERVER.listen(5)
        print("Waiting for connection...")
        accept_thread = Thread(target=self.accept_incoming_connections)
        accept_thread.start()
        accept_thread.join()
        SERVER.close()

    def accept_incoming_connections(self):
        """Sets up handling for incoming clients."""
        num_clients = 0
        while True:
            client, client_address = SERVER.accept()
            self.addresses[client] = client_address
            print("%s:%s has connected." % client_address)
            Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):
        """Handles a single client connection."""
        name = str(len(self.clients) + 1)
        self.clients[client] = name
        self.broadcast(name, bytes("JOIN", "utf8"))

        while True:
            msg = client.recv(BUFSIZ)
            if msg != bytes("{quit}", "utf8"):
                self.broadcast(name, msg)
            else:
                client.close()
                del self.clients[client]
                print("%s:%s has disconnected." % self.addresses[client])
                self.broadcast(name, bytes("EXIT", "utf8"))
                del self.addresses[client]
                break

    def broadcast(self, name, msg):
        """Broadcasts a message to all the clients."""
        for sock in self.clients:
            sock.send(bytes(name + ",", "utf8") + msg)


if __name__ == "__main__":
    HOST = ''
    PORT = 33000
    BUFSIZ = 1024
    ADDR = (HOST, PORT)

    SERVER = socket(AF_INET, SOCK_STREAM)
    SERVER.bind(ADDR)

    server = Server()
