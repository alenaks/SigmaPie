#!/bin/python3

"""
   A class of Finite State Machines.
   Copyright (C) 2018  Alena Aksenova

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.
"""


class FSM(object):
    """
    This class implements Finite State Machine.

    Attributes:
        initial (str): initial symbol;
        final (str): final symbol;
        transitions (list): triples of the form [prev_state,
            transition, next_state].
    """

    def __init__(self, initial, final, transitions=None):
        
        if transitions == None: self.transitions = []
        else: self.transitions = transitions

        self.initial = initial
        self.final = final


    def sl_to_fsm(self, grammar):
        """
        Creates FSM transitions based on the SL grammar.

        Arguments:
            grammar (list): SL ngrams.
        """

        if not grammar:
            raise ValueError("The grammar must not be empty.")
        self.transitions = [(i[:-1], i[-1], i[1:]) for i in grammar]


    def scan_sl(self, string):
        """
        Scans the given string with SL dependencies.

        Arguments:
            string (str): a string that needs to be scanned.

        Returns:
            bool: tells whether the string is well-formed.
        """
        if len(string) < 2:
            raise ValueError("The string is too short.")
        if string[0] != self.initial or string[-1] != self.final:
            raise ValueError("The string is not annotated with the delimeters.")
        if not self.transitions:
            raise ValueError("The transitions are empty.")

        k = len(self.transitions[0][0])+1
        for i in range(k-1, len(string)):
            move_to_next = []
            for j in self.transitions:
                if string[i-k+1:i+1] == "".join(j[0])+j[1]:
                    move_to_next.append(True)
                else:
                    move_to_next.append(False)
            if not any(move_to_next):
                return False
        return True


    def trim_fsm(self):
        """
        This function trims useless transitions.
        1. Finds the initial state and collects the set of states to which one
           can come from that node and the nodes connected to it.
        2. Changes direction of the transitions and runs algorithm again to
           detect states from which one cannot get to the final state.
        As the result, self.transitions only contains useful transitions.
        """
        if not self.transitions:
            raise ValueError("Transtitions of the automaton must"
                             " not be emtpy.")
        can_start = self.accessible_states(self.initial)
        self.transitions = [(i[2], i[1], i[0]) for i in can_start]
        mirrored = self.accessible_states(self.final)
        self.transitions = [(i[2], i[1], i[0]) for i in mirrored]
        

    def accessible_states(self, marker):
        """
        Finds accessible states.

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
        while mod_reachable != [] or first_time == True:
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


########################################################################

    def sp_template(self, seq, alphabet, k):
        """
        Generates a template for a k-SP path.

        Arguments:
        -- self;
        -- seq: path for which the template is being generated;
        -- alphabet: list of all symbols of the grammar;
        -- k: window of the grammar.
        """

        # creating the "sceleton" of the FSM
        for i in range(k-1):
            # boolean shows whether the transition was accessed
            self.transitions.append([i, seq[i], i+1, False])

        # adding non-final loops
        newtrans = []
        for t in self.transitions:
            for s in alphabet:
                if s != t[1]:
                    newtrans.append([t[0], s, t[0], False])

        # adding final loops
        for s in alphabet:
            newtrans.append([self.transitions[-1][2], s, self.transitions[-1][2], False])

        self.transitions += newtrans


    def run_sp(self, w):
        """
        Runs a word through an SP sequence automaton.
        WARNING: SP automata only!
            -- deterministic;
            -- state 0 is the only initial state;
            -- every state is final.

        Arguments:
        -- self;
        -- w: string to run through the automaton.

        Returns:
        -- True if w can be accepted by the automaton, otherwise False.
        """

        state = 0
        for s in w:
            change = False
            for t in self.transitions:
                if (t[0] == state) and (t[1] == s):
                    state = t[2]
                    change = True
                    break

            if change == False:
                return False

        return True


    def run_learn_sp(self, w):
        """
        Runs a word through an SP sequence automaton, and marks transitions
        if they were taken.
        WARNING: SP automata only!
            -- deterministic;
            -- state 0 is the only initial state;
            -- every state is final.

        Arguments:
        -- self;
        -- w: string to run through the automaton.

        Results:
        -- Transitions that are taken are marked.
        """

        state = 0

        for s in w:
            for t in self.transitions:
                if (t[0] == state) and (t[1] == s):
                    state = t[2]
                    t[3] = True
                    break


    def sp_clean(self):
        """
        Removes the "untouched" transitions from the automaton.

        Attributes:
        -- self.

        Results:
        -- "cleans" the list of the transitions.
        """

        new = []
        for i in self.transitions:
            if i[3] == True:
                new.append(i[0:3])
        self.transitions = new




