#!/bin/python3

"""
   A module with the unittests for the SP module.
   Copyright (C) 2018  Alena Aksenova

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.
"""

import sys, os
sys.path.insert(0, os.path.abspath('..'))

import unittest
from PyKleene.sp_class import *


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


if __name__ == '__main__':
    unittest.main()
    
