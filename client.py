# !/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


class Client:
    def __init__(self):
        self.name = None
        self.client_socket = None
        self.host = "127.0.0.1"
        self.port = 33000
        self.buffer_size = 1024

        self.start_client()

    def start_client(self):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.host, self.port)

        receive_thread = Thread(target=self.receive)
        receive_thread.start()

        while True:
            move = input()
            message = "MOVE,{}".format(move)
            if move != "-1,-1":
                self.send(message)
            else:
                self.send("{quit}")
                self.client_socket.close()
                print("connection closed")

    def receive(self):
        """Handles receiving of messages."""
        while True:
            try:
                message = self.client_socket.recv(self.buffer_size).decode("utf8")
                message = message.split(',')
                if len(message) == 2:
                    if name is None:
                        self.name = message[0]
                        print("Joined the game as Player {}".format(self.name))
                    elif message[1] == "EXIT":
                        name = message[0]
                        print("Player {} has left the game".format(self.name))
                if message[0] != self.name and message[1] == "MOVE":
                    x = int(message[2])
                    y = int(message[3])
                    print("move: {}, {}".format(x, y))
                    # say a piece is at 1,2
                    if (x, y) == (1, 2):
                        self.send("RESP,HIT".format(self.name))
                    else:
                        self.send("RESP,MISS".format(self.name))
                elif message[0] == self.name and message[1] == "RESP":
                    if message[2] == "HIT":
                        print("HIT")
                    elif message[2] == "MISS":
                        print("MISS")
            except OSError:
                break

    def send(self, message):
        """Handles sending of messages."""
        self.client_socket.send(bytes(message, "utf8"))


if __name__ == "__main__":
    client = Client()
