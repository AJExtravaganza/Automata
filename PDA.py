class PushdownAutomata:

    def __init__(self, terminal_alphabet_str, stack_alphabet_str, initial_stack_str, states_list, final_states_list, transitions_dict):
        self.input_symbols = terminal_alphabet_str
        self.pushdown_symbols = stack_alphabet_str
        self.initial_stack = initial_stack_str
        self.states = states_list
        self.final_states = final_states_list
        self.transitions = transitions_dict

        # Check that the parameters are valid
        assert self.initial_stack in self.pushdown_symbols
        for final_state in self.final_states:
            assert final_state in self.states
        for condition, transitions in self.transitions.items():
            assert condition[0] in self.states
            assert condition[1] in self.input_symbols
            assert condition[2] in self.pushdown_symbols
            for transition in transitions:
                assert transition[0] in self.states
                for char in transition[1]:
                    assert char in self.pushdown_symbols

    def string_in_language(self, input_str, current_state=0, stack=None):
        # For initial call, initialise the stack
        if stack == None:
            stack = self.initial_stack

        if (current_state, input_str[:1], stack[-1:]) in self.transitions:
            valid_transitions = self.transitions[(current_state, input_str[:1], stack[-1])]
        else:
            valid_transitions = ()

        for transition in valid_transitions:
            if self.string_in_language(input_str[1:], transition[0], stack[:-1]+transition[1]):
                return True

        # For base case (all characters read), return success/failure
        if len(input_str) == 0:
            return current_state in self.final_states

        return False


# define parameters
terminal_alphabet = 'ab'
stack_alphabet = '$ab'
initial_stack = '$'

states = [0, 1, 2]
final_states = [2, ]

# transitions defined (from_state, read_symbol, stack_top) : (to_state, stack_push)
transitions = {
    (0, 'a', '$'): [(0, '$a'), ],
    (0, 'a', 'a'): [(0, 'aa'), ],
    (0, 'b', 'a'): [(1, ''), ],
    (0, '', '$'): [(2, ''), ],
    (1, 'b', 'a'): [(1, ''), ],
    (1, '', '$'): [(2, ''), ]
}


pda = PushdownAutomata(terminal_alphabet, stack_alphabet, initial_stack, states, final_states, transitions)

test_strings = ('', 'ab', 'aabb', 'ba', 'abab')

for string in test_strings:
    print (pda.string_in_language(string))

