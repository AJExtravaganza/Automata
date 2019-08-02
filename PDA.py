class PushdownAutomata:
    terminal_symbols = ''
    pushdown_symbols = '$'
    initial_stack = '$'
    states = []
    final_states = []
    transitions = {}

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



    def prompt_for_state_count(self):
        return int(input('Enter number of states:'))


    def prompt_for_terminal_alphabet(self):
        raw_input = input("Enter terminal alphabet string:")
        assert ' ' not in raw_input
        return raw_input

    def prompt_for_transition_definitions(self):
        raw_input = input('Enter transitions:')
        if raw_input == '-1':
            return False

        separated_args = raw_input.split(' ')

        from_state = int(separated_args[0])
        read = separated_args[1]
        top = separated_args[2]
        to_state = int(separated_args[3])
        push = separated_args[4][::-1]

        assert from_state in self.states
        assert to_state in self.states
        assert read in self.terminal_symbols

        self.transitions.update({(from_state, read, top):(to_state, push)})
        self.prompt_for_transition_definitions()

    def prompt_for_final_states(self):
        raw_input = input('Enter final states, space-separated, followed by " -1"')
        assert raw_input[-3:] == ' -1'

        final_states = [int(x) for x in raw_input.split(' ')[:-1] if int(x) in self.states]

        return final_states


    # def __init__(self):
    #     terminal_alphabet = self.prompt_for_terminal_alphabet()
    #     initial_stack = '$'
    #     states = [x for x in range(0, self.prompt_for_state_count())]
    #     final_states = self.prompt_for_final_states()
    #     transitions = self.prompt_for_transition_definitions()
    #
    #     # Parse stack alphabet from transition definitions
    #     stack_alphabet = {'$'}
    #     for transition in self.transitions:
    #         for char in transition.value()[1]:
    #             self.pushdown_symbols.add(char)

    def generate_stack_alphabet(self):
        # Parse stack alphabet from transition definitions
        stack_alphabet = {'$'}
        for transition in self.transitions:
            for char in transition.value()[1]:
                stack_alphabet.add(char)

        return ''.join(stack_alphabet)

    def __init__(self, terminal_alphabet_str=None, initial_stack_str=None, states_list=None, final_states_list=None, transitions_dict=None, stack_alphabet_str=None):
        self.states = states_list if states_list else [x for x in range(0, self.prompt_for_state_count())]
        self.terminal_symbols = terminal_alphabet_str if terminal_alphabet_str else self.prompt_for_terminal_alphabet()
        self.initial_stack = initial_stack_str if initial_stack_str else '$'
        self.transitions = transitions_dict if transitions_dict else self.prompt_for_transition_definitions()
        self.final_states = final_states_list if final_states_list else self.prompt_for_final_states()
        self.pushdown_symbols = stack_alphabet_str if stack_alphabet_str else self.generate_stack_alphabet()

        # Check that the parameters are valid
        assert self.initial_stack in self.pushdown_symbols
        for final_state in self.final_states:
            assert final_state in self.states
        for condition, transitions in self.transitions.items():
            assert condition[0] in self.states
            assert condition[1] in self.terminal_symbols
            assert condition[2] in self.pushdown_symbols
            for transition in transitions:
                assert transition[0] in self.states
                for char in transition[1]:
                    assert char in self.pushdown_symbols





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


# pda = PushdownAutomata(terminal_alphabet, initial_stack, states, final_states, transitions, stack_alphabet)
pda = PushdownAutomata()

test_strings = ('', 'ab', 'aabb', 'ba', 'abab')

for string in test_strings:
    print (pda.string_in_language(string))

