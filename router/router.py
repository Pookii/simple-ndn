from socket import *
import os
class Router:
    def __init__(self):
        self.host = ''
        self.port = ''
        self.register_cmd = 'registerFIB:'
        self.fib_path = os.getcwd() +'/config/fib'


    def setup(self):
        with open(self.fib_path, 'w') as f:
            f.write("")

    def receive_data(self):
        serverSock = socket(AF_INET, SOCK_STREAM)
        serverSock.bind((self.host, self.port))
        serverSock.listen()
        connectionSock, addr = serverSock.accept()
        msg = connectionSock.recv(1024).decode('utf-8')
        print('Received data : ', msg)

        if msg.startswith(self.register_cmd):
            ttl = int(msg.split('&')[1].split("=")[1]) + 1
            print(ttl)
            next_section = ""

        connectionSock.send('I am a server!'.encode('utf-8'))
        print('Sent message.')


if __name__ == '__main__':
    msg = 'registerFIB:/speed/test/sc/1.txt&ttl=0'
    ttl = int(msg.split('&')[1].split("=")[1]) + 1
    print(ttl)