import threading
import socket
import array
from collections import defaultdict

class SocketListener(threading.Thread):
    def __init__(self, udpAddr, udpPort):
        threading.Thread.__init__(self)
        self.subscriptions = defaultdict(list)

        self.addr = udpAddr
        self.port = udpPort

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.addr, self.port))
        while True:
            data, addr = sock.recvfrom(4096)

            for i in range(5, len(data), 36):
                index = int.from_bytes(data[i:i+4], byteorder="little")
                values = array.array('f', data[i+4:i+36]).tolist()

                if index in self.subscriptions:
                    for callback in self.subscriptions[index]:
                        callback(values)

    def subscribe(self, index, callback):
        self.subscriptions[index].append(callback)
