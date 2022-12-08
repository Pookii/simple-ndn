# Author: Bingqi Xia
# Id: 22300549

import os
import pandas as pd
import ast
import pylru

class FIB:
    def __init__(self, path):
        # source_name, next_section, ttl
        self.path = path
        self.record = None

    def setup(self):
        if not os.path.exists(self.path):
            (fib_dir, filename) = os.path.split(self.path)
            if not os.path.exists(fib_dir):
                os.makedirs(fib_dir)

            # create fib
            self.record = pd.DataFrame({"source_name": [], "next_section": [], "ttl": []})
            self.record.to_csv(self.path, index=False)
        else:
            self.record = pd.read_csv(self.path)

    # addr: 'ip:port'
    def add_record(self, name_prefix, addr, ttl):
        # print('fib path: %s' % self.path)
        if self.record is None:
            self.setup()

        old_record = self.record.loc[(self.record['source_name'] == name_prefix)]
        if (old_record is not None) and (len(old_record) > 0):
            # same name_prefix in fib
            if int(list(old_record['ttl'])[0]) > int(ttl):
                # update fib record
                self.record.loc[(self.record['source_name'] == name_prefix), 'next_section'] = addr
                self.record.loc[(self.record['source_name'] == name_prefix), 'ttl'] = str(ttl)
                self.record.to_csv(self.path, index=False)
        else:
            # this record not in fib
            new_record = {"source_name": name_prefix, "next_section": addr, "ttl": str(ttl)}
            self.record = self.record.append(new_record, ignore_index=True)
            self.record.to_csv(self.path, index=False)

    def find_next_section(self, name_prefix):
        next_section = None
        if self.record is None:
            self.setup()

        for i, r in self.record.iterrows():
            source_name = str(r['source_name'])
            if name_prefix.startswith(source_name):
                next_section = str(r['next_section'])
        return next_section


class InterestPacket:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

class PIT:
    def __init__(self, path):
        self.path = path
        # key: source name
        # value: '['ip, port')]'
        self.record = None

    def setup(self):
        if not os.path.exists(self.path):
            (pit_dir, filename) = os.path.split(self.path)

            if not os.path.exists(pit_dir):
                os.makedirs(pit_dir)

            # create pit
            self.record = pd.DataFrame({"source_name": [], "requester": []})
            self.record.to_csv(self.path, index=False)
        else:
            self.record = pd.read_csv(self.path)

    # addr: 'ip:port'
    def add_record(self, name_prefix, addr):

        if self.record is None:
            self.setup()

        old_record = self.record.loc[(self.record['source_name'] == name_prefix)]

        if (old_record is not None) and (len(old_record) > 0):
            requesters = list(old_record['requester'])[0]
            # string to list
            requesters = ast.literal_eval(requesters)
            # add new addr into same name_prefix
            if addr not in requesters:
                requesters.append(addr)
                self.record.loc[(self.record['source_name'] == name_prefix), 'requester'] = \
                    value = '[' + ','.join("'" + x + "'" for x in requesters) + ']'
                self.record.to_csv(self.path, index=False)
        else:
            # add a new record
            req = "'" + addr + "'"
            new_record = {'source_name': name_prefix, 'requester': '[' + req + ']'}
            self.record = self.record.append(new_record, ignore_index=True)
            self.record.to_csv(self.path, index=False)

    def find_requesters(self, name_prefix):
        if self.record is None:
            self.setup()

        ret = []
        old_record = self.record.loc[(self.record['source_name'] == name_prefix)]

        if (old_record is not None) and (len(old_record) > 0):
            requesters = list(old_record['requester'])[0]
            ret = ast.literal_eval(requesters)

        return ret

    def remove_record(self, name_prefix):
        if self.record is None:
            self.setup()

        self.record = self.record.drop(self.record[self.record['source_name'] == name_prefix].index)
        self.record.to_csv(self.path, index=False)


class ContentStore:
    def __init__(self, max_size):
        # key: source name
        # value: data content
        self.size = max_size
        self.cache = pylru.lrucache(self.size)

    def find_data(self, name_prefix):
        value = None
        if name_prefix in self.cache.keys():
            value = self.cache.peek(name_prefix)
        return value

    def add_record(self, name_prefix, data):
        print("cache add record: name: %s, data: %s" % (name_prefix, data))
        self.cache[name_prefix] = data

if __name__ == '__main__':
    # fib = FIB('test/fib')
    # fib.add_record('/test/1/2', '127.0.0.2:8080', '0')
    # fib.add_record('/test/1/3', '127.0.0.1:8001', '0')
    # print(fib.find_next_section('/test/1/2'))

    pit = PIT('test/pit')

    pit.add_record('/test/1/5', '127.0.0.2:5000')
    pit.add_record('/test/1/5', "127.0.0.2:5001")
    pit.add_record('/test/1/3', "127.0.0.2:5001")

    print(pit.find_requesters('/test/1/3'))

    # cs = ContentStore()
    # cs.add_record('/test/1/2', 'intpak2')
    # cs.find_data('/test/1/1')
    # cs.add_record('/test/1/2', 'intpak2')