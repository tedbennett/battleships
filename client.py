import json
import socket
import pickle
import time


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
        """
        :param data: str
        :return: str
        """
        print("we out here")
        start_time = time.time()
        while time.time() - start_time < 5:
            try:
                self.client.send(json.dumps(data).encode("utf-8"))
                reply = self.client.recv(4096*8)
                try:
                    reply = json.loads(reply)
                    print("Reply loaded")
                    break
                except Exception as e:
                    print(e)

            except socket.error as e:
                print(e)


        return reply


if __name__ == "__main__":
    network = Network()
    print(network.connect())
    print("now send")
    while True:
        reply = network.send({"message": "Hello"})
        print("Response: ", reply)
        time.sleep(15)
