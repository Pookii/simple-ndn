# Author: Bingqi Xia
# Id: 22300549

import os.path
import socket
import sys
# sys.path.append('../')
from Structures import *
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

class Router:
    def __init__(self, name_prefix, port):
        # /area43
        self.name_prefix = name_prefix

        self.register_cmd = 'register'
        self.data_cmd = 'data'
        self.interest_cmd = 'interest'

        self.neighbor_path = os.getcwd()+'/router/%s/neighbors' % self.name_prefix
        self.neighbors = pd.read_csv(self.neighbor_path)

        self.port = port

        self.fib_path = os.getcwd() +'/router/%s/fib' % self.name_prefix
        # print(self.fib_path)
        self.fib = FIB(self.fib_path)

        self.pit_path = os.getcwd() + '/router/%s/pit' % self.name_prefix
        self.pit = PIT(self.pit_path)

        self.cache = ContentStore(500)
        print("name: %s, router host: %s, port: %d" % (self.name_prefix, self.getHost(), self.port))


    def register_fib(self, info, addr):
        # insert a new fib record
        ttl = int(info.split('&')[1].split("=")[1]) + 1
        file_name = info.split('&')[0]
        self.fib.add_record(file_name, addr, ttl)
        ip_req = addr.split(":")[0]
        port_req = addr.split(":")[1]
        for i, r in self.neighbors.iterrows():
            ip = str(r['ip'])
            port = str(r['port'])
            # print("%s, %s, %s, %s" % (ip, port, ip_req, port_req))
            last_split = file_name.rfind('/')
            filename = file_name[:last_split]
            if last_split == 0:
                filename = file_name

            if not ((ip == ip_req) and (port_req == port)):
                msg = self.register_cmd + ':' + filename + '&ttl=%d' % ttl + "&sender=" + self.name_prefix + ';' + str(self.port)
                self.send_msg(msg, ip, port)

    def process_interest(self, data_name, addr):
    # 1.check pit insert to pit if pit don't have this name_prefix
    # 2. check fib, if have this record then go to next section, otherwise do nothing
        data = 'not found'

        # print("process_interest: name %s" % data_name)
        self.pit.add_record(data_name, addr)
        next_section = self.fib.find_next_section(data_name)
        # print("process_interest: next section %s" % next_section)
        if next_section is not None:
            ip = next_section.split(':')[0]
            port = next_section.split(':')[1]
            msg = self.interest_cmd + ':' + data_name + "&sender=/%s"%self.name_prefix
            data = self.send_msg(msg, ip, port)
    #             send to next_section
        return data

    def send_msg(self, msg, next_section_ip, next_section_port):
        # print("send msg: %s, %s, %s" % (msg, next_section_ip, next_section_port))
        ack = None
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((next_section_ip, int(next_section_port)))
        s.send(msg.encode('utf-8'))
        ack = s.recv(1024).decode('utf-8')

        if ack.startswith(self.data_cmd):
            #     data:dataname^datacontent&sender=xx
            #     receive data packet, save to cache
            # data:dataname^datacentent&sender=xx
            ack = ack.split(':')[1]
            data_name = ack.split('^')[0]
            ack = ack.split('^')[1]
            requester_name = ack.split('&')[1].split("=")[1]
            data_content = ack.split('&')[0]

            print("Received data name:%s, content:%s, from %s" % (data_content, data_name, requester_name))

            self.cache.add_record(data_name, data_content)

        s.close()
        return ack

    def process_data(self, data_name, data_content):
    #     1. check if has same name pit record
    #     if has, send to all requester then remove this record
    #     save in cache.
        self.cache.add_record(data_name, data_content)
        # print("process_data: name: %s, content: %s" % (data_name, data_content))
        requesters = self.pit.find_requesters(data_name)
        if len(requesters) > 0:
            for request in requesters:
                next_ip = request.split(':')[0]
                next_port = request.split(':')[1]
                msg = self.data_cmd + ':' + data_name + '&' + data_content
                print("send msg: %s, %s, %s" % (msg, next_ip, next_port))
                self.send_msg(msg, next_ip, next_port)

    def getHost(self):
        hostname = socket.gethostname()
        host = socket.gethostbyname(hostname)
        # print("name: %s, router host: %s, port: %d" % (self.name_prefix, host, self.port))
        return host

    def listen(self):
        buff_size = 1024
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # print("star listen: name: %s, router host, %s, port: %d" % (self.name_prefix, self.getHost(), self.port))
        server.bind((self.getHost(), self.port))
        server.listen(10)

        while True:
            client, addr = server.accept()
            ip = addr[0]
            send_port = addr[1]
            send_addr = ip+':'+str(send_port)

            msg = client.recv(buff_size).decode('utf-8')
            
            cmd = msg.split(':')[0]
            if cmd == self.interest_cmd:
                # interest:/area43/device1/sensor1/1&sender=jj
                requester_name = msg.split('&')[1].split("=")[1]
                msg = msg.split('&')[0]
                data_name = msg.split(':')[1]
                print('Received interest %s, from %s' % (data_name, requester_name))
                data = self.cache.find_data(data_name)
                #  already have data, send to client
                if data is None:
                    data = self.process_interest(data_name, send_addr)
                    # self.cache.add_record(data_name, data)
                else:
                    print("hit cache")
                send_data = self.data_cmd + ":" + data_name + "^" + data + "&sender=%s" % self.name_prefix
                # print(send_data)
                client.send(str(send_data).encode('utf-8'))

            elif cmd == self.data_cmd:
            #     data:/area43/device1/sensor1/1&content=222
                requester_name = msg.split('&')[1].split("=")[1]
                msg = msg.split('&')[0]
                data_name = msg.split(':')[1]
                print('Received data %s, from %s' % (data_name, requester_name))
                data_name = data_name.split('&')[0]
                data_content = data_name.split('&')[1]
                self.process_data(data_name, data_content)
            elif cmd == self.register_cmd:
                # register:/area43/device1&ttl=0&sender=/area43/device1;port_listen
                extra = msg.split('&')[2].split("=")[1]
                requester_name = extra.split(";")[0]
                data_name = msg.split('&')[0]
                data_name = data_name.split(':')[1]
                print('Received register %s, from %s' % (data_name, requester_name))
                
                listen_port = extra.split(';')[1]
                listen_addr = ip + ':' + str(listen_port)
                # data_name&ttl=0
                data_name = data_name + "&" + msg.split('&')[1]
                local_addr = self.getHost() + ':' + str(self.port)
                if local_addr != listen_addr:
                    self.register_fib(data_name, listen_addr)
                client.send(str("%s:%s register_fib done"%(self.getHost(), str(self.port))).encode('utf-8'))


if __name__ == '__main__':
    # msg = 'register:/speed/test/sc/1.txt&ttl=0'
    # ttl = int(msg.split('&')[1].split("=")[1]) + 1
    # print(ttl)
    # 33000~34000
    gateway_port = 33421
    name_prefix = 'area43'
    router = Router(name_prefix, gateway_port)
    router.listen()
