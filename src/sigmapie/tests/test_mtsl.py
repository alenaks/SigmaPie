#!/bin/python3

"""A module with the unit tests for the MTSL module. Copyright (C) 2019  Alena
Aksenova.

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 3 of the License, or (at your
option) any later version.
"""

import unittest
import unittest.mock
from mtsl_class import *


class TestMTSLLanguages(unittest.TestCase):
    """Tests for the MTSL class."""

    def test_grammar_learning_neg(self):
        """Tests the learner."""
        a = MTSL(polar="n")
        VC = [
            "aabbaabb",
            "abab",
            "aabbab",
            "abaabb",
            "aabaab",
            "abbabb",
            "ooppoopp",
            "opop",
            "ooppop",
            "opoopp",
            "oopoop",
            "oppopp",
            "aappaapp",
            "apap",
            "aappap",
            "apaapp",
            "aapaap",
            "appapp",
            "oobboobb",
            "obob",
            "oobbob",
            "oboobb",
            "ooboob",
            "obbobb",
            "aabb",
            "ab",
            "aab",
            "abb",
            "oopp",
            "op",
            "oop",
            "opp",
            "oobb",
            "ob",
            "oob",
            "obb",
            "aapp",
            "ap",
            "aap",
            "app",
            "aaa",
            "ooo",
            "bbb",
            "ppp",
            "a",
            "o",
            "b",
            "p",
            "",
        ]
        expected = {
            ("a", "o"): [("a", "o"), ("o", "a")],
            ("b", "p"): [("b", "p"), ("p", "b")],
        }
        a.data = VC[:]
        a.extract_alphabet()
        a.learn()

        correct = True
        for i in a.grammar:
            if not (i in expected and set(a.grammar[i]) == set(expected[i])):
                correct = False
        if len(a.grammar) != len(expected):
            correct = False

        self.assertTrue(correct)

    def test_grammar_learning_pos(self):
        """Tests the learner."""
        b = MTSL(polar="p")
        VC = [
            "aabbaabb",
            "abab",
            "aabbab",
            "abaabb",
            "aabaab",
            "abbabb",
            "ooppoopp",
            "opop",
            "ooppop",
            "opoopp",
            "oopoop",
            "oppopp",
            "aappaapp",
            "apap",
            "aappap",
            "apaapp",
            "aapaap",
            "appapp",
            "oobboobb",
            "obob",
            "oobbob",
            "oboobb",
            "ooboob",
            "obbobb",
            "aabb",
            "ab",
            "aab",
            "abb",
            "oopp",
            "op",
            "oop",
            "opp",
            "oobb",
            "ob",
            "oob",
            "obb",
            "aapp",
            "ap",
            "aap",
            "app",
            "aaa",
            "ooo",
            "bbb",
            "ppp",
            "a",
            "o",
            "b",
            "p",
            "",
        ]
        expected2 = {
            ("a", "o"): [
                (">", "a"),
                ("a", "<"),
                ("a", "a"),
                (">", "o"),
                ("o", "o"),
                ("o", "<"),
                (">", "<"),
            ],
            ("b", "p"): [
                (">", "b"),
                ("b", "b"),
                ("b", "<"),
                (">", "p"),
                ("p", "p"),
                ("p", "<"),
                (">", "<"),
            ],
        }

        b.data = VC[:]
        b.extract_alphabet()
        b.learn()

        correct = True
        for i in b.grammar:
            if not (i in expected2 and set(b.grammar[i]) == set(expected2[i])):
                correct = False
        if len(b.grammar) != len(expected2):
            correct = False

        self.assertTrue(correct)

    @unittest.mock.patch(
        # Artificially enforce a particular case of list(set())'s naturally-
        # occurring non-determinism with respect to ordering: 
        # make it ascending if odd number of elements, descending if even.

        # While impractical, this re-implementation of list(set()) is perfectly
        # legal. It could be discarded, but that way, the test becomes
        # non-deterministic and reveals the bug only in some 10% of runs.

        "mtsl_class.list", 
        new=lambda x: sorted(x, reverse=len(x) % 2 == 0) \
                      if type(x) == set else list(x)
    )
    def test_grammar_learning_raised_issue(self):
        """Checks a specific case related to GitHub issue #6."""
        mtsl = MTSL(k=2, polar="n")
        mtsl.data = ["axb", "ayxb", "azxb", "azxyb"]
        mtsl.extract_alphabet()
        mtsl.learn()
        self.assertTrue(all({*tier} == {"a", "b", "x"} for tier, restrict \
                            in mtsl.grammar.items() if ("a", "b") in restrict))

    def test_convert_pos_to_neg(self):
        """Tests conversion of a positive grammar to a negative one."""
        z = MTSL(polar="p")
        z.grammar = {
            ("a", "o"): [
                (">", "a"),
                ("a", "<"),
                ("a", "a"),
                (">", "o"),
                ("o", "o"),
                ("o", "<"),
                (">", "<"),
            ],
            ("b", "p"): [
                (">", "b"),
                ("b", "b"),
                ("b", "<"),
                (">", "p"),
                ("p", "p"),
                ("p", "<"),
                (">", "<"),
            ],
        }
        z.switch_polarity()
        expected = {
            ("a", "o"): [("a", "o"), ("o", "a")],
            ("b", "p"): [("b", "p"), ("p", "b")],
        }
        self.assertTrue(z.grammar == expected)

    def test_scan_pos(self):
        """Tests scanning using a positive grammar."""
        c = MTSL(polar="p")
        c.grammar = {
            ("a", "o"): [
                (">", "a"),
                ("a", "<"),
                ("a", "a"),
                (">", "o"),
                ("o", "o"),
                ("o", "<"),
                (">", "<"),
            ],
            ("b", "p"): [
                (">", "b"),
                ("b", "b"),
                ("b", "<"),
                (">", "p"),
                ("p", "p"),
                ("p", "<"),
                (">", "<"),
            ],
        }
        for s in ["apapappa", "ppp", "appap", "popo", "bbbooo"]:
            self.assertTrue(c.scan(s))
        for s in ["aoap", "popa", "pbapop", "pabp", "popoa"]:
            self.assertFalse(c.scan(s))

    def test_scan_neg(self):
        """Tests scanning using a positive grammar."""
        d = MTSL(polar="n")
        d.grammar = {
            ("a", "o"): [("a", "o"), ("o", "a")],
            ("b", "p"): [("b", "p"), ("p", "b")],
        }
        for s in ["apapappa", "ppp", "appap", "popo", "bbbooo"]:
            self.assertTrue(d.scan(s))
        for s in ["aoap", "popa", "pbapop", "pabp", "popoa"]:
            self.assertFalse(d.scan(s))


if __name__ == "__main__":
    unittest.main()
