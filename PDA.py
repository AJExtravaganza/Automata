class PushdownAutomata:
    terminal_symbols = ''
    pushdown_symbols = '$'
    initial_stack = '$'
    states = []
    final_states = []
    transitions = {}

    # Test whether input_str is in language defined by current state of PushdownAutomata object
    def string_in_language(self, input_str, current_state=0, stack=None):
        # For initial call, initialise the stack
        if stack == None:
            stack = self.initial_stack

        # Get all possible transitions (only single transition for DPDA)
        if (current_state, input_str[:1], stack[-1:]) in self.transitions:
            valid_transitions = self.transitions[(current_state, input_str[:1], stack[-1])]
        else:
            valid_transitions = ()

        # Instantiate a recursive test for each transition
        for transition in valid_transitions:
            if self.string_in_language(input_str[1:], transition[0], stack[:-1]+transition[1]):
                return True

        # For base case (all characters read), return success/failure
        if len(input_str) == 0:
            return current_state in self.final_states

        return False

    # Test whether string of individually-entered char inputs is in language defined by current state of PushdownAutomata object
    def string_in_language_single_char_input(self, current_state=0, stack=None):
        # For initial call, initialise the stack
        if stack == None:
            stack = self.initial_stack

        # Prompt for letter
        input_char = input(f'\nCurrent status {current_state}:{stack[::-1]}, Enter input: ')
        print(input_char, end='')


        # For base case (all characters read), return success/failure
        if input_char == '.':
            print(f'\nString {"accepted" if current_state in self.final_states else "rejected"}')

        # Get all possible transitions (only single transition for DPDA)
        if (current_state, input_char, stack[-1:]) in self.transitions:
            valid_transitions = self.transitions[(current_state, input_char, stack[-1])]
        else:
            valid_transitions = ()

        # Instantiate a recursive test for each transition
        for transition in valid_transitions:
            self.string_in_language_single_char_input(transition[0], stack[:-1] + transition[1])

    def prompt_for_state_count(self):
        return int(input('Enter number of states:'))


    def prompt_for_terminal_alphabet(self):
        raw_input = input('Enter terminal alphabet string:')
        assert ' ' not in raw_input
        return raw_input

    def prompt_for_transition_definitions(self):
        raw_input = input('Enter transitions:')
        while raw_input != '-1':

            separated_args = raw_input.split(' ')

            from_state = int(separated_args[0])
            read = separated_args[1]
            top = separated_args[2]
            to_state = int(separated_args[3])
            push = separated_args[4][::-1] if separated_args[4] is not '.' else ''

            assert from_state in self.states
            assert to_state in self.states
            assert read in self.terminal_symbols

            # To make compatible with NPDAs as well as DPDAs
            # value of transition dict holds a list of possible valid transitions given a unique key
            if (from_state, read, top) in self.transitions:
                self.transitions[(from_state, read, top)].append((to_state, push))
            else:
                self.transitions.update({(from_state, read, top):[(to_state, push)]})

            raw_input = input('Enter transitions:')

    def prompt_for_final_states(self):
        raw_input = input('Enter final states, space-separated, followed by " -1"')
        assert raw_input[-3:] == ' -1'

        final_states = [int(x) for x in raw_input.split(' ')[:-1] if int(x) in self.states]

        return final_states

    def generate_stack_alphabet(self):
        # Parse stack alphabet from transition definitions
        stack_alphabet = {'$'}
        for transition_key in self.transitions.values():
            for transition in transition_key:
                for char in transition[1]:
                    stack_alphabet.add(char)

        return ''.join(stack_alphabet)

    def __init__(self, terminal_alphabet_str=None, initial_stack_str=None, states_list=None, final_states_list=None, transitions_dict=None, stack_alphabet_str=None):
        self.states = states_list if states_list else [x for x in range(0, self.prompt_for_state_count())]
        self.terminal_symbols = terminal_alphabet_str if terminal_alphabet_str else self.prompt_for_terminal_alphabet()
        self.initial_stack = initial_stack_str if initial_stack_str else '$'
        if transitions_dict:
            self.transitions = transitions_dict
        else:
            self.prompt_for_transition_definitions()
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

# Instantiate blank pda (definition via input()
pda = PushdownAutomata()

test_strings = ('', 'ab', 'aabb', 'ba', 'abab')
print('\n\n')

# Test some strings directly
for string in test_strings:
    print (f'"{string}" in language? {pda.string_in_language(string)}')

# Test example from specification, character-by-character
pda.string_in_language_single_char_input()

