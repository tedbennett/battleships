# !/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


class Client:
    def __init__(self, board):
        self.host = "127.0.0.1"
        self.port = 33000
        self.buffer_size = 1024

        self.name = None
        self.client_socket = None
        self.board = board

        self.start_client()

    def start_client(self):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

        receive_thread = Thread(target=self.receive)
        receive_thread.start()

    def receive(self):
        """Handles receiving of messages."""
        while True:
            try:
                message = self.client_socket.recv(self.buffer_size).decode("utf8")
                message = message.split(',')
                print("received {}".format(message))
                response = self.board.process_message(message)
                if response:
                    self.send(response)
            except OSError:
                break

    def send(self, message):
        """Handles sending of messages."""
        print("sent {}".format(message))
        self.client_socket.send(bytes(message, "utf8"))

    def close(self):
        self.send("EXIT")

if __name__ == "__main__":
    client = Client()
