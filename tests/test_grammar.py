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
sys.path.insert(0, os.path.abspath('..'))

import unittest
from PyKleene.grammar import L


class TestGeneralLanguages(unittest.TestCase):
    """ Tests for the L class. """

    def test_good_ngram_standard_edges(self):
        """ Checks if ill-formed ngrams are correctly recognized, and
            that the well-formed ones are not blocked. Tests standard
            edge-markers.
        """
        l = L()
        self.assertTrue(l.well_formed_ngram("aba"))
        self.assertTrue(l.well_formed_ngram(">ab"))
        self.assertTrue(l.well_formed_ngram(">a<"))
        self.assertTrue(l.well_formed_ngram("><"))
        self.assertTrue(l.well_formed_ngram("b<"))
        self.assertTrue(l.well_formed_ngram("aaaaa"))
        
        self.assertFalse(l.well_formed_ngram("a>"))
        self.assertFalse(l.well_formed_ngram(">d<>"))
        self.assertFalse(l.well_formed_ngram("a>a"))
        self.assertFalse(l.well_formed_ngram(">>"))
        self.assertFalse(l.well_formed_ngram("<"))


    def test_good_ngram_non_standard_edges(self):
        """ Checks if ill-formed ngrams are correctly recognized, and
            that the well-formed ones are not blocked. Tests user-provided
            edge markers.
        """
        l = L()
        l.edges=["$", "#"]
        self.assertTrue(l.well_formed_ngram("$ab"))
        self.assertTrue(l.well_formed_ngram("$a#"))
        self.assertTrue(l.well_formed_ngram("$#"))
        self.assertTrue(l.well_formed_ngram("b#"))
        
        self.assertFalse(l.well_formed_ngram("a$"))
        self.assertFalse(l.well_formed_ngram("$d#$"))
        self.assertFalse(l.well_formed_ngram("a$a"))
        self.assertFalse(l.well_formed_ngram("$$"))
        self.assertFalse(l.well_formed_ngram("#"))
        

    def test_ngram_gen(self):
        """ Checks if ngram generation method produces the expected
            results.
        """
        l = L(alphabet=["a", "b"])
        ngrams = l.generate_all_ngrams(l.alphabet, l.k)

        ng = {(">", "<"), (">", "a"), ("a", "<"), (">", "b"), ("b", "<"),
              ("a", "a"), ("b", "b"), ("b", "a"), ("a", "b")}
        self.assertTrue(set(ngrams) == ng)


    def test_switch_same_alpha(self):
        """ Checks if the generated grammar is correct when all alphabet
            symbols are used in the grammar, also checks that polarity
            was changed.
        """
        g = [(">", "a"), ("b", "<"), ("a", "b"), ("b", "a")]
        l = L(grammar=g)
        l.extract_alphabet()

        old_polarity = l.check_polarity()

        g_opp = {(">", "<"), ("a", "<"), (">", "b"), ("b", "b"), ("a", "a")}
        self.assertTrue(set(l.opposite_polarity(l.alphabet)) == g_opp)
        self.assertFalse(old_polarity == l.check_polarity)


    def test_switch_different_alpha(self):
        """ Checks if the generated grammar is correct when not all
            alphabet symbols are used in the grammar; also checks
            that polarity was changed.
        """
        g = [(">", "b"), ("b", "<"), (">", "<")]
        l = L(grammar=g)
        l.alphabet = ["a", "b"]

        old_polarity = l.check_polarity()

        g_opp = {(">", "a"), ("a", "<"), ("a", "a"), ("b", "a"),
                 ("a", "b"), ("b", "b")}
        self.assertTrue(set(l.opposite_polarity(l.alphabet)) == g_opp)
        self.assertFalse(old_polarity == l.check_polarity)


if __name__ == '__main__':
    unittest.main()
    
##
##class L(object):
##    """
##    A general class for grammars and languages. Contains methods that are applicable
##    to all grammars in this package.
##
##    Attributes:
##        polar ("p" or "n"): polarity of the grammar;
##        alphabet (list): alphabet used in the language;
##        grammar (list): the list of substructures;
##        k (int): locality window;
##        data (list): input data.
##    """
##
##    def __init__(self, alphabet=None, grammar=None, k=2, data=None,
##                 edges=[">", "<"], polar="p"):
##        if polar not in ["p", "n"]:
##            raise ValueError("The value of polarity should be either "
##                            "positive ('p') or negative ('n').")
##        self.__polarity = polar
##        self.alphabet = alphabet
##        self.grammar = [] if grammar == None else grammar
##        self.k = k
##        self.data = [] if data == None else data
##        self.edges = edges
##
##
##    def extract_alphabet(self):
##        """
##        Extracts alphabet from the given data or grammar and saves it
##        into the 'alphabet' attribute.
##
##        CAUTION: if not all symbols were used in the data or grammar,
##                the result is not correct: update manually.
##        """
##
##        if self.alphabet == None:
##            self.alphabet = []
##        symbols = set(self.alphabet)
##        if self.data:
##            for item in self.data:
##                symbols.update({j for j in item})
##        if self.grammar:
##            for item in self.grammar:
##                symbols.update({j for j in item})
##        symbols = symbols - set(self.edges)
##        self.alphabet = sorted(list(symbols))
##
##
##    def well_formed_ngram(self, ngram):
##        """
##        Tells whether the given ngram is well-formed.
##        An ngram is ill-formed if:
##        * there is something in-between two start- or end-symbols ('>a>'), or
##        * something is before start symbol or after the end symbol ('a>'), or
##        * the ngram consists only of start- or end-symbols.
##        Otherwise it is well-formed.
##
##        Arguments:
##            ngram (str): The ngram that needs to be evaluated.
##
##        Returns:
##            bool: Tells whether the ngram is well-formed.
##        """
##
##        start, end = [], []
##        for i in range(len(ngram)):
##            if ngram[i] == self.edges[0]: start.append(i)
##            elif ngram[i] == self.edges[1]: end.append(i)
##
##        start_len, end_len = len(start), len(end)
##        if any([start_len == len(ngram), end_len == len(ngram)]):
##            return False
##
##        if start_len > 0:
##            if ngram[0] != self.edges[0]: return False
##            if start_len > 1:
##                for i in range(1,start_len):
##                    if start[i] - start[i-1] != 1: return False
##
##        if end_len > 0:
##            if ngram[-1] != self.edges[1]: return False
##            if end_len > 1:
##                for i in range(1,end_len):
##                    if end[i] - end[i-1] != 1: return False
##
##        return True
##
##
##    def generate_all_ngrams(self, symbols, k):
##        """
##        Generates all possible ngrams of the length k out of the given alphabet.
##
##        Arguments:
##            alphabet (list): alphabet, regular or tier;
##            k (int): ngram's length.
##
##        Returns:
##            list: generated ngrams
##        """
##
##        symb = symbols[:]
##        if (self.edges[0] not in symb) and (self.edges[1] not in symb):
##            symb += self.edges
##
##        combinations = product(symb, repeat=k)
##        ngrams = []
##        for ngram in combinations:
##            if self.well_formed_ngram(ngram) and (ngram not in ngrams):
##                ngrams.append(ngram)
##
##        return ngrams
##
