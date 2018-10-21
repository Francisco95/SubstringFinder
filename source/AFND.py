from collections import defaultdict
from source.reader import ERReader, _ALPHABET
from source.automata import Automaton


class AFND(Automaton):
    def __init__(self, alphabet):
        super().__init__([0, 1], defaultdict(list), 0)
        self.set_alphabet(alphabet)
        self.add_end_state(1)

    def new_states(self, n):
        r = []
        for i in range(n):
            self.states.append(self.last_state()+1)
            r.append(self.last_state())
        return r

    def or_expression(self, init_state, er1, end_state, er2):
        news = self.new_states(4)
        self.new_connection(init_state, ERReader("_"), news[0])
        self.new_connection(init_state, ERReader("_"), news[1])
        self.new_connection(news[2], ERReader("_"), end_state)
        self.new_connection(news[3], ERReader("_"), end_state)
        self.expression_to_afnd(news[0], er1, news[2])
        self.expression_to_afnd(news[1], er2, news[3])

    def and_expression(self, init_state, er1, end_state, er2):
        news = self.new_states(1)
        self.expression_to_afnd(init_state, er1, news[0])
        self.expression_to_afnd(news[0], er2, end_state)

    def kleen_expression(self, init_state, er, end_state):
        news = self.new_states(2)
        self.new_connection(init_state, ERReader("_"), news[0])
        self.new_connection(init_state, ERReader("_"), end_state)
        self.new_connection(news[1], ERReader("_"), end_state)
        self.new_connection(news[1], ERReader("_"), news[0])
        self.expression_to_afnd(news[0], er, news[1])

    def add_initial_loops(self):
        for literal in self.alphabet:
            self.new_connection(self.init_state, literal, self.init_state)

    def expression_to_afnd(self, init_state, er: ERReader, end_state):
        if er.char(0) is "*":
            self.kleen_expression(init_state, er.read_kleen(), end_state)

        elif er.char(0) is "|":
            er1, er2 = er.read_or()
            self.or_expression(init_state, er1, end_state, er2)

        elif er.char(0) is ".":
            er1, er2 = er.read_and()
            self.and_expression(init_state, er1, end_state, er2)
        elif er.char(0) is "":
            pass
        else:
            self.new_connection(init_state, er, end_state)

    def to_afd(self):
        from source.AFD import AFD
        return AFD(self.alphabet, afnd=self)


class BackwardAFND(AFND):
    def __init__(self, alphabet=""):
        super().__init__(alphabet)

    def backward(self, afnd: AFND):
        #  swap the init state with the end state
        self.end_states = [afnd.init_state]
        self.init_state = afnd.end_states[0]
        self.set_alphabet(afnd.alphabet)
        self.states = afnd.states
        self._backward_connections(afnd.transitions)

    def _backward_connections(self, transitions):
        self.transitions = defaultdict(list)  # reset, just in case
        for k, values in transitions.items():
            # print(values)
            for v in values:
                # print(v)
                if k[0] != v:  # this avoid the initial loops
                    self.transitions[(v, k[1])].append(k[0])


#  to test
# c = "*|.ab..abc"
# w = ERReader(c)
# a = AFND(list("abc"))
# a.expression_to_afnd(a.init_state, w, a.end_states[0])
# a.add_initial_loops()
# print("Transitions form")
# print("(state_From, char_readed) -> state_to")
# for k, v in a.transitions.items():
#     for d in v:
#         print("({}, {}) -> {}".format(k[0], str(k[1]), d))
# print(":::now the reverse AFND")
# ra = BackwardAFND()
# ra.backward(a)
# print("Transitions form")
# print("(state_From, char_readed) -> state_to")
# for k, v in ra.transitions.items():
#     for d in v:
#         print("({}, {}) -> {}".format(k[0], str(k[1]), d))

# c = "|a..bab"
# a = AFND(_ALPHABET)
# w = ERReader(c)
# a.expression_to_afnd(a.init_state, w, a.end_states[0])
# a.add_initial_loops()
# for k, v in a.transitions.items():
#     for d in v:
#         print("({}, {}) -> {}".format(k[0], str(k[1]), d))
