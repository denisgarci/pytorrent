import struct
import random
from hashlib import sha1
import requests


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
    def hash_info(self):
        return sha1(utils.bencode(self.info)).digest()

    @property
    def tracker_info(self):
        tracker_info = {'info_hash': self.hash_info,
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
        peers=  utils.bdecode(self.request_tracker())['peers']
        return struct.unpack(">L", peers)[0]

if __name__ == '__main__':
    import utils
    import io

    with io.open('flagfromserver.torrent', 'rb') as iostream:
        tom_torrent = Torrent(utils.bdecode(iostream))
    print(tom_torrent.tracker_info)
    print(tom_torrent.hash_info)
    print(tom_torrent.request_tracker())
    print(tom_torrent.get_peers())
