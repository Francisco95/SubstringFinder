from source.reader import ERReader, _ALPHABET
from source.AFND import AFND, BackwardAFND
from source.AFD import AFD, to_str, to_list


_ALPHABET = ["a", "b"]

class FindSubstring:
    def __init__(self, er):
        self.er = ERReader(er)
        self.afd, self.back_afd = self._get_afds()
        # prints_dict(self.afd.transitions)
        # print(":::::::")
        # prints_dict(self.back_afd.transitions)

    def _construct_afnd(self) -> AFND:
        afnd = AFND(_ALPHABET)
        afnd.expression_to_afnd(afnd.init_state, self.er, afnd.end_states[0])
        afnd.add_initial_loops()
        # print(afnd.transitions)
        # print("transition for AFND")
        # prints_dict(afnd.transitions)
        return afnd

    def _construct_backward_afnd(self, afnd: AFND) -> BackwardAFND:
        backward_afnd = BackwardAFND()
        backward_afnd.backward(afnd)
        # print("transition for backward AFND")
        # prints_dict(backward_afnd.transitions)
        # print("end state is", backward_afnd.end_states)
        return backward_afnd

    def _get_afds(self) -> (AFD, AFD):
        afnd = self._construct_afnd()
        back_afnd = self._construct_backward_afnd(afnd)
        return afnd.to_afd(), back_afnd.to_afd()

    def find_end(self, text):
        pointer = 0
        ends_visited = []
        state = self.afd.init_state
        # print("states", self.afd.states)
        # print("end states", self.afd.end_states)
        # print("init state", self.afd.init_state)
        # print("TRANSICIONES")
        # prints_dict(self.afd.transitions)
        # print(state)
        while pointer < len(text):
            state = self.afd.transitions[(to_str(state), text[pointer])]
            # print(state)
            # print("estado", to_list(state[0]))
            if to_list(state[0]) in self.afd.end_states:
                ends_visited.append(pointer)
            pointer += 1
        # print("ends", ends_visited)
        return ends_visited

    def find_init(self, ends, text):
        inits = []
        # print("states", self.back_afd.states)
        # print("init states", self.back_afd.init_state)
        # print("end states", self.back_afd.end_states)
        for end in ends:
            p = 0
            state = self.back_afd.init_state
            # print("init state", state)
            while end - p >= 0:
                state = self.back_afd.transitions[(to_str(state), text[end-p])]
                # print("state", state)
                # print("estado", to_list(state[0]))
                if to_list(state[0]) in self.back_afd.end_states:
                    inits.append(end-p)
                    break
                p += 1
            if p > end:
                inits.append(-1)
        return inits

    def find(self, text: str):
        ends = self.find_end(list(text))
        inits = self.find_init(ends, list(text))
        for i, f in zip(inits, ends):
            if i != -1:
                print("[{}, {}]: {}".format(i, f, "".join(text[i:f+1])))


def prints_dict(a_dict):
    for k, values in a_dict.items():
        for v in values:
            print("({}, {}) -> {}".format(k[0], k[1], v))


# print("::::::::::::::::::::::")
# # find_substring = FindSubstring("|a..bab")
# find_substring = FindSubstring("|a.ab")
# # text = list("babbaba")
# # ends = find_substring.find_end(text)
# # print(ends)
# print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
# # inits = find_substring.find_init(ends, text)
# # print("inits and ends", inits, ends)
# find_substring.find("bab")
