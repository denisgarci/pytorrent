import io

class Parser():

    def __init__(self, iostream):
        self._iostream = iostream
        self._rules = {c: self._parse_string for c in '0123456789'}
        self._rules['i'] = self._parse_int
        self._rules['d'] = self._parse_dict
        self._rules['l'] = self._parse_list

        #self._types = {c: str for c in '0123456789'}
        #self._types['i'] = int
        #self._types['d'] = dict
        #self._types['l'] = list

        #self._end = {c: ':' for c in '0123456789'}
        #self._end['i'] = 'e'
        #self._end['d'] = 'e'
        #self._end['l'] = 'e'

    #def _parse_char(self, c):
        #parse_type = self._type[c]
        #parse_end = self._end[c]
        #while True:
            #char = self._iostream.read(1)
            #acc = parse_type()
            #if char == parse_end:
                #return parse_type(acc)


    def _parse_string(self, c):
        assert c in '0123456789'
        length = c
        while True:
            char = self._iostream.read(1)
            if char == ':':
                length = int(length)
                return self._iostream.read(length)
            length += char

    def _parse_int(self, c):
        assert c == 'i'
        int_val = ''
        while True:
            char = self._iostream.read(1)
            if char == 'e':
                return int(int_val)
            int_val += char

    def _parse_list(self, c):
        assert c == 'l'
        list_val = []
        while True:
            char = self._iostream.read(1)
            if char == 'e':
                return list_val
            list_val.append(self._rules[char](char))

    def _parse_dict(self, c):
        assert c == 'd'
        dict_val = {}
        while True:
            char = self._iostream.read(1)
            if char == 'e':
                return dict_val
            key = self._rules[char](char)
            value_char = self._iostream.read(1)
            value = self._rules[value_char](value_char)
            dict_val[key] = value

    def parse(self):
        char = self._iostream.read(1)
        assert char == 'd'
        return self._rules['d']('d')


if __name__ == '__main__':
    with io.open('simple_torrent.txt', 'rb') as iostream:
        my_parser = Parser(iostream)
        print(my_parser.parse())

    with io.open('flagfromserver.torrent', 'rb') as iostream:
        my_parser = Parser(iostream)
        print(my_parser.parse())




