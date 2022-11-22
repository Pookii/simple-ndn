class InterestPacket:
    def __init__(self, name, nonce, hop_count_tag, previous_section, next_section):
        self.name = name
        self.nonce = nonce
        # Number of retweets
        self.hop_count_tag = hop_count_tag
        # Previous node
        self.previous_section = previous_section
        self.next_section = next_section


class ResourcePacket:
    def __init__(self, name, signature, hop_count_tag, next_section, content):
        self.name = name
        self.signature = signature
        # Number of retweets
        self.hop_count_tag = hop_count_tag
        # next node
        self.next_section = next_section
        self.content = content


class DetectPacket:
    def __init__(self, name, nonce, hop_count_tag, previous_section, section_list):
        self.name = name
        self.nonce = nonce
        # Number of retweets
        self.hop_count_tag = hop_count_tag
        # Previous node
        self.previous_section = previous_section
        # the path of detectpacket
        self.section_list = section_list


# producer send it to costumer when it received detectpacket
class ConfirmPacket:
    def __init__(self, name, nonce, hop_count_tag, previous_section, section_list, ttl):
        self.name = name
        self.nonce = nonce
        # Number of retweets
        self.hop_count_tag = hop_count_tag
        # Previous node
        self.previous_section = previous_section
        # the path of detectpacket
        self.section_list = section_list
        # Number of hops from consumer to resource owner
        self.ttl = ttl


#     The node broadcasts a heartbeat packet to establish a neighbourhood relationship with nodes
#     within communication distance, exchanging information such as coordinates and speed
class HeartbeatPacket:
    def __init__(self):
        pass