#!/bin/python3

"""
   A class of Families of Finite State Machines.
   Copyright (C) 2018  Alena Aksenova
   
   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.
"""
import sys, os
sys.path.insert(0, os.path.abspath('..'))

from PyKleene.fsm import *


class FSMFamily(object):
    """
    This class encodes Family of Finite State Machines.
    Used for scanning and/or generating data.

    Attributes:
    -- transitions: triples of the worm [prev_state, transition, next_state].
    """

    def __init__(self, family=None):
        """ Initializes the FSMFamily object. """
        if family == None: self.family = []
        else: self.family = family


    def run_all_fsm(self, string):
        """ Tells whether the given string is accepted by all
        the automata within the family.

        Arguments:
            string (str): the input string.

        Returns:
            bool: True if the string is accepted by all the
                fsms, otherwise False.
        """
        return all([f.sp_pass_string(string) for f in self.family])
