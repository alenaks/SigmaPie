#!/bin/python3

"""
   A class of Strictly Local Grammars.
   Copyright (C) 2017  Alena Aksenova
   
   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.
"""

from typing import TypeVar, Union, Tuple
from helper import *
from fsm import *
from grammar import *

PosStL = TypeVar('PosStL', bound='PosSL')
NegStL = TypeVar('NegStL', bound='NegSL')

class PosSL(PosGram):
    """ A class for Positive Strictly Local grammars. """

    def __init__(self:PosStL, grammar:list=[], k:int=2, data:list=[], alphabet:list=[]) -> None:
        """ Initialize basic attributes """
        super().__init__(grammar, k, data, alphabet)


    def learn(self:PosStL) -> None:
        """ Function for extracting positive SL grammar and alphabet
            from the given data.
        """

        if self.data:
            self.alphabet = alphabetize(self.data)
        else:
            raise IndexError("Language is not provided or empty -- "
                             "no grammar can be generated.")
        
        self.grammar = self._ngramize_data(self.k, self.data)


    def clean(self:PosStL) -> None:
        """ Function for removing useless n-grams from the grammar """

        fin_state = FiniteStateMachine()
        fin_state.sl_states(self.grammar)
        fin_state.trim_fsm()
        self.grammar = self.__build_ngrams(fin_state.transitions)


    def annotate_data(self:PosStL, data:str, k:int) -> str:
        return ">"*(k-1) + data.strip() + "<"*(k-1)
        

    def _ngramize_data(self:PosStL, k:int, data:list) -> list:
        """ Creates set of k-grams based on the given data. """
        
        grammar:list = []
        for s in data:
            item = self.annotate_data(s, k)
            grammar += self.__ngramize_item(item, k)

        return list(set(grammar))


    def __ngramize_item(self:PosStL, item:str, k:int) -> list:
        """ N-gramizes a given string """

        ngrams:list = []
        for i in range(len(item)-(k-1)):
            ngrams += [tuple(item[i:i+k])]
                
        return list(set(ngrams))


    def __build_ngrams(self:PosStL, transitions:list) -> list:
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

    def __init__(self:NegStL, grammar:list=[], k:int=2, data:list=[], alphabet:list=[]) -> None:
        super().__init__(grammar, k, data, alphabet)


    def learn(self:NegStL) -> None:
        """ Function for extracting negative SL grammar and alphabet
            from the given data.
        """
        super().learn()
        self.grammar = self.change_polarity(self.grammar, self.alphabet, self.k)


    def clean(self:NegStL) -> None:
        """ Function for removing useless n-grams from the grammar """

        self.grammar = self.change_polarity(self.grammar, self.alphabet, self.k)
        super().clean()
        self.grammar = self.change_polarity(self.grammar, self.alphabet, self.k)
        
