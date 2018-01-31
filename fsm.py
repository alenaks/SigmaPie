#!/bin/python3

"""
   A class of Finite State Machines.
   Copyright (C) 2017  Alena Aksenova
   
   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.
"""

from typing import TypeVar

FSM = TypeVar('FSM', bound='FiniteStateMachine')

class FiniteStateMachine(object):
    """
    This class encodes Finite State Machines.
    Used for scanning and/or generating data.

    Attributes:
    -- transitions: triples of the worm [prev_state, transition, next_state].
    """

    def __init__(self:FSM, transitions:list=[]) -> None:
        """ Initializes the FiniteStateMachine object. """
        
        self.transitions = transitions
        self.states = None # to be implemented


    def sl_states(self:FSM, grammar:list) -> None:
        """
        Translates (T)SL grammar in FSM transitions.

        Arguments:
        -- self;
        -- grammar: the list of ngrams.

        Results:
        -- self.transitions is rewritten as transitions that correspond
                            to the given grammar.
        """

        if not grammar:
            raise IndexError("The grammar is empty -- "
                             "FSM cannot be generated!")
        transitions = [(i[:-1], i[-1], i[1:]) for i in grammar]
        self.transitions = transitions


    def trim_fsm(self:FSM, markers:list=[">", "<"]) -> None:
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


    def __accessible_states(self:FSM, transitions:list, marker:str) -> list:
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
