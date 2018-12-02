#!/bin/python3

"""
   A module with the unittests for the TSL module.
   Copyright (C) 2018  Alena Aksenova

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.
"""

import sys, os
sys.path.insert(0, os.path.abspath('..'))

import unittest
from PyKleene.tsl_class import *


class TestTSLLanguages(unittest.TestCase):
    """ Tests for the TSL class. """

    def test_tier_learning(self):
        """ Tests the tier learning function. """
        a = TSL()
        a.data = ["aaaab", "abaaaa", "b"]
        a.alphabet = ["a", "b"]
        a.learn_tier()
        self.assertTrue(a.tier == ["b"])

        b = TSL()
        b.data = ["ccaccaccbc", "acbbaababc", "ababbab"]
        b.alphabet = ["a", "b", "c"]
        b.learn_tier()
        self.assertTrue(set(b.tier) == {"a", "b"})

    def test_tier_image(self):
        """ Tests the erasing function. """
        a = TSL()
        a.tier = ["a"]
        self.assertTrue(a.tier_image("cvamda") == "aa")


    def test_learn_pos(self):
        """ Tests learning of the positive TSL grammar. """
        a = TSL()
        a.data = ["o", "oko", "a", "aka", "oo", "aa", "kak", "kok", "kk",
                  "kkakka", "akk", "kkokko", "okk"]
        a.extract_alphabet()
        a.learn()
        goal = {('>', '<'), ('>', 'a'), ('a', 'a'), ('>', 'o'), ('o', 'o'),
                ('a', '<'), ('o', '<')}
        self.assertTrue(set(a.grammar) == goal)
        self.assertTrue(set(a.tier) == {"a", "o"})


    def test_learn_neg(self):
        """ Tests learning of the negative TSL grammar. """
        a = TSL(polar="n")
        a.data = ["o", "oko", "a", "aka", "oo", "aa", "kak", "kok", "kk",
                  "kkakka", "akk", "kkokko", "okk"]
        a.extract_alphabet()
        a.learn()
        goal = {('a', 'o'), ('o', 'a')}
        self.assertTrue(set(a.grammar) == goal)
        self.assertTrue(set(a.tier) == {"a", "o"})

if __name__ == '__main__':
    unittest.main()
    
