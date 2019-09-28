#!/bin/python3

"""
   A module with the definition of the grammar class.
   Copyright (C) 2018  Alena Aksenova

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.
"""

import sys, os
#sys.path.insert(0, os.path.abspath('..'))

from itertools import product
from helper import *

class L(object):
    """
    A general class for grammars and languages. Contains methods that are
    applicable to all grammars in this package.

    Attributes:
        alphabet (list): alphabet used in the language;
        grammar (list): the list of substructures;
        k (int): locality window;
        data (list): input data;
        edges (list): start- and end-symbols for the grammar;
        polar ("p" or "n"): polarity of the grammar.

    Methods:
        extract_alphabet: extracts alphabet from data/grammar;
        well_formed_ngram: checks if ngram is well-formed;
        generate_all_ngrams: generates all possible well-formed ngrams
            based on the given alphabet;
        opposite_polarity: returns the opposite grammar;
        check_polarity: returns the polarity of the grammar;
        change_polarity: changes the polarity of the grammar to the one
            that is provided by the user.
    """

    def __init__(self, alphabet=None, grammar=None, k=2, data=None,
                 edges=[">", "<"], polar="p"):
        if polar not in ["p", "n"]:
            raise ValueError("The value of polarity should be either "
                            "positive ('p') or negative ('n').")
        self.__polarity = polar
        self.alphabet = alphabet
        self.grammar = [] if grammar == None else grammar
        self.k = k
        self.data = [] if data == None else data
        self.edges = edges


    def extract_alphabet(self):
        """
        Extracts alphabet from the given data or grammar and saves it
        into the 'alphabet' attribute.

        CAUTION: if not all symbols were used in the data or grammar,
                the result is not correct: update manually.
        """
        if self.alphabet == None:
            self.alphabet = []
        symbols = set(self.alphabet)
        if self.data:
            for item in self.data:
                symbols.update({j for j in item})
        if self.grammar:
            for item in self.grammar:
                symbols.update({j for j in item})
        symbols = symbols - set(self.edges)
        self.alphabet = sorted(list(symbols))


    def well_formed_ngram(self, ngram):
        """
        Tells whether the given ngram is well-formed.
        An ngram is ill-formed if:
        * there is something in-between two start- or end-symbols ('>a>'), or
        * something is before start symbol or after the end symbol ('a>'), or
        * the ngram consists only of start- or end-symbols.
        Otherwise it is well-formed.

        Arguments:
            ngram (str): The ngram that needs to be evaluated.

        Returns:
            bool: Tells whether the ngram is well-formed.
        """
        start, end = [], []
        for i in range(len(ngram)):
            if ngram[i] == self.edges[0]: start.append(i)
            elif ngram[i] == self.edges[1]: end.append(i)

        start_len, end_len = len(start), len(end)
        if any([start_len == len(ngram), end_len == len(ngram)]):
            return False

        if start_len > 0:
            if ngram[0] != self.edges[0]: return False
            if start_len > 1:
                for i in range(1,start_len):
                    if start[i] - start[i-1] != 1: return False

        if end_len > 0:
            if ngram[-1] != self.edges[1]: return False
            if end_len > 1:
                for i in range(1,end_len):
                    if end[i] - end[i-1] != 1: return False

        return True


    def generate_all_ngrams(self, symbols, k):
        """
        Generates all possible ngrams of the length k out of the given alphabet.

        Arguments:
            alphabet (list): alphabet, regular or tier;
            k (int): ngram's length.

        Returns:
            list: generated ngrams
        """
        symb = symbols[:]
        if (self.edges[0] not in symb) and (self.edges[1] not in symb):
            symb += self.edges

        combinations = product(symb, repeat=k)
        ngrams = []
        for ngram in combinations:
            if self.well_formed_ngram(ngram) and (ngram not in ngrams):
                ngrams.append(ngram)

        return ngrams


    def opposite_polarity(self, symbols):
        """
        Returns the grammar opposite to the one given.

        Arguments:
            symbols (list): alphabet, regular or tier.

        Returns:
            list: ngrams of the opposite polarity.
        """
        all_ngrams = self.generate_all_ngrams(symbols, self.k)
        opposite = [i for i in all_ngrams if i not in self.grammar]

        return opposite


    def check_polarity(self):
        """ Returns "p" or "n" showing the polarity of the grammar. """
        if self.__polarity == "p": return "p"
        else: return "n"


    def change_polarity(self, new_polarity=None):
        """
        Changes the polarity of the grammar.

        Arguments:
            new_polarity ("p" or "n"): the new value of the polarity.
        """
        if new_polarity != None:
            if new_polarity not in ["p", "n"]:
                raise ValueError("The value of polarity should be either "
                                "positive ('p') or negative ('n').")
            self.__polarity = new_polarity
        else:
            if self.__polarity == "p": self.__polarity = "n"
            elif self.__polarity == "n": self.__polarity = "p"
