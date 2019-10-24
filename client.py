import socket
import threading
from server import port


def listener():
    while True:
        message = s.recv(16)
        if message:
            print("Received: ", message)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), port))

t = threading.Thread(target=listener)
t.start()

msg = input()
if msg == "send":
    s.send(bytes("Hello", "utf-8"))

