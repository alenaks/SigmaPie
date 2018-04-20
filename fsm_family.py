#!/bin/python3

"""
   A class of Families of Finite State Machines.
   Copyright (C) 2017  Alena Aksenova
   
   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.
"""

from typing import TypeVar, Union
from fsm import *

FSMFam = TypeVar('FSMFam', bound='FSMFamily')

class FSMFamily(object):
    """
    This class encodes Family of Finite State Machines.
    Used for scanning and/or generating data.

    Attributes:
    -- transitions: triples of the worm [prev_state, transition, next_state].
    """

    def __init__(self:FSMFam, family:Union[None,list]=None) -> None:
        """ Initializes the FiniteStateMachine object. """
        
        if family == None:
            self.family = []
        else:
            self.family = family



    def run_all(self:FSMFam, w:str) -> None:
        """
        Runs ass the automata in the family and returns whether the
        string can be accepted by all of them.

        Arguments:
        -- self;
        -- w: a string to pass.

        Returns:
        -- True if w is accepted, otherwise False.
        """

        runs = []
        for f in self.family:
            runs.append(f.run_sp(w))
            
        return all(runs)
