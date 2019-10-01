#!/bin/python3

"""
   A module with the unittests for the SL module.
   Copyright (C) 2019  Alena Aksenova

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.abspath('..'), 'code'))

import unittest
from sl_class import *


class TestSLLanguages(unittest.TestCase):
    """ Tests for the SL class. """

    def test_scan_pos(self):
        """ Checks if well-formed strings are detected
            correctly given the provided positive grammar.
        """
        slp = SL()
        slp.grammar = [(">", "a"), ("b", "a"), ("a", "b"), ("b", "<")]
        slp.alphabet = ["a", "b"]
        self.assertTrue(slp.scan("abab"))
        self.assertTrue(slp.scan("ab"))
        self.assertTrue(slp.scan("ababababab"))
        self.assertFalse(slp.scan("abb"))
        self.assertFalse(slp.scan("a"))
        self.assertFalse(slp.scan(""))


    def test_scan_neg(self):
        """ Checks if well-formed strings are detected
            correctly given the provided negative grammar.
        """
        sln = SL(polar="n")
        sln.grammar = [("b", "a"), ("a", "b")]
        sln.alphabet = ["a", "b"]
        self.assertFalse(sln.scan("abab"))
        self.assertFalse(sln.scan("ab"))
        self.assertFalse(sln.scan("ababababab"))
        self.assertTrue(sln.scan("bbbb"))
        self.assertTrue(sln.scan("aaaaa"))
        self.assertTrue(sln.scan(""))


    def test_ngramize_2(self):
        """ Checks if ngramize() correctly constructs bigrams. """
        sl = SL()
        sl.data = ["aaa", "bbb"]
        ngrams = set(sl.ngramize_data())
        goal = {('>', 'b'), ('>', 'a'), ('a', 'a'), ('b', 'b'),
                ('a', '<'), ('b', '<')}
        self.assertTrue(ngrams == goal)


    def test_ngramize_3(self):
        """ Check if ngramize() correctly constructs trigrams. """
        sl = SL()
        sl.k = 3
        sl.data = ["aaa", "bbb"]
        ngrams = set(sl.ngramize_data())
        goal = {('>', 'a', 'a'), ('>', 'b', 'b'), ('b', 'b', '<'),
                ('b', '<', '<'), ('a', '<', '<'), ('>', '>', 'a'),
                ('a', 'a', 'a'), ('a', 'a', '<'), ('>', '>', 'b'),
                ('b', 'b', 'b')}
        self.assertTrue(ngrams == goal)
        

    def test_learn(self):
        """ Checks if positive and negative grammars are
            learned correctly.
        """
        data = ["abab", "ababab"]
        gpos = {(">", "a"), ("b", "a"), ("a", "b"), ("b", "<")}
        gneg = {(">", "<"), ("a", "<"), (">", "b"), ("b", "b"), ("a", "a")}

        a = SL(data=data, alphabet=["a", "b"])
        a.learn()
        self.assertTrue(set(a.grammar) == gpos)

        a.change_polarity()
        a.learn()
        self.assertTrue(set(a.grammar) == gneg)


    def test_fsmize_pos(self):
        """ Checks if the transitions of the fsm corresponding to the
            positive grammar are constructed correctly.
        """
        sl = SL(polar="p")
        sl.alphabet = ["a", "b"]
        sl.grammar = [(">", "a"), ("b", "a"), ("a", "b"), ("b", "<")]
        sl.fsmize()

        f = FSM(initial=">", final="<")
        f.sl_to_fsm([(">", "a"), ("b", "a"), ("a", "b"), ("b", "<")])

        self.assertTrue(set(sl.fsm.transitions) == set(f.transitions))

        
    def test_fsmize_neg(self):
        """ Checks if the transitions of the fsm corresponding to the
            negative grammar are constructed correctly.
        """
        sl = SL()
        sl.change_polarity("n")
        sl.alphabet = ["a", "b"]
        sl.grammar = [(">", "<"), ("a", "<"), (">", "b"), ("b", "b"),
                      ("a", "a")]
        sl.fsmize()

        f = FSM(initial=">", final="<")
        f.sl_to_fsm([(">", "a"), ("b", "a"), ("a", "b"), ("b", "<")])

        self.assertTrue(set(sl.fsm.transitions) == set(f.transitions))


    def test_generate_sample(self):
        """ Checks if all generated data points are actually
            well-formed with respect to the given grammar,
            and that the number of generated data points is
            correct.
        """
        sl = SL()
        sl.alphabet = ["a", "b"]
        sl.grammar = [(">", "a"), ("b", "a"), ("a", "b"), ("b", "<")]
        sl.fsmize()

        sample = sl.generate_sample(n=10)
        self.assertTrue(all([sl.scan(i) for i in sample]))
        self.assertTrue(len(sample) == 10)


    def test_switch_polarity(self):
        """ Makes sure that switch_polarity actually switches
            the grammar to the opposite, and that switching it
            again will result in the original grammar.
        """
        gpos = {(">", "a"), ("b", "a"), ("a", "b"), ("b", "<")}
        gneg = {(">", "<"), ("a", "<"), (">", "b"), ("b", "b"), ("a", "a")}
        sl = SL(polar="n")
        sl.alphabet = ["a", "b"]
        sl.grammar = list(gneg)
        
        sl.switch_polarity()
        self.assertTrue(set(sl.grammar) == gpos)
        self.assertTrue(sl.check_polarity() == "p")

        sl.switch_polarity()
        self.assertTrue(set(sl.grammar) == gneg)
        self.assertTrue(sl.check_polarity() == "n")


    def test_clean_grammar_2_pos(self):
        """ Tests if clean_grammar correctly cleans 2-local positive
            SL grammar.
        """
        goal = {(">", "a"), ("b", "a"), ("a", "b"), ("b", "<")}
        s = SL()
        s.grammar = [(">", "a"), ("b", "a"), ("a", "b"), ("b", "<"),
                     (">", "g"), ("f", "<"), ("t", "t")]
        s.extract_alphabet()
        s.clean_grammar()
        self.assertTrue(set(s.grammar) == goal)


    def test_clean_grammar_2_neg(self):
        """ Tests if clean_grammar correctly cleans 2-local negative
            SL grammar.
        """
        goal = {(">", "<"), ("a", "<"), (">", "b"), ("b", "b"), ("a", "a")}
        a = SL(polar="n")
        a.alphabet = ["a", "b"]
        a.grammar = [(">", "<"), ("a", "<"), (">", "b"), ("b", "b"),
                     ("a", "a"), (">", "<"), ("b", "b")]
        a.clean_grammar()
        self.assertTrue(set(a.grammar) == goal)


    def test_clean_grammar_3_pos(self):
        """ Tests if clean_grammar correctly cleans 2-local positive
            SL grammar.
        """
        goal = {('>', 'a', 'a'), ('>', 'b', 'b'), ('b', 'b', '<'),
                ('b', '<', '<'), ('a', '<', '<'), ('>', '>', 'a'),
                ('a', 'a', 'a'), ('a', 'a', '<'), ('>', '>', 'b'),
                ('b', 'b', 'b')}
        s = SL()
        s.grammar = [('>', 'a', 'a'), ('>', 'b', 'b'), ('b', 'b', '<'),
                     ('b', '<', '<'), ('a', '<', '<'), ('>', '>', 'a'),
                     ('a', 'a', 'a'), ('a', 'a', '<'), ('>', '>', 'b'),
                     ('b', 'b', 'b'), ('>', '>', 'f'), ('b', 'd', 'c')]
        s.extract_alphabet()
        s.clean_grammar()
        self.assertTrue(set(s.grammar) == goal)


if __name__ == '__main__':
    unittest.main()
    
