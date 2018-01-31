#!/bin/python3

"""
   A class of Families of Finite State Machines.
   Copyright (C) 2017  Alena Aksenova
   
   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.
"""

from typing import TypeVar

FSMFam = TypeVar('FSMFam', bound='FSMFamily')

class FSMFamily(object):
    """
    This class encodes Family of Finite State Machines.
    Used for scanning and/or generating data.

    Attributes:
    -- transitions: triples of the worm [prev_state, transition, next_state].
    """

    def __init__(self:FSM, transitions:list=[]) -> None:
        """ Initializes the FiniteStateMachine object. """
        
        self.transitions = transitions
        self.states = None # to be implemented
