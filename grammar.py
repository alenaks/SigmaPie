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
    """ A general class for positive grammars. Contains methods that are applicable
        to (positive) grammars in general.
    """

    def __init__(self:PosG, grammar:Union[None,List[tuple]]=None, k:int=2,
                 data:Union[list,None]=None, edges=[">", "<"]) -> None:
        self.grammar = [] if grammar == None else grammar
        self.k = k
        self.data = [] if data == None else data
        self.edges = edges
        self.data_sample:list = []

    @property
    def alphabet(self):
        return alphabetize(self.data)

    @alphabet.setter
    def alphabet(self, value):
        self.alphabet = value

    def change_polarity(self:PosG) -> None:
        """ For a grammar with given polarity, returns set of ngrams
            of the opposite polarity.
        """
        self.grammar = self.opposite_polarity(self.grammar, self.alphabet, self.k)
        self.__class__ = NegGram


    def opposite_polarity(self:PosG, ngrams:list, alphabet:list, k:int) -> list:
        """ Returns set of ngrams of the opposite polarity. """

        combinations = set(self.generate_all_ngrams(alphabet, k))
        return list(combinations.difference(set(ngrams)))


    def generate_all_ngrams(self:PosG, alphabet:list, k:int) -> list:
        """ Generate possible ngrams of a given length based on
            the given alphabet.
        """

        local_alphabet = alphabet[:]
        if (">" not in local_alphabet) and ("<" not in local_alphabet):
            local_alphabet += [">", "<"]
        combinations = product(local_alphabet, repeat=k)
        ngrams = set([i for i in combinations if self.good_ngram(i)])
        return list(ngrams)


    def good_ngram(self:PosG, ngram:tuple) -> bool:
        """ Auxiliary function for the ngram generator. Returns True
            iff the ngram is ill-formed, and False otherwise: if there is
            somthing in-between two start- or two end-symbols ('>a>'),
            something is before start symbol or after end symbol ('a>'), or
            if the ngram consists only of start- or only of end-symbols.
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
    """ A general class for negative grammars. Contains methods that are applicable
        to negative grammars in general.
    """

    def __init__(self:NegG, alphabet:list=[], grammar:List[tuple]=[], k:int=2, data:list=[]) -> None:
        super().__init__(alphabet, grammar, k, data)


    def change_polarity(self:NegG) -> None:
        """ For a grammar with given polarity, returns set of ngrams
            of the opposite polarity, and changes the class of the grammar.
        """
        self.grammar = self.opposite_polarity(self.grammar, self.alphabet, self.k)
        self.__class__ = PosGram
