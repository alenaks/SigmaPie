"""A module with the definition of the grammar class. Copyright (C) 2019  Alena
Aksenova.

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 3 of the License, or (at your
option) any later version.
"""

from itertools import product
from sigmapie.helper import *


class L(object):
    """A general class for grammars and languages.

    Implements methods that
    are applicable to all grammars in this package.
    Attributes:
        alphabet (list): alphabet used in the language;
        grammar (list): the list of substructures;
        k (int): locality window;
        data (list): input data;
        edges (list): start- and end-symbols for the grammar;
        polar ("p" or "n"): polarity of the grammar.
    """

    def __init__(
        self, alphabet=None, grammar=None, k=2, data=None, edges=[">", "<"], polar="p"
    ):
        """Initializes the L object."""
        if polar not in ["p", "n"]:
            raise ValueError(
                "The value of polarity should be either "
                "positive ('p') or negative ('n')."
            )
        self.__polarity = polar
        self.alphabet = alphabet
        self.grammar = [] if grammar is None else grammar
        self.k = k
        self.data = [] if data is None else data
        self.edges = edges

    def extract_alphabet(self):
        """Extracts alphabet from the given data or grammar and saves it into
        the 'alphabet' attribute.

        CAUTION: if not all symbols were used in the data or grammar,
                the result is not correct: update manually.
        """
        if self.alphabet is None:
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
        """Tells if the given ngram is well-formed. An ngram is ill-formed if:

        * there is something in-between two start- or end-symbols
          ('>a>'), or
        * something is before start symbol or after the end symbol
          ('a>'), or
        * the ngram consists only of start- or end-symbols.
        Otherwise it is well-formed.
        Arguments:
            ngram (str): The ngram that needs to be evaluated.
        Returns:
            bool: well-formedness of the ngram.
        """
        start, end = [], []
        for i in range(len(ngram)):
            if ngram[i] == self.edges[0]:
                start.append(i)
            elif ngram[i] == self.edges[1]:
                end.append(i)

        start_len, end_len = len(start), len(end)
        if any([start_len == len(ngram), end_len == len(ngram)]):
            return False

        if start_len > 0:
            if ngram[0] != self.edges[0]:
                return False
            if start_len > 1:
                for i in range(1, start_len):
                    if start[i] - start[i - 1] != 1:
                        return False

        if end_len > 0:
            if ngram[-1] != self.edges[1]:
                return False
            if end_len > 1:
                for i in range(1, end_len):
                    if end[i] - end[i - 1] != 1:
                        return False

        return True

    def generate_all_ngrams(self, symbols, k):
        """Generates all possible ngrams of the length k based on the given
        alphabet.

        Arguments:
            alphabet (list): alphabet;
            k (int): locality window (length of ngram).
        Returns:
            list: generated ngrams.
        """
        symb = symbols[:]
        if not ((self.edges[0] in symb) or (self.edges[1] in symb)):
            symb += self.edges

        combinations = product(symb, repeat=k)
        ngrams = []
        for ngram in combinations:
            if self.well_formed_ngram(ngram) and (ngram not in ngrams):
                ngrams.append(ngram)

        return ngrams

    def opposite_polarity(self, symbols):
        """Returns the grammar opposite to the one given.

        Arguments:
            symbols (list): alphabet.
        Returns:
            list: ngrams of the opposite polarity.
        """
        all_ngrams = self.generate_all_ngrams(symbols, self.k)
        opposite = [i for i in all_ngrams if i not in self.grammar]

        return opposite

    def check_polarity(self):
        """Returns the polarity of the grammar ("p" or "n")."""
        if self.__polarity == "p":
            return "p"
        return "n"

    def change_polarity(self, new_polarity=None):
        """Changes the polarity of the grammar.

        Warning: it does not rewrite the grammar!
        """
        if new_polarity is not None:
            if new_polarity not in ["p", "n"]:
                raise ValueError(
                    "The value of polarity should be either "
                    "positive ('p') or negative ('n')."
                )
            self.__polarity = new_polarity
        else:
            if self.__polarity == "p":
                self.__polarity = "n"
            elif self.__polarity == "n":
                self.__polarity = "p"
