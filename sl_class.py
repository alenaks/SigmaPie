#!/bin/python3

"""
   A class of Strictly Local Grammars.
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

PosStL = TypeVar('PosStL', bound='PosSL')
NegStL = TypeVar('NegStL', bound='NegSL')

class PosSL(PosGram):
    """ A class for Positive Strictly Local grammars. """

    def __init__(self:PosG, alphabet:Union[None,list]=None, grammar:Union[None,List[tuple]]=None, k:int=2,
                 data:Union[list,None]=None, edges=[">", "<"]) -> None:
        """ Initialize basic attributes """
        super().__init__(alphabet, grammar, k, data, edges)
        self.fsm = None


    def learn(self:PosStL) -> None:
        """ Function for extracting positive SL grammar and alphabet
            from the given data.
        """

        if self.data:
            self.grammar = self.ngramize_data(self.k, self.data)


    def generate_sample(self:PosStL, n:int=10, rep:bool=True) -> None:
        """ Generates a sample of the data of a given size. """
        
        self.fsmize()
        self.extract_alphabet()

        data = [self.generate_item() for i in range(n)]
        self.data_sample = data

        if rep == False:
            self.data_sample = list(set(self.data_sample))
            while len(self.data_sample) < n:
                self.data_sample += [self.generate_item()]
                self.data_sample = list(set(self.data_sample))


    def scan(self:PosStL, string:str) -> bool:
        """ Scans a string and tells whether it can be generated
            by the grammar.
        """
        
        if not self.grammar:
            self.learn()

        string = self.annotate_data(string, self.k)
        if set(self.ngramize_item(string, self.k)).issubset(set(self.grammar)):
            return True
        else:
            return False


    def clean(self:PosStL) -> None:
        """ Function for removing useless n-grams from the grammar """

        self.fsmize()
        self.fsm.trim_fsm()
        self.grammar = self.build_ngrams(self.fsm.transitions)


    def change_polarity(self:PosStL) -> None:
        """ For a grammar with given polarity, returns set of ngrams
            of the opposite polarity.
        """

        if not self.alphabet:
            self.extract_alphabet()
        self.grammar = self.opposite_polarity(self.grammar, self.alphabet, self.k)
        self.__class__ = NegSL


    def generate_item(self:PosStL) -> str:
        """ Randomly generates a well-formed word """
        
        smap = self.state_map()
        if any([len(smap[x]) for x in smap]) == 0:
            raise(ValueError("The grammar is not provided properly."))

        word = self.edges[0]
        while word[-1] != self.edges[1]:
            word += choice(smap[word[-1]])

        return word


    def state_map(self:PosStL) -> dict:
        """ Generates a map of possible transitions in the
            given FSM.
        """
            
        smap:dict = {}
        smap[self.edges[0]] = [i[1] for i in self.fsm.transitions if i[0] == (self.edges[0],)]
        for symb in self.alphabet:
            smap[symb] = [i[1] for i in self.fsm.transitions if i[0] == (symb,)]

        return smap

        
    def fsmize(self:PosStL) -> None:
        """ Function that builds FSM corresponding to the grammar """
        
        if self.grammar:
            fin_state = FiniteStateMachine()
            fin_state.sl_states(self.grammar)
            self.fsm = fin_state
        else:
            raise(IndexError("The grammar is not provided."))


    def annotate_data(self:PosStL, data:str, k:int) -> str:
        return ">"*(k-1) + data.strip() + "<"*(k-1)
        

    def ngramize_data(self:PosStL, k:int, data:list) -> list:
        """ Creates set of k-grams based on the given data. """
        
        grammar:list = []
        for s in data:
            item = self.annotate_data(s, k)
            grammar += self.ngramize_item(item, k)

        return list(set(grammar))


    def ngramize_item(self:PosStL, item:str, k:int) -> list:
        """ N-gramizes a given string """

        ngrams:list = []
        for i in range(len(item)-(k-1)):
            ngrams += [tuple(item[i:i+k])]
                
        return list(set(ngrams))


    def build_ngrams(self:PosStL, transitions:list) -> list:
        """ Generates SL grammar based on the given transitions.
            For the transition ("ab", "c", "bc") gives ngram "abc".
        """
        
        if transitions == []:
            return transitions

        ngrams:list = []
        for i in transitions:
            ngrams.append(i[0] + (i[1],))

        return ngrams


class NegSL(PosSL):
    """ A class for Negative Strictly Local grammars. """

    def learn(self:NegStL) -> None:
        """ Function for extracting negative SL grammar and alphabet
            from the given data.
        """

        self.extract_alphabet()
        super().learn()
        self.grammar = self.opposite_polarity(self.grammar, self.alphabet, self.k)
       

    def clean(self:NegStL) -> None:
        """ Function for removing useless n-grams from the grammar """

        super().clean()
        self.grammar = self.opposite_polarity(self.grammar, self.alphabet, self.k)


    def fsmize(self:NegStL) -> None:
        """ Function that builds FSM corresponding to the grammar """

        self.extract_alphabet()
        self.grammar = self.opposite_polarity(self.grammar, self.alphabet, self.k)
        super().fsmize()
        self.grammar = self.opposite_polarity(self.grammar, self.alphabet, self.k)

        
    def change_polarity(self:NegStL) -> None:
        """ For a grammar with given polarity, returns set of ngrams
            of the opposite polarity.
        """

        self.extract_alphabet()
        self.grammar = self.opposite_polarity(self.grammar, self.alphabet, self.k)
        self.__class__ = PosSL
