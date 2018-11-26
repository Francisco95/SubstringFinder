import string

OP = ["*", "|", "."]
_ALPHABET = list(string.ascii_lowercase +
                 string.ascii_uppercase +
                 string.digits +
                 " " +
                 "\n")


def _er_to_list(er: str):
    extra = '\n'
    tmps = []
    if '\n' in er:
        tmps = er.split("\n")
    elif '\\n' in er:
        tmps = er.split('\\n')
    else:
        tmps = [er]
        extra = ""
    r = []
    r.extend(tmps[0])
    for i in range(len(tmps)-1):
        r.extend(extra)
        r.extend(tmps[i+1])
    return r


class ERReader:
    def __init__(self, input_char):
        self.word = _er_to_list(input_char)
        self.pointer = 0

    def _search_valid_two_string(self):
        tmp_pointer = self.pointer
        need_to_read = 1
        while need_to_read > 0 and tmp_pointer < len(self.word):
            if self.word[tmp_pointer] in OP:
                if self.word[tmp_pointer] != "*":
                    need_to_read += 1
                else:  # not valid string
                    tmp_pointer = len(self.word)
            else:
                need_to_read -= 1
            tmp_pointer += 1

        if tmp_pointer == len(self.word):
            raise ValueError("string is not valid")

        return tmp_pointer

    def read_kleen(self):
        if not self.valid():
            return self
        self.pointer += 1
        return ERReader("".join(self.word[self.pointer:]))

    def read_or(self):
        if not self.valid():
            return self

        self.pointer += 1
        second_string_init = self._search_valid_two_string()
        return (ERReader("".join(self.word[self.pointer:second_string_init])),
                ERReader("".join(self.word[second_string_init:])))

    def read_and(self):
        if not self.valid():
            return self
        self.pointer += 1
        second_string_init = self._search_valid_two_string()
        return (ERReader("".join(self.word[self.pointer:second_string_init])),
                ERReader("".join(self.word[second_string_init:])))

    def reset(self):
        self.pointer = 0

    def valid(self):
        return len(self.word) > 1

    def char(self, pos):
        return self.word[pos]

    def __str__(self):
        return "".join(self.word)
