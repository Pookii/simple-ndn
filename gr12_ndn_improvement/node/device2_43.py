# Author: Bingqi Xia
# Id: 22300549


from sensor import Sensor
import socket
import time
import os

from sensor import Sensor
import socket
import time
import os

# '10.6.49.224'
class Device:
    def __init__(self, device_name, gateway_host, gateway_port, port_send, port_listen):
        # /area43/device1
        self.device_name = device_name
        self.save_dir = os.getcwd() + '/data'
        self.gateway_host = gateway_host
        self.port_send = port_send
        self.port_listen = port_listen
        self.gateway_port = gateway_port
        self.register_cmd = 'register:'
        self.interest_cmd = 'interest:'
        self.data_cmd = 'data:'
        self.client = None

        # print("name: %s, device host: %s, port_listen: %d, port_send: %d" \
        #       % (self.device_name, self.getHost(), self.port_listen, self.port_send))

    def getHost(self):
        hostname = socket.gethostname()
        host = socket.gethostbyname(hostname)
        return host

    def generate_date(self):
        sensor_name = 'speed'
        sensor = Sensor(self.device_name, sensor_name, self.save_dir)
        sensor.create_file()

    def register_to_router(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # print(self.getHost(), self.port_send)
        client.bind((self.getHost(), self.port_send))

        client.connect((self.gateway_host, self.gateway_port))
        client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        # register:/area43/device1&ttl=0&sender=/area43/device1;port_listen
        msg = self.register_cmd + self.device_name + '&' + 'ttl=0' + "&sender=" + self.device_name + ';' + str(self.port_listen)
        # print("register_to_router: %s" % msg)
        msg = msg.encode('utf-8')
        client.send(msg)

        client.close()


    def send_packet(self, msg, is_close=False):
        msg = msg.encode('utf-8')
        if self.client is None:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.bind((self.getHost(), self.port_send))
            self.client.connect((self.gateway_host, self.gateway_port))
        if not is_close:
            self.client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.client.send(msg)

        if is_close:
            self.client.close()

    def send_interest(self, data_name):
        msg = self.interest_cmd + data_name + "&sender=%s" % (self.device_name)
        msg = msg.encode('utf-8')

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.bind((self.getHost(), self.port_send))
        client.connect((self.gateway_host, self.gateway_port))

        client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        client.send(msg)
        print("Send inteset %s,  from %s" % (data_name, self.device_name))
        # data:dataname^datacentent&sender=xx
        ack = client.recv(1024).decode('utf-8')
        ack = ack.split(':')[1]
        data_name = ack.split('^')[0]
        ack = ack.split('^')[1]
        requester_name = ack.split('&')[1].split("=")[1]
        data_content = ack.split('&')[0]

        print("Received data name:%s, content:%s, from %s" % (data_name, data_content, requester_name))
        client.close()

    def listen(self):
        # listen interest packet
        buff_size = 1024
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.getHost(), self.port_listen))
        server.listen(5)

        while True:
            client, addr = server.accept()
            msg = client.recv(buff_size).decode('utf-8')

            if msg is not None:
                requester_name = msg.split('&')[1].split("=")[1]
                msg = msg.split('&')[0]
                data_name = msg.split(':')[1]
                print('Received inteset %s, from %s' % (data_name, requester_name))

                path = self.save_dir + data_name
                if os.path.exists(path):
                    with open(path, 'r') as f:
                        data_content = f.read()
                else:
                    data_content = 'data not found'
                #     data:dataname^datacentent&sender=xx
                msg = self.data_cmd + data_name + "^" + data_content + '&sender=%s'%self.device_name
                client.send(msg.encode('utf-8'))
                client.close()
                time.sleep(1)


if __name__ == '__main__':
    device1 = Device('/area43/device2', '10.35.70.43', 33421, 33225, 33226)
    device1.generate_data()
    device1.register_to_router()
    device1.listen()