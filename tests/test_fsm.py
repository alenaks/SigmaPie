#!/bin/python3

"""
   A module with the unittests for the fsm module.
   Copyright (C) 2019  Alena Aksenova

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.abspath('..'), 'code'))

import unittest
from fsm import FSM


class TestFSM(unittest.TestCase):
    """ Tests for the FSM class. """

    def test_sl_to_fsm_2(self):
        """ Checks if a 2-SL grammar translates to FSM correctly. """
        f = FSM(initial=">", final="<")
        grammar = [(">", "a"), ("b", "a"), ("a", "b"), ("b", "<")]
        f.sl_to_fsm(grammar)

        tr = {((">",), "a", ("a",)), (("b",), "a", ("a",)),
              (("a",), "b", ("b",)), (("b",), "<", ("<",))}
        self.assertTrue(set(f.transitions) == tr)


    def test_sl_to_fsm_3(self):
        """ Checks if a 3-SL grammar translates to FSM correctly. """
        f = FSM(initial=">", final="<")
        grammar = [(">", "a", "b"), ("a", "b", "a"), ("b", "a", "b"),
                   ("a", "b", "<"), (">", ">", "a"), ("b", "<", "<")]
        f.sl_to_fsm(grammar)

        tr = {((">", "a"), "b", ("a", "b")), (("a", "b"), "a", ("b", "a")),
              (("b", "a"), "b", ("a", "b")), (("a", "b"), "<", ("b", "<")),
              ((">", ">"), "a", (">", "a")), (("b", "<"), "<", ("<", "<"))}
        self.assertTrue(set(f.transitions) == tr)


    def test_scan_sl_2(self):
        """ Checks if a FSM for 2-SL grammar can correctly
            recognize strings.
        """
        f = FSM(initial=">", final="<")
        f.transitions = [((">",), "a", ("a",)), (("b",), "a", ("a",)),
                         (("a",), "b", ("b",)), (("b",), "<", ("<",))]

        self.assertTrue(f.scan_sl(">abab<"))
        self.assertTrue(f.scan_sl(">ab<"))
        self.assertTrue(f.scan_sl(">abababab<"))

        self.assertFalse(f.scan_sl("><"))
        self.assertFalse(f.scan_sl(">a<"))
        self.assertFalse(f.scan_sl(">ba<"))
        self.assertFalse(f.scan_sl(">ababbab<"))


    def test_scan_sl_3(self):
        """ Checks if a FSM for 3-SL grammar can correctly
            recognize strings.
        """
        f = FSM(initial=">", final="<")
        f.transitions = [((">", "a"), "b", ("a", "b")),
                         (("a", "b"), "a", ("b", "a")),
                         (("b", "a"), "b", ("a", "b")),
                         (("a", "b"), "<", ("b", "<")),
                         ((">", ">"), "a", (">", "a")),
                         (("b", "<"), "<", ("<", "<"))]

        self.assertTrue(f.scan_sl(">>abab<<"))
        self.assertTrue(f.scan_sl(">ab<"))
        self.assertTrue(f.scan_sl(">>abababab<<"))

        self.assertFalse(f.scan_sl(">><<"))
        self.assertFalse(f.scan_sl(">>a<<"))
        self.assertFalse(f.scan_sl(">>ba<<"))
        self.assertFalse(f.scan_sl(">>ababbab<<"))


    def test_trim_fsm_2(self):
        f = FSM(initial=">", final="<")
        f.transitions = [((">",), "a", ("a",)), (("b",), "a", ("a",)),
                         (("a",), "b", ("b",)), (("b",), "<", ("<",)),
                         ((">",), "c", ("c",)), (("d",), "<", ("<",))]
        goal = {((">",), "a", ("a",)), (("b",), "a", ("a",)),
                (("a",), "b", ("b",)), (("b",), "<", ("<",))}
        f.trim_fsm()
        self.assertTrue(set(f.transitions) == goal)


    def test_trim_fsm_3(self):
        f = FSM(initial=">", final="<")
        f.transitions = [((">", "a"), "b", ("a", "b")),
                         (("a", "b"), "a", ("b", "a")),
                         (("b", "a"), "b", ("a", "b")),
                         (("a", "b"), "<", ("b", "<")),
                         ((">", ">"), "a", (">", "a")),
                         (("b", "<"), "<", ("<", "<")),
                         ((">", "b"), "j", ("b", "j")),
                         ((">", ">"), "j", (">", "j")),
                         (("j", "k"), "o", ("k", "o"))]
        goal = {((">", "a"), "b", ("a", "b")), (("a", "b"), "a", ("b", "a")),
                (("b", "a"), "b", ("a", "b")), (("a", "b"), "<", ("b", "<")),
                ((">", ">"), "a", (">", "a")), (("b", "<"), "<", ("<", "<"))}
        f.trim_fsm()
        self.assertTrue(set(f.transitions) == goal)

if __name__ == '__main__':
    unittest.main()
    
