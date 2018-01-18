#!/bin/python3

"""
   A module with the definition of the grammar class.
   Copyright (C) 2017  Alena Aksenova
   
   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.
"""

from typing import TypeVar, List, Union
from itertools import product
from helper import *

PosG = TypeVar('PosG', bound='PosGram')
NegG = TypeVar('NegG', bound='NegGram')


class PosGram(object):
    """
    A general class for positive grammars. Contains methods that are applicable
    to all grammars in this package.

    Attributes:
    -- alphabet: the list of symbols used in the given language;
    -- grammar: the list of grammatical rules;
    -- k: the locality measure;
    -- data: the language data given as input;
    -- data_sample: the generated data sample.
    """

    def __init__(self:PosG, alphabet:Union[None,list]=None, grammar:Union[None,List[tuple]]=None, k:int=2,
                 data:Union[list,None]=None, edges=[">", "<"]) -> None:
        """ Initializes the PosGram object. """
        
        self.alphabet = [] if alphabet == None else alphabet
        self.grammar = [] if grammar == None else grammar
        self.k = k
        self.data = [] if data == None else data
        self.edges = edges
        self.data_sample:list = []

    
    def change_polarity(self:PosG) -> None:
        """
        Changes polarity of the grammar.

        Arguments:
        -- self.

        Results:
        -- self.grammar is being switched to the opposite;
        -- self.__class__ is changed to 'NegGram'.
        """
        
        self.grammar = self.opposite_polarity(self.grammar, self.alphabet, self.k)
        self.__class__ = NegGram


    def extract_alphabet(self:PosG) -> None:
        """
        Extracts alphabet from the given data/grammar.

        Arguments:
        -- self.

        Results:
        -- self.alphabet contains symbols that are used in the data.
        """
        
        symbols = set(self.alphabet)
        if self.data:
            for item in self.data:
                symbols.update({j for j in item})
        if self.grammar:
            for item in self.grammar:
                symbols.update({j for j in item})
        symbols = symbols - set(self.edges)
        self.alphabet = sorted(list(symbols))
        

    def opposite_polarity(self:PosG, ngrams:list, alphabet:list, k:int) -> list:
        """
        For a grammar with given polarity, returns set of ngrams
        of the opposite polarity.

        Arguments:
        -- self;
        -- ngrams: list of ngrams;
        -- alphabet: list of symbold used in the given grammar;
        -- k: the locality window.

        Returns:
        -- a list of ngrams opposite to the ones given as input.
        """

        combinations = set(self.generate_all_ngrams(alphabet, k))
        return list(combinations.difference(set(ngrams)))


    def generate_all_ngrams(self:PosG, alphabet:list, k:int) -> list:
        """
        Generate possible ngrams of a given length based on
        the given alphabet.

        Arguments:
        -- self;
        -- alphabet: list of symbols used in the given grammar;
        -- k: the locality window.

        Returns:
        -- list of all possible ngrams of the length k that can
           be generated basen of the given alphabet.
        """

        local_alphabet = alphabet[:]
        if (">" not in local_alphabet) and ("<" not in local_alphabet):
            local_alphabet += [">", "<"]
        combinations = product(local_alphabet, repeat=k)
        ngrams = set([i for i in combinations if self.good_ngram(i)])
        return list(ngrams)


    def good_ngram(self:PosG, ngram:tuple) -> bool:
        """
        Auxiliary function for the ngram generator. Returns True
        iff the ngram is ill-formed, and False otherwise.

        An ngram is ill-formed if:
        * there is somthing in-between two start- or end-symbols ('>a>'), or
        * something is before start symbol or after end symbol ('a>'), or
        * the ngram consists only of start- or only of end-symbols.

        Arguments:
        -- self;
        -- ngram: an ngram that needs to be evaluated.

        Returns:
        -- a boolean value depending on the well-formedness of the ngram.
        """

        start = [i for i in range(len(ngram)) if ngram[i] == ">"]
        if len(start) > 0:
            s_inter = [i for i in range(start[0], start[-1]) if i not in start]
            if len(s_inter) > 0 or start[0] != 0 or len(start) == len(ngram):
                return False

        end = [i for i in range(len(ngram)) if ngram[i] == "<"]
        if len(end) > 0:
            e_inter = [i for i in range(end[0], end[-1]) if i not in end]
            if len(e_inter) > 0 or end[-1] != (len(ngram)-1) or len(end) == len(ngram):
                return False

        return True


        
class NegGram(PosGram):
    """
    A general class for positive grammars. Contains methods that are applicable
    to all grammars in this package.

    Attributes:
    -- alphabet: the list of symbols used in the given language;
    -- grammar: the list of grammatical rules;
    -- k: the locality measure;
    -- data: the language data given as input;
    -- data_sample: the generated data sample.
    """

    def change_polarity(self:NegG) -> None:
        """
        Version of the function for negative grammar.

        Arguments:
        -- self.

        Results:
        -- self.grammar is being switched to the opposite;
        -- self.__class__ is changed to 'PosGram'.
        """
        
        self.grammar = self.opposite_polarity(self.grammar, self.alphabet, self.k)
        self.__class__ = PosGram
