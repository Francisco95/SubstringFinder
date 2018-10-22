from collections import defaultdict
from source.AFND import AFND
from source.automata import Automaton


def to_str(state: list):
    return "".join(map(str, state))


def to_list(state: str):
    return [int(x) for x in list(state)]


class AFD(Automaton):
    def __init__(self, alphabet, afnd: AFND=None):
        super().__init__([], defaultdict(list), None)
        self.set_alphabet(alphabet)
        if afnd is not None:
            self.from_afnd(afnd)

    def _get_init_state(self, afnd: AFND):
        init = self._dfs(afnd.transitions, afnd.init_state, [], "_")
        init.sort()
        return init

    def _next_state(self, from_state, afnd: AFND, char):
        to_state = []
        for st in from_state:
            visited = []
            for s in afnd.transitions[(st, char)]:
                visited = self._dfs(afnd.transitions, s, visited, "_")
            for v in visited:
                if v not in to_state:
                    to_state.append(v)

        if len(to_state)==0:
            to_state = ["-1"]

        to_state.sort()
        return to_state

    def _construct(self, state, a: AFND):
        for char in self.alphabet:
            s = self._next_state(state, a, char)
            self.new_connection(to_str(state), char, to_str(s))
            if s not in self.states:
                self._update(a, s)
                self._construct(s, a)

    def _update(self, a: AFND, state_to):
        self.states.append(state_to)
        if a.end_states[0] in state_to:
            self.add_end_state(state_to)

    def _dfs(self, transitions, state, visited, er):
        if state not in visited:
            visited.append(state)
            for v in transitions[(state, str(er))]:
                visited = self._dfs(transitions, v, visited, er)
        return visited

    def from_afnd(self, a: AFND):
        self.init_state = self._get_init_state(a)
        self._update(a, self.init_state)
        self._construct(self.init_state, a)


#  to test
# c = "*|.ab..aba"
# w = ERReader(c)
# a = AFND(list("ab"))
# a.expression_to_afnd(a.init_state, w, a.end_states[0])
# a.add_initial_loops()
# print("Transitions form")
# print("(state_From, char_readed) -> state_to")
# for k, v in a.transitions.items():
#     for d in v:
#         print("({}, {}) -> {}".format(k[0], str(k[1]), d))
# print(":::::::::::::::::::::::::")
# afd = AFD(list("ab"))
# print(":::::::::::")
# afd.from_afnd(a)
# print(afd.states)
# for k, v in afd.transitions.items():
#     print(k, v)
#
# afd = a.to_afd()
# print(afd.states)
# for k, v in afd.transitions.items():
#     print(k, v)

