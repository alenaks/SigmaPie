#!/bin/python3
# -*- coding: utf-8 -*-
# Subregular Toolkit: __init__.py module
# Author: Alena Aksenova

import sl, tsl, helper

""" List of funstions:

    --- find_sl(data, n, text) ---
    Extracts strictly local grammar from the given data set.
    Arguments:
    * data (any iterable) -- data to be analyzed
    * n (integer) -- length of ngrams to be constructed
    * text (boolean) -- type of the data, symbols or text

    --- find_tsl(data, n, text) ---
    Extracts tier-based strictly local grammar from the given
    data set. Follows the algorithm provided in (Jardine and
    McMullin in prep.)
    Arguments: see find_sl function.

    --- alphabet(data, text) ---
    Collects alphabet based on the input data. If text=False,
    considers words to be alphabet units.
    Arguments:
    * data (any iterable) -- data to be analyzed
    * text (boolean) -- type of the data, symbols or text
    
"""

def find_sl(data, n=2, text=False):
    return sl.find_sl(data, n, text)

def find_tsl(data, n=2, text=False):
    return tsl.find_tsl(data, n, text)

def alphabet(data, text=False):
    return helper.alphabetize(data, text)
