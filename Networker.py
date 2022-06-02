import socket
import time
from threading import Thread


class Networker:
    def __init__(self, message, save_or_load, address):
        self.message = message
        self.save_or_load = save_or_load
        self.address = address
        self.answer = None
        self.err_msg = None

    def get_to_work(self):
        thread = Thread(self.send_recv)
        thread.start()

    def send_recv(self):
        try:
            self.user.connect(self.address)
            self.user.protocol_message(self.message, self.save_or_load)
            self.my_socket.settimeout(0.01)
            answer = self.user.recv_message()
            counter = 0
            while answer is None or counter != 100:
                counter += 1
                time.sleep(0.01)
                answer = self.user.recv_message()
            self.answer = answer
            self.my_socket.settimeout(0.0)
        except Exception as ex:
            self.user.my_socket.close()
            self.err_msg = ex
            return False, None
        self.user.my_socket.close()
        return True, answer
