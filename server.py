import json
import socket
from _thread import *
import pickle
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = "192.168.68.118"
port = 5555

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen()
print("[START] Waiting for a connection")

connections = 0

# games = {0: Board(8, 8)}

# spectartor_ids = []
# specs = 0
#

# def read_specs():
#     global spectartor_ids
#
#     spectartor_ids = []
#     try:
#         with open("specs.txt", "r") as f:
#             for line in f:
#                 spectartor_ids.append(line.strip())
#     except:
#         print("[ERROR] No specs.txt file found, creating one...")
#         open("specs.txt", "w")


def threaded_client(conn, addr, spec=False):
    global pos, games, currentId, connections, specs

    if not spec:
        name = None

        if connections % 2 == 0:
            currentId = "A"
        else:
            currentId = "B"
        data_string = f"Welcome player {currentId}"
        conn.send(json.dumps(data_string).encode("utf-8"))
        # bo.start_user = currentId
        #
        # # Pickle the object and send it to the server
        # data_string = pickle.dumps(bo)
        #
        # if currentId == "A":
        #     bo.ready = True
        #     bo.startTime = time.time()

        # conn.send(data_string)
        connections += 1

        while True:
            try:
                d = conn.recv(8192 * 3)
                data = json.loads(d.decode("utf-8"))
                if not d:
                    break
                send_data = json.dumps(data).encode("utf-8")
                for connection in conns.keys():
                    if connection != conn:
                        connection.sendall(send_data)
                        print("Sending move to player", currentId, "at ", conns[connection])

            except Exception as e:
                print(e)

        connections -= 1
        print("[DISCONNECT] Player", name, "left game")
        conn.close()

conns = {}
while True:
    if connections < 2:
        conn, addr = s.accept()
        conns[conn] = addr
        print("[CONNECT] New connection")

        start_new_thread(threaded_client, (conn, addr))
