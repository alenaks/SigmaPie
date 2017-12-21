#!/bin/python3

"""
   A class of Strictly Local Grammars.
   Copyright (C) 2017  Alena Aksenova
   
   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.
"""

from typing import TypeVar

FSM = TypeVar('FSM', bound='FiniteStateMachine')

class FiniteStateMachine(object):
    """ Class of Finite State Machines """

    def __init__(self:FSM, transitions:list=[]) -> None:
        """ Initialize the list of transitions"""
        self.transitions = transitions
        self.states = None # to be implemented


    def sl_states(self:FSM, grammar:list) -> None:
        """ Translate SL grammar in FSM transitions """

        if not grammar:
            raise IndexError("The grammar is empty -- "
                             "FSM cannot be generated!")
        transitions = [(i[:-1], i[-1], i[1:]) for i in grammar]
        self.transitions = transitions


    def trim_fsm(self:FSM, markers:list=[">", "<"]) -> None:
        """ FSA's useless states trimmer. Algorithm (C) Gordon Pace (U of Malta).
            Finds the initial state and collect the set of states to which one can
            come from that node and the nodes connected to it.
            My modification: change direction of the transitions and run this
            algorithm to detect states drom which one cannot get to the final state.
        """

        if self.transitions:
            can_start = self.__accessible_states(self.transitions, markers[0])
            self.transitions = [(i[2], i[1], i[0]) for i in can_start]
            mirrored = self.__accessible_states(self.transitions, markers[1])
            useful_transitions = [(i[2], i[1], i[0]) for i in mirrored]
            self.transitions = useful_transitions


    def __accessible_states(self:FSM, transitions:list, marker:str) -> list:
        """ Auxiliary function that finds accessible states """

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
