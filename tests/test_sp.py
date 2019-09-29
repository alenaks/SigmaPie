#!/bin/python3

"""
   A module with the unittests for the SP module.
   Copyright (C) 2019  Alena Aksenova

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.abspath('..'), 'code'))

import unittest
from sp_class import *


class TestSPLanguages(unittest.TestCase):
    """ Tests for the SP class. """

    def test_subsequences_2(self):
        """ Tests extraction of 2-subsequences """
        str1 = "abab"
        ssq1 = {("a", "a"), ("a", "b"), ("b", "a"), ("b", "b")}
        str2 = "a"
        ssq2 = set()
        str3 = "abcde"
        ssq3 = {tuple(i) for i in ["ab", "ac", "ad", "ae", "bc", "bd",
                                   "be", "cd", "ce", "de"]}
        sp = SP()
        self.assertTrue(set(sp.subsequences(str1)) == ssq1)
        self.assertTrue(set(sp.subsequences(str2)) == ssq2)
        self.assertTrue(set(sp.subsequences(str3)) == ssq3)


    def test_subsequences_3(self):
        """ Tests extraction of 3-subsequences """
        str1 = "abab"
        ssq1 = {tuple(i) for i in ["aba", "abb", "bab", "aab"]}
        str2 = "abcde"
        ssq2 = {tuple(i) for i in ["abc", "abd", "abe", "acd", "ace",
                                   "ade", "bcd", "bce", "bde", "cde"]}
        sp = SP(k=3)
        self.assertTrue(set(sp.subsequences(str1)) == ssq1)
        self.assertTrue(set(sp.subsequences(str2)) == ssq2)


    def test_learn_pos(self):
        """ Tests learning of the positive grammar. """
        data = ["abab", "abcde"]
        goal = {tuple(i) for i in ["aba", "abb", "bab", "aab", "abc", "abd",
                                   "abe", "acd", "ace", "ade", "bcd", "bce",
                                   "bde", "cde"]}
        sp = SP(k=3)
        sp.data = data
        sp.alphabet = ["a", "b", "c", "d", "e"]
        sp.learn()
        self.assertTrue(set(sp.grammar) == goal)


    def test_learn_neg(self):
        """ Tests learning of the negative grammar. """
        data = ["aaaaabbbb", "abbbb", "aaab"]
        goal = {tuple("ba")}
        sp = SP(polar="n")
        sp.data = data
        sp.alphabet = ["b", "a"]
        sp.learn()
        self.assertTrue(set(sp.grammar) == goal)


    def test_change_polarity(self):
        """ Tests change_polarity function """
        sp1 = SP(polar="p")
        sp1.change_polarity()
        self.assertTrue(sp1.check_polarity() == "n")

        sp2 = SP()
        sp2.change_polarity("p")
        sp2.change_polarity()
        self.assertTrue(sp2.check_polarity() == "n")

        sp3 = SP(polar="n")
        sp3.change_polarity()
        self.assertTrue(sp3.check_polarity() == "p")

        sp4 = SP()
        sp4.change_polarity("n")
        sp4.change_polarity()
        self.assertTrue(sp4.check_polarity() == "p")

        sp5 = SP()
        sp5.change_polarity("p")
        self.assertTrue(sp5.check_polarity() == "p")


    def test_scan_neg(self):
        """ Tests if automata correctly recognize illicit
            substructures.
        """
        sp = SP(polar="n")
        sp.grammar = [tuple("aba")]
        sp.k = 3
        sp.extract_alphabet()
        sp.fsmize()

        self.assertTrue(sp.scan("aaaa"))
        self.assertTrue(sp.scan("aaabbbbbb"))
        self.assertTrue(sp.scan("baaaaaaabbbbb"))
        self.assertTrue(sp.scan("a"))
        self.assertTrue(sp.scan("b"))

        self.assertFalse(sp.scan("aaaabaabbbba"))
        self.assertFalse(sp.scan("abababba"))
        self.assertFalse(sp.scan("abbbbabbaababab"))


    def test_generate_item(self):
        """ Tests string generation """
        sp = SP(polar="n")
        sp.grammar = [tuple("aba")]
        sp.k = 3
        sp.extract_alphabet()
        sp.fsmize()
        
        for i in range(30):
            self.assertTrue(sp.scan(sp.generate_item()))


    def test_generate_sample_pos(self):
        """
        Tests sample generation when the grammar
        is positive.
        """
        sp = SP()
        sp.grammar = [tuple(i) for i in ["ab", "ba", "bb"]]
        sp.extract_alphabet()
        sp.fsmize()

        a = sp.generate_sample(n=10)
        self.assertTrue(len(a) == 10)
        

    def test_generate_sample_neg(self):
        """
        Tests sample generation when the grammar
        is negative.
        """
        sp = SP(polar="n")
        sp.grammar = [tuple("aba")]
        sp.k = 3
        sp.extract_alphabet()
        sp.fsmize()

        a = sp.generate_sample(n=15, repeat=False)
        self.assertTrue(len(set(a)) == 15)


if __name__ == '__main__':
    unittest.main()
    
