import socket
import threading
from server import port


class Client:
    def __init__(self, board):
        self.s = None
        self.start_connection()
        self.board = board

    def listener(self):
        while True:
            message = self.s.recv(16).decode("utf-8")
            if message == "end of turn":
                print(message)
                self.board.change_turn()

    def start_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((socket.gethostname(), port))

        t = threading.Thread(target=self.listener)
        t.start()

    def send(self, message):
        if not self.s:
            self.start_connection()
        self.s.send(bytes(message, "utf-8"))


if __name__ == "__main__":
    client = Client()
    client.send("Hello")

