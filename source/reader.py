import string

OP = ["*", "|", "."]
_ALPHABET = list(string.ascii_lowercase +
                 string.ascii_uppercase +
                 string.digits +
                 " " +
                 "\n")


class ERReader:
    def __init__(self, input_char):
        self.word = list(input_char)
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


#  to test
# c = "*|.ab..abc"
# w = ERReader(c)
#
# c1 = w.read_kleen()
# print("leido pirmer char, op kleen y da el substring:", c1)
# c2, c3 = c1.read_or()
# print("leido segundo, op or y da 2 substring:", c2, c3)
# c4, c5 = c2.read_and()
# c6, c7 = c3.read_and()
# print("leido tercer, op and y da 2 substr:", c4, c5)
# print("leido cuarto, op and y da 2 substr:", c6, c7)
# c8, c9 = c6.read_and()
# print("leido ultimo, op and y da 2 substr:", c8, c9)
# print("-----------------")

