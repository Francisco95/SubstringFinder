


class State:
    def __init__(self, this, state_type):
        self.thisNode = this
        self.input_to_connect = []
        self.next_node = []
        self.thisType = state_type

    def add_connection(self, literal, node):
        self.input_to_connect.append(literal)
        self.next_node.append(node)
