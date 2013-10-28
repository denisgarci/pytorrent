import random
from hashlib import sha1
import requests
import socket


class Torrent():

    def __init__(self, torrent_dict):
        self.torrent_dict = torrent_dict

    @property
    def tracker(self):
        return self.torrent_dict['announce']

    @property
    def info(self):
        return self.torrent_dict['info']

    @property
    def total_length(self):
        return self.torrent_dict['info']['length']

    @property
    def info_hash(self):
        return sha1(utils.bencode(self.info)).digest()

    @property
    def tracker_info(self):
        tracker_info = {'info_hash': self.info_hash,
                    'peer_id': '-TR2820-wa0n562rl3lu',
                    'port': random.randint(6881, 6889),
                    'uploaded': 0,
                    'downloaded' : 0,
                    'left': self.total_length,
                    'compact': 1,
                    'event': 'started'}
        return tracker_info

    def request_tracker(self):
        r = requests.get(self.tracker, params=self.tracker_info)
        return r.text

    def get_peers(self):
        '''
        Returns a list of pairs (str, int), (ip, port)
        Return a set, better than a list?
        '''
        peers =  utils.bdecode(self.request_tracker())['peers']
        assert len(peers) % 6 == 0
        byte_peers = [peers[i: i+6] for i in range(len(peers)/6)]
        human_readable_peers = {self._decode_peer(peer) for peer in byte_peers}
        return human_readable_peers

    def _decode_peer(self, byte_peer):
        assert len(byte_peer) == 6
        # WHY IS BYZE PEERS IN UNICODE?
        # TOM :)
        # big endian
        # spec: 4 first bytes ip adress (ip4: 1 byte per number)
        ip = '.'.join((str(ord(c)) for c in byte_peer[:4]))
        # sepc: 2 last bytes port number
        port = ord(byte_peer[4]) * 16 + ord(byte_peer[5])
        return (ip, int(port))

    def _handshake(self, peer):
        """ Peer tuple (str, int) being (ipadress, """
        pstr = 'BitTorrent protocol'
        pstrlen = chr(len(pstr))
        reserved = chr(0) * 8
        info_hash = self.info_hash
        peer_id = '-TR2820-wa0n562rl3lu'
        handshake = '{0}{1}{2}{3}{4}'.format(pstrlen, pstr, reserved, info_hash, peer_id)
        s = socket.socket()
        print(peer)
        s.connect(peer)
        s.send(handshake)
        return s.recv(len(handshake))



class Message():

    def __init__(self, *args):
        try:
            msg_len = ord(args[0])
            if msg_len == 0:
                pass
            else:
                msg_id = args[1]
                msg_payload = args[2]
        except:
            raise Exception # trouver mieux?
        self.msg_dict = {'len': msg_len, 'id': msg_id, 'payload': msg_payload}

        def send(self):
            msg_send = self.msg_dict['len']
            msg_send += self.msg_dict.get('id', '')
            msg_send += self.sg_dict.get('payload', '')
            return ''.join(self.msg_dict.values) # PROBLEME D'ORDRE... GROS PBME... LIST?
            return msg_send



if __name__ == '__main__':
    import utils
    import io

    with io.open('flagfromserver.torrent', 'rb') as iostream:
        tom_torrent = Torrent(utils.bdecode(iostream))
    print(tom_torrent.tracker_info)
    print(tom_torrent.info_hash)
    print(tom_torrent.request_tracker())
    peers = tom_torrent.get_peers()
    print(peers)
    print(tom_torrent._handshake(('96.126.104.219', 62859)))

    # user repr!
    # ord and chr
    # see as number
    # check struct
    # x.decode / encode
