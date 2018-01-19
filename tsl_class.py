#!/bin/python3

"""
   A class of Tier-based Strictly Local Grammars.
   Copyright (C) 2017  Alena Aksenova
   
   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.
"""

from typing import TypeVar, Generator, Union
from sl_class import *

PTSL = TypeVar('PTSL', bound='PosTSL')

class PosTSL(PosSL):
    """ A class for positive strictly local grammars.

    Attributes:
    -- alphabet: the list of symbols used in the given language;
    -- grammar: the list of grammatical rules;
    -- k: the locality measure;
    -- data: the language data given as input;
    -- data_sample: the generated data sample;
    -- fsm: the finite state machine that corresponds to the given grammar;
    -- tier: the list of tier symbols.
    """
    
    def __init__(self:PTSL, alphabet:Union[None,list]=None, grammar:Union[None,List[tuple]]=None, k:int=2,
                 data:Union[list,None]=None, edges=[">", "<"], tier:Union[None,list]=None) -> None:
        """ Initializes the PosTSL object. """
        
        super().__init__(alphabet, grammar, k, data, edges)
        self.tier = tier


    def learn_tier(self:PTSL) -> None:
        """
        This function determines which of the symbols used in the language
        are tier symbols. The learner is taken from Jardine & McMullin (2016).

        Arguments:
        -- self.

        Results:
        -- self.tier contains the list of the tier symbols.
        """
        
        self.extract_alphabet()
        self.tier = self.alphabet[:]

        if self.tier:
            ngrams = self.ngramize_data(self.k, self.data)
            ngrams_less = self.ngramize_data(self.k-1, self.data)
            ngrams_more = self.ngramize_data(self.k+1, self.data)

            for symbol in self.tier:
                if self.test_insert(symbol, ngrams, ngrams_less) and \
                   self.test_remove(symbol, ngrams, ngrams_more):
                    self.tier.remove(symbol)
                   


    def test_insert(self:PTSL, symbol:str, ngrams:list, ngrams_less:list) -> bool:
        """
        Tier presense test #1. For every (n-1)-gram of the type 'xy',
        there must be an n-gram of the type 'xSy'.

        Arguments:
        -- self;
        -- symbol: the symbol that is currently being tested;
        -- ngrams: the list of ngrams;
        -- ngrams_less: the list of (n-1)-grams.

        Returns:
        -- a boolean value depending on whether the symbol passed
           the test or not.
        """

        extension = []
        for small in ngrams_less:
            for i in range(len(small)):
                new = small[:i] + (symbol,) + small[i:]
                if self.good_ngram(new):
                    extension.append(new)
                    
        if set(extension).issubset(set(ngrams)):
            return True
        else:
            return False


    def test_remove(self:PTSL, symbol:str, ngrams:list, ngrams_more:list) -> bool:
        """
        Tier presense test #2. For every (n+1)-gram of the type 'xSy',
        there must be an n-gram of the type 'xy'.

        Arguments:
        -- self;
        -- symbol: the symbol that is currently being tested;
        -- ngrams: the list of ngrams;
        -- ngrams_more: the list of (n+1)-grams.

        Returns:
        -- a boolean value depending on whether the symbol passed
           the test or not.
        """
        
        extension = []
        for big in ngrams_more:
            if symbol in big:
                for i in range(len(big)):
                    if big[i] == symbol:
                        new = big[:i] + big[i+1:]
                        if self.good_ngram(new):
                            extension.append(new)

        if set(extension).issubset(set(ngrams)):
            return True
        else:
            return False
                
