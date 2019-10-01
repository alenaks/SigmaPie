#!/bin/python3

"""
   A module with the unittests for the TSL module.
   Copyright (C) 2019  Alena Aksenova

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.abspath('..'), 'code'))

import unittest
from tsl_class import *


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


    def test_scan_pos(self):
        """ Tests recognition of strings. """
        a = TSL(polar = "p")
        a.data = ["o", "oko", "a", "aka", "oo", "aa", "kak", "kok", "kk",
                  "kkakka", "akk", "kkokko", "okk"]
        a.extract_alphabet()
        a.learn()
        self.assertTrue(a.scan("akkaka"))
        self.assertTrue(a.scan("kkk"))
        self.assertTrue(a.scan("okoko"))
        self.assertTrue(a.scan("ookokkk"))
        self.assertFalse(a.scan("okoak"))
        self.assertFalse(a.scan("okakok"))
        self.assertFalse(a.scan("kakokak"))


    def test_scan_neg(self):
        """ Tests recognition of strings. """
        a = TSL(polar = "n")
        a.data = ["o", "oko", "a", "aka", "oo", "aa", "kak", "kok", "kk",
                  "kkakka", "akk", "kkokko", "okk"]
        a.extract_alphabet()
        a.learn()
        self.assertTrue(a.scan("akkaka"))
        self.assertTrue(a.scan("kkk"))
        self.assertTrue(a.scan("okoko"))
        self.assertTrue(a.scan("ookokkk"))
        self.assertFalse(a.scan("okoak"))
        self.assertFalse(a.scan("okakok"))
        self.assertFalse(a.scan("kakokak"))


    def test_generate_item_pos(self):
        """ Tests that the generated items are grammatical.  """
        a = TSL(polar = "p")
        a.data = ["o", "oko", "a", "aka", "oo", "aa", "kak", "kok", "kk",
                  "kkakka", "akk", "kkokko", "okk"]
        a.extract_alphabet()
        a.learn()
        gen_items = [a.generate_item() for i in range(15)]
        for i in gen_items:
            self.assertTrue(a.scan(i))


    def test_generate_item_neg(self):
        """ Tests that the generated items are grammatical.  """
        a = TSL(polar = "n")
        a.data = ["o", "oko", "a", "aka", "oo", "aa", "kak", "kok", "kk",
                  "kkakka", "akk", "kkokko", "okk"]
        a.extract_alphabet()
        a.learn()
        gen_items = [a.generate_item() for i in range(15)]
        for i in gen_items:
            self.assertTrue(a.scan(i))


    def test_change_polarity_pos_to_neg(self):
        """ Checks that the polarity switching works. """
        a = TSL(polar = "p")
        a.grammar = [('>', 'o'), ('a', '<'), ('a', 'a'), ('o', 'o'), 
                    ('o', '<'), ('>', 'a'), ('>', '<')]
        a.tier = ["a", "o"]
        a.switch_polarity()
        self.assertTrue(set(a.grammar) == {('a', 'o'), ('o', 'a')})
        self.assertTrue(a.check_polarity() == "n")

        b = TSL(polar = "p")
        b.data = ["aaaab", "abaaaa", "b"]
        b.extract_alphabet()
        b.learn()
        b.switch_polarity()
        self.assertTrue(set(b.grammar) == {('b', 'b'), ('>', '<')})
        self.assertTrue(b.check_polarity() == "n")



    def test_change_polarity_neg_to_pos(self):
        """ Checks that the polarity switching works. """
        a = TSL(polar = "n")
        expected = {('>', 'o'), ('a', '<'), ('a', 'a'), ('o', 'o'), 
                    ('o', '<'), ('>', 'a'), ('>', '<')}
        a.grammar = [('a', 'o'), ('o', 'a')]
        a.tier = ["a", "o"]
        a.switch_polarity()
        self.assertTrue(set(a.grammar) == expected)
        self.assertTrue(a.check_polarity() == "p")


        b = TSL(polar = "n")
        b.data = ["aaaab", "abaaaa", "b"]
        b.extract_alphabet()
        b.learn()
        b.switch_polarity()
        self.assertTrue(set(b.grammar) == {('>', 'b'), ('b', '<')})
        self.assertTrue(b.check_polarity() == "p")


    def test_polarity_raised_issue(self):
        """ Checks a specific case from the GitHub issue. """
        a = TSL(polar = "p")
        a.grammar = [('>', 'a'), ('a', 'b'), ('b', '<'), ('b', 'a')]
        a.tier = ["a", "b"]
        a.switch_polarity()
        expected = {('a', 'a'), ('a', '<'), ('b', 'b'), 
                    ('>', 'b'), ('>', '<')}
        self.assertTrue(set(a.grammar) == expected)
        self.assertTrue(a.check_polarity() == "n")


    def test_generate_sample(self):
        a = TSL(polar = "p")
        a.grammar = [('>', 'a'), ('a', 'b'), ('b', '<'), ('b', 'a')]
        a.tier = ["a", "b"]
        a.alphabet = ["a", "b", "c"]

        sample = a.generate_sample(n=10, repeat=False)
        for i in sample:
            self.assertTrue(a.scan(i))


if __name__ == '__main__':
    unittest.main()
    
