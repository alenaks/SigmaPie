"""A class of Families of Finite State Machines. Copyright (C) 2019  Alena
Aksenova.

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 3 of the License, or (at your
option) any later version.
"""

from sigmapie.fsm import *


class FSMFamily(object):
    """
    This class encodes Family of Finite State Machines. Used for 
    a simple encoding of FSMs corresponding to SP languages.
    Attributes:
      transitions(list): triples of the form 
        [prev_state, transition, next_state].
    """

    def __init__(self, family=None):
        """Initializes the FSMFamily object."""
        if family is None:
            self.family = []
        else:
            self.family = family

    def run_all_fsm(self, string):
        """Tells whether the given string is accepted by all the automata of
        the family.

        Arguments:
            string (str): the input string.
        Returns:
            bool: True if the string is accepted by all the
                fsms, otherwise False.
        """
        return all([f.scan_sp(string) for f in self.family])
