from collections import defaultdict


class Automaton:
    def __init__(self, states, transitions=None, init_state=0):
        self.states = states
        if transitions is None:
            self.transitions = defaultdict(list)
        else:
            self.transitions = transitions
        self.init_state = init_state
        self.end_states = []
        self.alphabet = []

    def set_alphabet(self, alphabet):
        self.alphabet = alphabet

    def last_state(self):
        return self.states[-1]

    def new_connection(self, state1, literal, state2):
        # print(state1, literal, state2)
        self.transitions[(state1, str(literal))].append(state2)

    def add_end_state(self, state):
        self.end_states.append(state)
