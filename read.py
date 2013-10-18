import io


class Token():
    pass

class Tokenizer(): # token stream?
    def __init__(self, iostream):
        self._iostream = iostream
        self._counter = 0
        self._rules = [
            (lambda x: x in '0123456789', self._parse_string),
            (lambda x: x == 'i', self._parse_int),
            (lambda x: x == 'd', self._parse_dict),
            (lambda x: x == 'l', self._parse_list),
            (lambda x: x == 'e', self._parse_end) 
            ]

    def tokenize(self):
        while True:
            char = self._iostream.read(1)
            if char == '':
                raise StopIteration
            else:
                for test, rule in self._rules:
                    if test(char):
                        yield rule(char)

    def _parse_int(self, char):
        integer = ''
        while True:
            char = self._iostream.read(1)
            if char == 'e':
                return (int, int(integer))
            else:
                integer += char

    def _parse_string(self, char):
        length = char
        while True:
            char = self._iostream.read(1)
            if char == ':':
                break
            length += char
        length = int(length)
        return (str, self._iostream.read(length))

    def _parse_dict(self, char):
        value = (dict, self._counter)
        self._counter += 1
        return value

    def _parse_list(self, char):
        value = (list, self._counter)
        self._counter += 1
        return value

    def _parse_end(self, char):
        self._counter -= 1
        value = ('e', self._counter)
        return value

    def _create_dict(self):
        created_dict = {}
        while True:
            key = next(self.tokenize())
            if key[0] == 'e':
                return created_dict
            else:
                value = next(self.tokenize())
                created_dict[self._evaluate(key)()] = self._evaluate(value)()

    def _create_list(self):
        created_list = []
        while True:
            token = next(self.tokenize())
            if token[0] == 'e':
                return created_list
            else:
                created_list.append(self._evaluate(token)())

    def _create_struc(self):
        while True:
            try:
                token = next(self.tokenize())
                yield self._evaluate(token)()
            except Exception as e:
                print(e)
                break

    def _evaluate(self, token):
        token_type = token[0]
        if token_type == dict:
            return self._create_dict
        elif token_type == list:
            return self._create_list
        else:
            return lambda : token[1]



if __name__ == '__main__':
    with io.open('simple_torrent.txt', 'rb') as iostream:
        myTokenizer = Tokenizer(iostream)
        print([tok for tok in myTokenizer._create_struc()])


    with io.open('flagfromserver.torrent', 'rb') as iostream:
        myTokenizer = Tokenizer(iostream)
        print([tok for tok in myTokenizer._create_struc()])