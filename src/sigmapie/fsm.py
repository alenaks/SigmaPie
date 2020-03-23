"""A class of Finite State Machines. Copyright (C) 2019  Alena Aksenova.

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 3 of the License, or (at your
option) any later version.
"""


class FSM(object):
    """This class implements Finite State Machine.

    Attributes:
        initial (str): initial symbol;
        final (str): final symbol;
        transitions (list): triples of the form [prev_state,
            transition, next_state].
    """

    def __init__(self, initial, final, transitions=None):
        if transitions == None:
            self.transitions = []
        else:
            self.transitions = transitions

        self.initial = initial
        self.final = final

    def sl_to_fsm(self, grammar):
        """Creates FSM transitions based on the SL grammar.

        Arguments:
            grammar (list): SL ngrams.
        """
        if not grammar:
            raise ValueError("The grammar must not be empty.")
        self.transitions = [(i[:-1], i[-1], i[1:]) for i in grammar]

    def scan_sl(self, string):
        """Scans a given string using the learned SL grammar.

        Arguments:
            string (str): a string that needs to be scanned.
        Returns:
            bool: well-formedness value of the string.
        """
        if string[0] != self.initial or string[-1] != self.final:
            raise ValueError("The string is not annotated with " "the delimeters.")
        if not self.transitions:
            raise ValueError(
                "The transitions are empty. Extract the"
                " transitions using grammar.fsmize()."
            )

        k = len(self.transitions[0][0]) + 1
        for i in range(k - 1, len(string)):
            move_to_next = []
            for j in self.transitions:
                can_read = string[(i - k + 1) : (i + 1)] == "".join(j[0]) + j[1]
                move_to_next.append(can_read)

            if not any(move_to_next):
                return False

        return True

    def trim_fsm(self):
        """This function trims useless transitions.

        1. Finds the initial state and collects the set of states to which one
           can come from that node and the nodes connected to it.
        2. Changes direction of the transitions and runs algorithm again to
           detect states from which one cannot get to the final state.
        As the result, self.transitions only contains useful transitions.
        """
        if not self.transitions:
            raise ValueError("Transtitions of the automaton must" " not be emtpy.")
        can_start = self.accessible_states(self.initial)
        self.transitions = [(i[2], i[1], i[0]) for i in can_start]
        mirrored = self.accessible_states(self.final)
        self.transitions = [(i[2], i[1], i[0]) for i in mirrored]

    def accessible_states(self, marker):
        """Finds accessible states.

        Arguments:
            marker (str): initial or final state.
        Returns:
            list: list of transitions that can be made from
                the given initial or final state.
        """
        updated = self.transitions[:]

        # find initial/final transitions
        reachable = []
        for i in self.transitions:
            if i[0][0] == i[0][-1] == marker:
                reachable.append(i)
                updated.remove(i)

        # to keep copies that can be modified while looping
        mod_updated = updated[:]
        mod_reachable = []
        first_time = True

        # find transitions that can be reached
        while mod_reachable != [] or first_time:
            mod_reachable = []
            first_time = False
            for p in updated:
                for s in reachable:
                    if p[0] == s[2]:
                        mod_reachable.append(p)
                        mod_updated.remove(p)
            updated = mod_updated[:]
            reachable.extend(mod_reachable)

        return reachable

    def sp_build_template(self, path, alphabet, k):
        """Generates a template for the given k-SP path.

        Arguments:
            path (str): the sequence for which the template is generated;
            alphabet (list): list of all symbols of the grammar;
            k (int): window size of the grammar.
        """

        # creating the "sceleton" of the FSM
        for i in range(k - 1):
            # boolean shows whether the transition was accessed
            self.transitions.append([i, path[i], i + 1, False])

        # adding non-final loops
        newtrans = []
        for t in self.transitions:
            for s in alphabet:
                if s != t[1]:
                    newtrans.append([t[0], s, t[0], False])

        # adding final loops
        for s in alphabet:
            newtrans.append(
                [self.transitions[-1][2], s, self.transitions[-1][2], False]
            )

        self.transitions += newtrans

    def sp_fill_template(self, sequence):
        """Runs the imput sequence through the SP automaton and marks
        transitions if they were taken.

        Cleans
        transitions that were not taken afterwards.
        Arguments:
            sequence (str): sequence of symbols that needs to be
                passed through the automaton.
        """
        state = 0
        for s in sequence:
            for t in self.transitions:
                if (t[0] == state) and (t[1] == s):
                    state = t[2]
                    t[3] = True
                    break

    def sp_clean_template(self):
        """Removes transitions that were not accessed."""
        self.transitions = [i[:3] for i in self.transitions if i[3] == True]

    def scan_sp(self, string):
        """Runs the given sequence through the automaton.

        Arguments:
            string (str): string to run through the automaton.
        Returns:
            bool: True if input can be accepted by the automaton,
                otherwise False.
        """
        state = 0
        for s in string:
            change = False
            for t in self.transitions:
                if (t[0] == state) and (t[1] == s):
                    state = t[2]
                    change = True
                    break

            if not change:
                return False

        return True
