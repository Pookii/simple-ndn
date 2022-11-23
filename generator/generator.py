from sensor import Sensor
from datetime import datetime
from socket import *
import os
class Generator:
    def __init__(self, name):
        self.name = name

    def generator_file(self):
        sensor_name = self.name + '/A'
        sensor = Sensor(sensor_name)

        for i in range(10):
            time_nonce = datetime.now().strftime('%Y%m%d%H%M%S')
            file_name = self.name + "/seed/test/sc/%d_%s.txt" % (i, time_nonce)
            sensor.create_file(file_name)

    def register_to_router(self, file_name):
        cmd = 'registerFIB:'
        (path, filename) = os.path.split(file_name)

        clientSock = socket(AF_INET, SOCK_STREAM)
        clientSock.connect(('127.0.0.1', 8080))

        # connetcionSock
        filename = cmd+filename+'&'+'ttl=0'
        clientSock.send(file_name.encode('utf-8'))

        print('register name %s.' % filename)
        data = clientSock.recv(1024)

        print('received data: ', data.decode('utf-8'))
