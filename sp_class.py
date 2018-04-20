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
        self.fsm = None


    def learn(self:PosStP) -> None:
        """
        Learns possible subsequences of the given length.

        Arguments:
        -- self.

        Results:
        -- self.grammar is updated.
        """

        if not self.data:
            raise ValueError("The data is not provided")

        self.grammar = []
        gr = []

        for i in self.data:
            ss = self.subsequences(i)
            for j in ss:
                if j not in gr:
                    gr.append(j)
        for i in gr:
            self.grammar.append(tuple(i))


    def fsmize(self:PosStP) -> None:
        """
        Creates FSM family for the given SP grammar.

        Arguments:
        -- self.

        Results:
        -- fills self.fsm with the corresponding FSMFamily object.
        """

        self.fsm = FSMFamily()

        if not self.grammar:
            self.learn()

        seq = self.generate_paths(self.k-1)
        for i in seq:
            f = FiniteStateMachine()
            f.sp_template(i, self.alphabet, self.k)
            self.fsm.family.append(f)

        for f in self.fsm.family:
            for d in self.grammar:
                f.run_learn_sp(d)

        for f in self.fsm.family:
            f.sp_clean()


    def generate_sample(self:PosStP) -> None:
        raise NotImplemented("Coming soon!")


    def scan(self:PosStP, w:str) -> None:
        """
        Accepts of rejects the given string.

        Arguments:
        -- self;
        -- w: string to be checked.

        Returns:
        -- boolean depending on well-formedness of the string.
        """
        
        if self.fsm == None:
            self.fsmize()

        return self.fsm.run_all(w)


    def change_polarity(self:PosStP) -> None:
        pass
    

    def generate_paths(self:PosStP, rep:int) -> None:
        """
        Generates all possible permutations of the alphabet items
        of the desired length.

        Arguments:
        -- self;
        -- rep: length of the generated sequences.

        Returns:
        -- the list of generated sequences.
        
        """
        
        return product(self.alphabet, repeat=rep)


    def subsequences(self:PosStP, string:str) -> list:
        """
        Extracts subsequences of the length self.k out of a
        given word.

        Arguments:
        -- self;
        -- string: string from which the substrings need to
                   be extracted.

        Returns:
        -- list of subsequences of that string.
        """

        choices = []
        s = 0
        e = len(string) - self.k
        for i in range(self.k):
            choices.append(range(s, e + 1))
            s += 1
            e += 1

        general = []
        local = []
        
        for i in choices[0]:
            for j in choices[1]:
                if i < j:
                    local.append([i,j])
        general = local[:]
        local = []
        
        choices = choices[2:]


        for layer in choices:
            for item in layer:
                for prefix in general:
                    if prefix[-1] < item:
                        local.append(prefix + [item])
            general = local[:]
            local = []

        subseq = []
        for i in general:
            new = []
            for j in i:
                new.append(string[j])
            subseq.append(new)

        return subseq


    def opposite_polarity(self:PosStP) -> list:
        """
        For a grammar with given polarity, returns set of ngrams
        of the opposite polarity.

        Arguments:
        -- self.

        Returns:
        -- a list of ngrams opposite to the ones given as input.
        """

        opposite = []
        possib = self.generate_paths(self.k)
        for i in possib:
            if i not in self.grammar:
                opposite.append(i)
                
        return opposite



class NegSP(PosSP):
    """ A class for negative strictly piecewise grammars.

    Attributes:
    -- alphabet: the list of symbols used in the given language;
    -- grammar: the list of grammatical rules;
    -- k: the locality measure;
    -- data: the language data given as input;
    -- data_sample: the generated data sample;
    -- fsm: the finite state machine that corresponds to the given grammar.
    """

    def learn(self:NegStP) -> None:
        """
        Learns possible subsequences of the given length.

        Arguments:
        -- self.

        Results:
        -- self.grammar is updated.
        """

        if self.data:
            self.extract_alphabet()
            
        super().learn()
        self.grammar = self.opposite_polarity()


    def fsmize(self:PosStP) -> None:
        """
        Creates FSM family for the given SP grammar.

        Arguments:
        -- self.

        Results:
        -- fills self.fsm with the corresponding FSMFamily object.
        """

        self.grammar = self.opposite_polarity()
        super().fsmize()
        self.grammar = self.opposite_polarity()
