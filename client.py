# !/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def receive():
    """Handles receiving of messages."""
    name = None
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg = msg.split(',')
            if len(msg) == 2:
                if name is None:
                    name = msg[0]
                    print("Joined the game as Player {}".format(name))
                elif msg[1] == "EXIT":
                    name = msg[0]
                    print("Player {} has left the game".format(name))
            if msg[0] != name and msg[1] == "MOVE":
                x = int(msg[2])
                y = int(msg[3])
                print("move: {}, {}".format(x, y))
                # say a piece is at 1,2
                if (x, y) == (1, 2):
                    send("RESP,HIT".format(name))
                else:
                    send("RESP,MISS".format(name))
            elif msg[0] == name and msg[1] == "RESP":
                if msg[2] == "HIT":
                    print("HIT")
                elif msg[2] == "MISS":
                    print("MISS")

        except OSError:
            break


def send(message):
    """Handles sending of messages."""
    client_socket.send(bytes(message, "utf8"))


HOST = "127.0.0.1"
PORT = 33000

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()

while True:
    move = input()
    message = "MOVE,{}".format(move)
    if move != "-1,-1":
        send(message)
    else:
        send("{quit}")
        client_socket.close()
        print("connection closed")
