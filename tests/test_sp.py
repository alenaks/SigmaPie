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


if __name__ == '__main__':
    unittest.main()
    
