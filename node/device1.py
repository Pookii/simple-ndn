from sensor import Sensor
import socket
import time
import os

# '10.6.49.224'
class Device:
    def __init__(self, device_name, gateway_host, gateway_port, port_send, port_listen):
        # /area1/device1
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

        print("name: %s, device host: %s, port_listen: %d, port_send: %d" \
              % (self.device_name, self.getHost(), self.port_listen, self.port_send))

    def getHost(self):
        hostname = socket.gethostname()
        host = socket.gethostbyname(hostname)
        return host

    def generate_date(self):
        sensor_name = 'speed'
        sensor = Sensor(self.device_name, sensor_name, self.save_dir)
        sensor.create_file('1')

    def register_to_router(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # print(self.getHost(), self.port_send)
        client.bind((self.getHost(), self.port_send))

        client.connect((self.gateway_host, self.gateway_port))
        client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

        msg = self.register_cmd + self.device_name + '&' + 'ttl=0' + ';' + str(self.port_listen)
        # print("register_to_router: %s" % msg)
        msg = msg.encode('utf-8')
        client.send(msg)

        client.close()


    def send_packet(self, msg, is_close=False):
        msg = msg.encode('utf-8')
        if self.client is None:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.bind((self.getHost(), self.port_send))
            print(self.client.getsockname())
            self.client.connect((self.gateway_host, self.gateway_port))
        if not is_close:
            self.client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.client.send(msg)

        if is_close:
            self.client.close()

    def send_interest(self, data_name):
        msg = self.interest_cmd + data_name
        msg = msg.encode('utf-8')

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.bind((self.getHost(), self.port_send))
        print(client.getsockname())
        client.connect((self.gateway_host, self.gateway_port))

        client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        client.send(msg)

        ack = client.recv(1024).decode('utf-8')
        print("ACKNOWLEDGEMENT", ack)
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
            print('Received data %s from %s' % (msg, addr))

            if msg is not None:

                cmd = msg.split(':')[0]
                data_name = msg.split(':')[1]

                path = self.save_dir + data_name
                if os.path.exists(path):
                    with open(path, 'r') as f:
                        data_content = f.read()
                        print(data_content)
                else:
                    data_content = 'data not found'
                msg = self.data_cmd + data_name + '&' + data_content
                client.send(msg.encode('utf-8'))
                client.close()
                time.sleep(1)


if __name__ == '__main__':
    device1 = Device('/area1/device1', '10.108.9.2', 60001, 50001, 50002)
    device1.generate_date()
    device1.register_to_router()
    device1.listen()