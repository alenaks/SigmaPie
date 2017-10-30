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
from local_helper import *
from fsm import *

SL = TypeVar('SL', bound='PosSL')

class PosSL(object):
    """ A class for Positive Strictly Local grammars. """

    def __init__(self:SL, grammar:list=[], k:int=2, data:list=[]) -> None:
        """ Initialize basic attributes """
        
        self.grammar = grammar
        self.k = k
        self.data = data
        self.alphabet:list = []


    def learn(self:SL) -> None:
        """ Function for extracting positive SL grammar and alphabet
            from the given data.
        """

        if self.data:
            self.alphabet = alphabetize(self.data)
        else:
            raise IndexError("Language is not provided or empty -- "
                             "no grammar can be generated.")
        
        self.grammar = self._ngramize_data(self.k, self.data)


    def clean(self:SL) -> None:
        """ Function for removing useless n-grams from the grammar """

        fin_state = FiniteStateMachine()
        fin_state.sl_states(self.grammar)
        fin_state.trim_fsm()
        self.grammar = self.__build_ngrams(fin_state.transitions)
        

    def _ngramize_data(self:SL, k:int, data:list) -> list:
        """ Creates set of k-grams based on the given data. """
        
        grammar:list = []
        for s in data:
            item = annotate_data(s, k)
            grammar += self.__ngramize_item(item, k)

        return list(set(grammar))


    def __ngramize_item(self:SL, item:str, k:int) -> list:
        """ N-gramizes a given string """

        ngrams:list = []
        for i in range(len(item)-(k-1)):
            ngrams += [tuple(item[i:i+k])]
                
        return list(set(ngrams))


    def __build_ngrams(self:SL, transitions:list) -> list:
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

    def __init__(self:SL, grammar:list=[], k:int=2, data:list=[]) -> None:
        super().__init__(grammar, k, data)
        self.alphabet:list = []

    def learn(self:SL) -> None:
        """ Function for extracting negative SL grammar and alphabet
            from the given data.
        """
        super().learn()
        self.grammar = change_polarity(self.grammar, self.alphabet, self.k)


    def clean(self:SL) -> None:
        """ Function for removing useless n-grams from the grammar """

        self.grammar = change_polarity(self.grammar, self.alphabet, self.k)
        super().clean()
        self.grammar = change_polarity(self.grammar, self.alphabet, self.k)
        
