from collections import defaultdict
import numpy as np

class AFND:
    def __init__(self, alphabet):
        self.states = [0, 1]
        self.alphabet = alphabet
        self.transitions = {}
        self.init_state = 0
        self.end_state = 1

    def last_state(self):
        return self.states[-1]

    def new_states(self, n):
        r = []
        for i in range(n):
            self.states.append(self.last_state()+1)
            r.append(self.last_state())
        return r

    def new_connection(self, node1, literal, node2):
        self.transitions[(node1, literal)] = node2

    def or_expresion(self, init_state, er1, end_state, er2):
        news = self.new_states(4)
        self.new_connection(init_state, "", news[0])
        self.new_connection(init_state, "", news[1])
        self.new_connection(news[2], "", end_state)
        self.new_connection(news[3], "", end_state)
        self.expresion_to_AFND(news[0], er1, news[2])
        self.expresion_to_AFND(news[1], er2, news[3])

    def and_expresion(self, init_state, er1, end_state, er2):
        news = self.new_states(1)
        self.expresion_to_AFND(init_state, er1, news[0])
        self.expresion_to_AFND(news[0], er2, end_state)

    def kleen_expression(self, init_state, er, end_state):
        news = self.new_states(2)
        self.new_connection(init_state, "", news[0])
        self.new_connection(news[1], "", end_state)
        self.new_connection(news[1], "", news[0])
        self.new_connection(init_state, "", end_state)
        self.expresion_to_AFND(news[0], er, news[1])

    def add_initial_loops(self):
        for literal in self.alphabet:
            self.new_connection(self.init_state, literal, self.init_state)

    def expresion_to_AFND(self, init_state, er, end_state):
        er_splitted = list(er)
        # inside_er = "".join(er_splitted[1:])
        if er_splitted[0] is "*":
            if er_splitted[1] not in ["*", "|", "."]:
                self.kleen_expression(init_state, "".join(er_splitted[1:]))
            else:
                pass

        elif er_splitted[0] is "|":
            pass
        elif er_splitted[0] is ".":
            pass
        else:
            pass



class BackwardAFND:
    def __init__(self):
        pass

    def backward_connections(self):
        pass

    def swap_init_end_state(self):
        pass