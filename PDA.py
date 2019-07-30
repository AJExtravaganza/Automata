class PushdownAutomata:
    input_symbols_str = 'ab'
    pushdown_symbols_str = '$ab'
    initial_stack = '$'


    states = [0,1,2]
    final_states = [2,]

    #transitions defined (from_state, read_symbol, stack_top) : (to_state, stack_push)
    transitions = {
        (0, 'a', '$'): [(0, '$a'), ],
        (0, 'a', 'a'): [(0, 'aa'), ],
        (0, 'b', 'a'): [(1, ''), ],
        (0, '', '$')  : [(2, ''), ],
        (1, 'b', 'a'): [(1, ''), ],
        (1, '', '$')  : [(2, ''), ]
    }

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


pda = PushdownAutomata()

test_strings = ('', 'ab', 'aabb', 'ba', 'abab')

for string in test_strings:
    print (pda.string_in_language(string))

