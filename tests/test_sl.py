#!/bin/python3

"""
   A module with the unittests for the grammar module.
   Copyright (C) 2018  Alena Aksenova

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.
"""

import sys, os
sys.path.insert(0, os.path.abspath('..'))

import unittest
from PyKleene.sl_class import *


class TestSLLanguages(unittest.TestCase):
    """ Tests for the SL class. """

    def test_learn(self):
        data = ["abab", "ababab"]
        gpos = {(">", "a"), ("b", "a"), ("a", "b"), ("b", "<")}
        gneg = {(">", "<"), ("a", "<"), (">", "b"), ("b", "b"), ("a", "a")}

        a = SL(data=data, alphabet=["a", "b"])
        a.learn()
        self.assertTrue(set(a.grammar) == gpos)

        a.change_polarity()
        a.learn()
        self.assertTrue(set(a.grammar) == gneg)
    

if __name__ == '__main__':
    unittest.main()
    
