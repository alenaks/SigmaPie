#!/bin/python3

"""
   A class of Strictly Piecewise Grammars.
   Copyright (C) 2017  Alena Aksenova
   
   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.
"""

from typing import TypeVar, Union, Tuple, List
from random import choice
from itertools import product
from helper import *
from fsm_family import *
from fsm import *
from grammar import *

PosStP = TypeVar('PosStP', bound='PosSP')
NegStP = TypeVar('NegStP', bound='NegSP')

class PosSP(PosGram):
    """ A class for positive strictly piecewise grammars.

    Attributes:
    -- alphabet: the list of symbols used in the given language;
    -- grammar: the list of grammatical rules;
    -- k: the locality measure;
    -- data: the language data given as input;
    -- data_sample: the generated data sample;
    -- fsm: the finite state machine that corresponds to the given grammar.
    """

    def __init__(self:PosStP, alphabet:Union[None,list]=None, grammar:Union[None,List[tuple]]=None, k:int=2,
                 data:Union[list,None]=None) -> None:
        """ Initializes the PosSL object. """
        
        super().__init__(alphabet, grammar, k, data)
        data_sample = None
        self.fsm = FSMFamily()


        
    def learn_fsm(self:PosStP) -> None:
        if not self.data:
            raise ValueError("The data is not provided")

        seq = self.generate_paths()
        for i in seq:
            f = FiniteStateMachine()
            f.sp_template(i, self.alphabet, self.k)
            self.fsm.family.append(f)

        for f in self.fsm.family:
            for d in self.data:
                f.run_learn_sp(d)

        for f in self.fsm.family:
            f.sp_clean()



    def generate_sample(self:PosStP) -> None:
        pass



    def scan(self:PosStP) -> None:
        pass



    def change_polarity(self:PosStP) -> None:
        pass


    def generate_paths(self:PosStP) -> None:
        return product(self.alphabet, repeat=self.k-1)



# TESTING AREA
a = PosSP()
a.alphabet = ["a", "b"]
a.data = ["ab", "aaaaabaaa", "aaaa", "b"]
a.k = 3
a.learn_fsm()
