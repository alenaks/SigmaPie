#!/bin/python3

"""A module with the unittests for the fsm module. Copyright (C) 2020  Alena
Aksenova.

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 3 of the License, or (at your
option) any later version.
"""

import unittest
from ostia import ostia


class TestOSTIA(unittest.TestCase):
    """Tests for the OSTIA learner.

    Warning: updated versions of the learner might require updating
    the unittests.
    """

    def test_ostia_success(self):
        """Checks if OSTIA can learn a rule rewriting "a" as "1" if "a" is
        final and as "0" otherwise, and always mapping "b" to "1"."""
        S = [
            ("a", "1"),
            ("b", "1"),
            ("aa", "01"),
            ("ab", "01"),
            ("aba", "011"),
            ("aaa", "001"),
        ]
        t = ostia(S, ["a", "b"], ["0", "1"])

        transitions = {
            ("", "a", "", "a"),
            ("", "b", "1", ""),
            ("a", "a", "0", "a"),
            ("a", "b", "01", ""),
        }
        stout = {"": "", "a": "1"}

        self.assertTrue(set(t.E) == transitions)
        self.assertTrue(stout == t.stout)

    def test_ostia_fail(self):
        """Checks that OTSIA cannot learn an unbounded tone plateauing."""
        S = [
            ("HHH", "HHH"),
            ("HHL", "HHL"),
            ("HLH", "HHH"),
            ("HLL", "HLL"),
            ("HLLH", "HHHH"),
            ("HL", "HL"),
        ]
        t = ostia(S, ["H", "L"], ["H", "L"])

        transitions = {
            ("", "H", "H", "H"),
            ("H", "H", "H", ""),
            ("H", "L", "", "HL"),
            ("HL", "H", "HH", ""),
            ("HL", "L", "", "HLL"),
            ("HLL", "H", "HHH", ""),
            ("", "L", "L", ""),
        }
        stout = {"": "", "H": "", "HL": "L", "HLL": "LL"}

        self.assertTrue(set(t.E) == transitions)
        self.assertTrue(stout == t.stout)


if __name__ == "__main__":
    unittest.main()
