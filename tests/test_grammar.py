#!/bin/python3

"""
   A module with the unittests for the grammar module.
   Copyright (C) 2019  Alena Aksenova

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.abspath('..'), 'code'))

import unittest
from grammar import L


class TestGeneralLanguages(unittest.TestCase):
    """ Tests for the L class. """

    def test_good_ngram_standard_edges(self):
        """ Checks if ill-formed ngrams are correctly recognized, and
            that the well-formed ones are not blocked. Tests standard
            edge-markers.
        """
        l = L()
        self.assertTrue(l.well_formed_ngram(("a", "b", "a")))
        self.assertTrue(l.well_formed_ngram((">", "a", "b")))
        self.assertTrue(l.well_formed_ngram((">", "a", "<")))
        self.assertTrue(l.well_formed_ngram((">", "<")))
        self.assertTrue(l.well_formed_ngram(("b", "<")))
        self.assertTrue(l.well_formed_ngram(("a", "a", "a", "a", "a")))
        
        self.assertFalse(l.well_formed_ngram(("a", ">")))
        self.assertFalse(l.well_formed_ngram(("?", "d", "<", ">")))
        self.assertFalse(l.well_formed_ngram(("a", ">", "a")))
        self.assertFalse(l.well_formed_ngram((">", ">")))
        self.assertFalse(l.well_formed_ngram(("<")))


    def test_good_ngram_non_standard_edges(self):
        """ Checks if ill-formed ngrams are correctly recognized, and
            that the well-formed ones are not blocked. Tests user-provided
            edge markers.
        """
        l = L()
        l.edges=["$", "#"]
        self.assertTrue(l.well_formed_ngram(("$", "a", "b")))
        self.assertTrue(l.well_formed_ngram(("$", "a", "#")))
        self.assertTrue(l.well_formed_ngram(("$", "#")))
        self.assertTrue(l.well_formed_ngram(("b", "#")))
        
        self.assertFalse(l.well_formed_ngram(("a", "$")))
        self.assertFalse(l.well_formed_ngram(("$", "d", "#", "$")))
        self.assertFalse(l.well_formed_ngram(("a", "$", "a")))
        self.assertFalse(l.well_formed_ngram(("$", "$")))
        self.assertFalse(l.well_formed_ngram(("#")))
        

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


    def test_change_polarity(self):
        """ Tests the correctness of change_polarity. """
        a = L(polar="n")
        a.change_polarity(new_polarity="n")
        self.assertTrue(a.check_polarity() == "n")
        a.change_polarity()
        self.assertFalse(a.check_polarity() == "n")

        b = L()
        old_polarity = b.check_polarity()
        b.change_polarity()
        self.assertTrue(b.check_polarity() != old_polarity)
        
        


if __name__ == '__main__':
    unittest.main()