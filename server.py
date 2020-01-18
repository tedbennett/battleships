from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    num_clients = 0
    while True:
        client, client_address = SERVER.accept()
        addresses[client] = client_address
        print("%s:%s has connected." % client_address)
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):
    """Handles a single client connection."""
    name = str(len(clients) + 1)
    clients[client] = name
    broadcast(name, bytes("JOIN", "utf8"))

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(name, msg)
        else:
            client.close()
            del clients[client]
            print("%s:%s has connected." % addresses[client])
            broadcast(name, bytes("EXIT", "utf8"))
            break


def broadcast(name, msg):
    """Broadcasts a message to all the clients."""
    for sock in clients:
        sock.send(bytes(name + ",", "utf8") + msg)


clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
