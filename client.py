import socket
import threading
from server import port


def listener(server):
    while True:
        message = server.recv(16)
        if message:
            process_message(message)

def process_message(message):
    board.move(message)

def start_connection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), port))

    t = threading.Thread(target=listener, args=s)
    t.start()

def send(server, message):
    server.send(bytes(message, "utf-8"))

