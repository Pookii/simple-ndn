class ForwardingInfomationBase:
    def __init__(self, source_name, next_section, ttl):
        self.source_name = source_name
        self.next_section = next_section
        self.ttl = ttl


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
