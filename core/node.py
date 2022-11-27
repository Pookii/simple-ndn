from socket import *
import os
import pandas as pd
import sys
sys.path.append('/Users/pooki/Documents/lecture/Scalable Computing/project3/simple-ndn/')
# sys.path.append('../')
from core.Structures import *

class Node:
    def __init__(self):
        self.host = ''
        self.port = 50000
        self.register_cmd = 'registerFIB:'
        self.interest_cmd = 'interest:'
        self.fib_path = os.getcwd() +'/router/fib'
        self.fib = FIB(self.fib_path)

    def register_fib(self, msg, addr):
        # insert a new fib record
        if msg.startswith(self.register_cmd):
            ttl = int(msg.split('&')[1].split("=")[1]) + 1
            file_name = msg.split(':')[1].split('&')[0]
            print('file_name: ' + file_name)
            (prefix, filename) = os.path.split(file_name)
            self.fib.add_new_record(prefix, addr, ttl)

    def search_pit(self):
        pass

    def search_cs(self):
        pass

    def parse_cmd(self, msg, addr):
        if msg.startswith(self.interest_cmd):
            pass
        elif msg.startswith(self.register_cmd):
            self.register_fib(msg, addr)

    def


    def listen(self):
        buff_size = 1024
        server = socket(AF_INET, SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(5)

        while True:
            client, addr = server.accept()
            msg = client.recv(buff_size).decode('utf-8')
            print('Received data %s from %s' % (msg, addr))
            client.send('I am a server!'.encode('utf-8'))
            print('Sent message.')
            self.register_fib(msg, addr)


if __name__ == '__main__':
    # msg = 'registerFIB:/speed/test/sc/1.txt&ttl=0'
    # ttl = int(msg.split('&')[1].split("=")[1]) + 1
    # print(ttl)
    router = Router()
    router.listen()
