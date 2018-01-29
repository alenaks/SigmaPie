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
from helper import *
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

<<<<<<< HEAD
    def __init__(self:PosStP, alphabet:Union[None,list]=None, grammar:Union[None,List[tuple]]=None, k:int=2,
=======
    def __init__(self:PosG, alphabet:Union[None,list]=None, grammar:Union[None,List[tuple]]=None, k:int=2,
>>>>>>> 01c14fc758b9eb1ea95f92920c0f8411faf53f70
                 data:Union[list,None]=None, edges=[">", "<"]) -> None:
        """ Initializes the PosSL object. """
        
        super().__init__(alphabet, grammar, k, data, edges)
        self.fsm = FiniteStateMachine()
