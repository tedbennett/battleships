import json
import socket
import pickle
import time
from _thread import *


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "192.168.68.118"
        self.port = 5555
        self.addr = (self.host, self.port)

    def connect(self):
        self.client.connect(self.addr)
        print("connected")
        return self.client.recv(4096*8)

    def disconnect(self):
        self.client.close()

    def send(self, data, pick=True):
        self.client.send(json.dumps(data).encode("utf-8"))
        return


    def listen(self):
        print("listening")
        reply = None
        while not reply:
            reply = self.client.recv(4096 * 8)
            if reply:
                reply = json.loads(reply)
                print("Reply loaded")
        return reply


if __name__ == "__main__":
    network = Network()
    print(network.connect())
    while True:
        network.send({"message": "Hello"})
        reply = network.listen()
        print("Response: ", reply)
        time.sleep(15)
