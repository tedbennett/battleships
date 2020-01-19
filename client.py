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
                if len(message) == 2:
                    if self.name is None:
                        self.name = message[0]
                        print("Joined the game as Player {}".format(self.name))
                        self.board.process_join(self.name)
                    elif message[1] == "EXIT":
                        exit_name = message[0]
                        print("Player {} has left the game".format(exit_name))
                        self.board.process_exit(exit_name)

                if message[0] != self.name and message[1] == "MOVE":
                    response = self.board.process_guess(message[2:3])
                    self.send("RESP,{}".format(response))
                elif message[0] == self.name and message[1] == "RESP":
                    self.board.process_response(message[2])
            except OSError:
                break

    def send(self, message):
        """Handles sending of messages."""
        self.client_socket.send(bytes(message, "utf8"))


if __name__ == "__main__":
    client = Client()
