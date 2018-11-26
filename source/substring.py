from source.reader import ERReader, _ALPHABET
from source.AFND import AFND, BackwardAFND
from source.AFD import AFD, to_str, to_list


class FindSubstring:
    def __init__(self, er):
        self.er = ERReader(er)
        self.afd, self.back_afd = self._get_afds()

    def _construct_afnd(self) -> AFND:
        afnd = AFND(_ALPHABET)
        afnd.expression_to_afnd(afnd.init_state, self.er, afnd.end_states[0])
        afnd.add_initial_loops()
        return afnd

    def _construct_backward_afnd(self, afnd: AFND) -> BackwardAFND:
        backward_afnd = BackwardAFND()
        backward_afnd.backward(afnd)
        return backward_afnd

    def _get_afds(self) -> (AFD, AFD):
        afnd = self._construct_afnd()
        back_afnd = self._construct_backward_afnd(afnd)
        return afnd.to_afd(), back_afnd.to_afd()

    def find_end(self, text):
        pointer = 0
        ends_visited = []
        state = self.afd.init_state
        while pointer < len(text):
            state = self.afd.transitions[(to_str(state), text[pointer])]
            if to_list(state[0]) in self.afd.end_states:
                ends_visited.append(pointer)
            pointer += 1
        return ends_visited

    def find_init(self, ends, text):
        inits = []
        for end in ends:
            p = 0
            state = self.back_afd.init_state
            while end - p >= 0:
                state = self.back_afd.transitions[(to_str(state), text[end-p])]
                if state[0] == "-1":
                    inits.append(-1)  # is not valid
                    break
                if to_list(state[0]) in self.back_afd.end_states:
                    inits.append(end - p)
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
