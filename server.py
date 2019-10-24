import socket
import threading

port = 1235


class Server:

    def __init__(self):
        self.clients = {}

    def on_new_client(self, client_socket, address):
        while True:
            message = client_socket.recv(16)
            if message:
                for client in self.clients.keys():
                    if self.clients[client] != address:
                        print("sending message: ", message)
                        client.send(message)
                        message = None
        client_socket.close()

    def main(self):
        s = socket.socket()
        host = socket.gethostname()
        print('Server started!')
        print('Waiting for clients...')

        s.bind((host, port))
        s.listen(5)

        threads = []

        while True:
            c, address = s.accept()
            self.clients[c] = address
            print('Got connection from', address)
            t = threading.Thread(target=self.on_new_client, args=(c, address))
            threads.append(t)
            t.start()
        s.close()


if __name__ == "__main__":
    server = Server()
    server.main()
