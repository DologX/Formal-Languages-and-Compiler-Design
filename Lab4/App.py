def complete_with_spaces(string, final_length):
    return string + " "*(final_length - len(string))


def print_transitions(transitions):
    column_length = 10
    alphabet = sorted(list(transitions[list(transitions.keys())[0]].keys()))

    print(complete_with_spaces("", column_length), end='|')
    for value in alphabet:
        print(complete_with_spaces(value, column_length), end='|')
    print()

    for start_state in transitions.keys():
        print(complete_with_spaces(start_state, column_length), end='|')
        for value in sorted(list(transitions[start_state].keys())):
            end_states = ""
            for end_state in transitions[start_state][value]:
                end_states += end_state + ','
            end_states = end_states[:-1]
            print(complete_with_spaces(end_states, column_length), end='|')
        print()


def print_menu():
    print("Menu")
    print("Type \'exit\' to exit the program")
    print("Type \'1\' to print the set of states")
    print("Type \'2\' to print the alphabet")
    print("Type \'3\' to print the transitions")
    print("Type \'4\' to print the initial state")
    print("Type \'5\' to print the final states")
    print("Type \'6\' to check if a sequence is accepted by the FA")


def check_sequence(sequence, alphabet, transitions, initial_state, final_states):
    current_state = initial_state

    """
    print(current_state)
    print(sequence)
    print("\n\n\n")
    """

    while len(sequence) > 0:
        first_character = sequence[0]

        if first_character not in alphabet:
            return False

        if len(transitions[current_state][first_character]) != 1:
            return False

        current_state = transitions[current_state][first_character][0]
        sequence = sequence[1:]

        """
        print(current_state)
        print(sequence)
        print("\n\n\n")
        """

    if current_state in final_states:
        return True
    else:
        return False


def run():
    finite_automata_file = open("DFA.in", "r")

    states = []
    alphabet = []
    transitions = {}
    initial_state = ""
    final_states = []

    line_number = 0
    for line in finite_automata_file:
        line_number += 1
        if line_number == 1:
            states = line[:-1].split(';')
        elif line_number == 2:
            alphabet = line[:-1].split(';')
        elif line_number == 3:
            transitions_elements = line[:-1].split(';')

            for state in states:
                transitions[state] = {}
                for alphabet_value in alphabet:
                    transitions[state][alphabet_value] = []

            for transitions_element in transitions_elements:
                start_state, value = transitions_element.split('->')[0].split(',')
                end_states = transitions_element.split('->')[1].split(',')

                for end_state in end_states:
                    if end_state not in transitions[start_state][value]:
                        transitions[start_state][value].append(end_state)

        elif line_number == 4:
            initial_state = line[:-1]
        elif line_number == 5:
            final_states = line[:-1].split(';')

    while True:
        print_menu()
        command = input(">>>")
        if command == "exit":
            finite_automata_file.close()
            return
        elif command == "1":
            print("States:")
            print(states)
        elif command == "2":
            print("Alphabet:")
            print(alphabet)
        elif command == "3":
            print("Transitions:")
            print_transitions(transitions)
        elif command == "4":
            print("Initial state:")
            print(initial_state)
        elif command == "5":
            print("Final states:")
            print(final_states)
        elif command == "6":
            sequence = input("Your sequence: ")
            if check_sequence(sequence, alphabet, transitions, initial_state, final_states):
                print("Your sequence is accepted by the FA")
            else:
                print("Your sequence is NOT accepted by the FA")


run()
