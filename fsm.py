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
        transitions (list): triples of the form [prev_state,
            transition, next_state].
    """

    def __init__(self, transitions=None):
        if transitions == None: self.transitions = []
        else: self.transitions = transitions


    def sl_to_fsm(self, grammar):
        """
        Creates FSM transitions based on the SL grammar.

        Arguments:
            grammar (list): SL ngrams.
        """

        if not grammar:
            raise ValueError("The grammar must not be empty.")
        self.transitions = [(i[:-1], i[-1], i[1:]) for i in grammar]


    def scan_sl(self, string, position=0):
        current_state = string[position]
        for i in range(len(string)):
            passed = False
            for j in range(len(self.transitions))
            if j[0] == i:
                passed = True

            if passed == True:
                self.scan_sl(string, position+1)
            else:
                return False

        return True





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



    def trim_fsm(self, markers=[">", "<"]):
        """
        This function trims useless states.
        1. Finds the initial state and collects the set of states to which one
           can come from that node and the nodes connected to it.
        2. Changes direction of the transitions and runs algorithm again to
           detect states drom which one cannot get to the final state.

        Arguments:
        -- self;
        -- markers (optional): list of markers used in the grammar.

        Results:
        -- self.transitions only contains useful transitions.
        """

        if self.transitions:
            can_start = self.__accessible_states(self.transitions, markers[0])
            self.transitions = [(i[2], i[1], i[0]) for i in can_start]
            mirrored = self.__accessible_states(self.transitions, markers[1])
            useful_transitions = [(i[2], i[1], i[0]) for i in mirrored]
            self.transitions = useful_transitions


    def __accessible_states(self, transitions, marker):
        """
        Auxiliary function that finds accessible states.

        Arguments:
        -- self;
        -- transitions: list of transitions;
        -- markers: list of markers used in the grammar.

        Returns:
        -- reachable: list of states that are reachable from
                      the initial state(s).
        """

        loop_trans, updated = self.transitions[:], self.transitions[:]

        reachable:list = []  # find initial/final transitions
        for i in self.transitions:
            if i[0][0] == i[0][-1] and i[0][-1] == marker:
                reachable.append(i)
                loop_trans.remove(i)
                updated.remove(i)
        loop_reach = reachable[:]

        previous_step:list = []  # loop while something is being detected
        while previous_step != updated:
            previous_step = updated[:]
            for i in loop_trans:
                for j in loop_reach:
                    if j[-1] == i[0]:
                        reachable.append(i)
                        updated.remove(i)
            loop_trans, loop_reach = updated[:], reachable[:]

        return reachable
