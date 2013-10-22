
def bdecode(iostream):
    """
    with io.open('simple_torrent.txt', 'rb') as iostream:
        bdecode(iostream)
    {'spam': ['a', 'b']}
    """

    def decode_str(c):
        assert c in '0123456789'
        length = c
        while True:
            char = iostream.read(1)
            if char == ':':
                length = int(length)
                return iostream.read(length)
            length += char

    def decode_int(c):
        assert c == 'i'
        int_val = ''
        while True:
            char = iostream.read(1)
            if char == 'e':
                return int(int_val)
            int_val += char

    def decode_list(c):
        assert c == 'l'
        list_val = []
        while True:
            char = iostream.read(1)
            if char == 'e':
                return list_val
            list_val.append(decode_rules[char](char))

    def decode_dict(c):
        assert c == 'd'
        dict_val = {}
        while True:
            char = iostream.read(1)
            if char == 'e':
                return dict_val
            key = decode_rules[char](char)
            value_char = iostream.read(1)
            value = decode_rules[value_char](value_char)
            dict_val[key] = value

    decode_rules = {c: decode_str for c in '0123456789'}
    decode_rules['i'] = decode_int
    decode_rules['d'] = decode_dict
    decode_rules['l'] = decode_list

    char = iostream.read(1)
    assert char == 'd' # a torrent file should start with a dict
    return decode_rules['d']('d')

def bencode(data):
    #"""
    #>>> bencode({'spam': ['a', 'b']})
    #d4:spaml1:a1:bee
    #"""

    def encode_int(integer):
        """
        >>> encode_int(42)
        i42e
        """
        return 'i{0}e'.format(integer)

    def encode_str(string):
        """
        >>> encode_str("")
        "0:"
        >>> encode_str("hello")
        5:hello
        """
        return '{0}:{1}'.format(len(string), string)

    def encode_list(a_list):
        """
        >>> encode_list(['a', 'b'])
        l1:a1:be
        """
        return 'l{0}e'.format(''.join(encode(item) for item in a_list))

    def encode_dict(a_dict):
        """
        >>> encode_dict({'a':'b'})
        d1:a1:be
        """
        return 'd{0}e'.format(''.join('{0}{1}'.format((bencode(key), bencode(value)) for key, value in a_dict.iteritems())))

    encode_rules = {int : encode_int,
                    str : encode_str,
                    dict : encode_dict,
                    list : encode_list}

    return encode_rules[type(data)](data)

if __name__ == '__main__':
    import io
    import doctest

    with io.open('simple_torrent.txt', 'rb') as iostream:
        my_decoder = bdecode(iostream)
        print(my_decoder)

    with io.open('flagfromserver.torrent', 'rb') as iostream:
        my_decoder = bdecode(iostream)
        print(my_decoder)

    doctest.testmod()



