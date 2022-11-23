# ForwardingInfomationBase
import os
import pandas as pd


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

    def add_new_record(self, name_prefix, addr, ttl):

        if self.record is None:
            self.setup()

        old_record = self.record.loc[(self.record['source_name'] == name_prefix)]

        if (old_record is not None) and (len(old_record) > 0):
            # same name_prefix in fib
            if int(old_record['ttl']) > int(ttl):
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

        target = self.record.loc[(self.record['source_name'] == name_prefix)]
        if (target is not None) and (len(target) > 0):
            next_section = list(target['next_section'])[0]
        return next_section


class IntersestPacket:
    def __init__(self, previous_section, nonce):
        self.previous_section = previous_section
        self.nonce = nonce


class PendingInterestTable:
    def __init__(self):
        # key: source name
        # value: interest list
        self.source_name = {}
        
    def add_record(self, source_name, intersest_record: IntersestPacket):
        if source_name in self.source_name.keys():
            pass


class ContentStore:
    def __init__(self):
        # key: source name
        # value: data content
        self.cache = {}


if __name__ == '__main__':
    fib = FIB('test/fib')
    fib.add_new_record('/test/1/2', '127.0.0.2', '0')
    fib.add_new_record('/test/1/3', '127.0.0.1', '0')
    fib.find_next_section('/test/1/2')