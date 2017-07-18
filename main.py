#!/bin/python3
# -*- coding: utf-8 -*-
# Subregular Toolkit: __init__.py module
# Author: Alena Aksenova

import sl_learn, tsl_learn, helper

""" List of funstions:

    --- find_sl(data, n, polar, param) ---
    Extracts strictly local grammar from the given data set.
    Arguments:
    * data (any iterable or a filename) -- data to be analyzed
    * polar (True or False) -- positive/negative grammar to be extracted
    * n (integer) -- length of ngrams to be constructed
    * param ("s", "m", "w") -- type of the data: symbols, morphemes, or words

    --- find_tsl(data, n, polar, param) ---
    Extracts tier-based strictly local grammar from the given
    data set. Follows the algorithm provided in (Jardine and
    McMullin in prep.) with small modifications.
    Arguments: see find_sl function.

    --- alphabet(data, param) ---
    Collects alphabet based on the input data type ("s", "m", "w")
    Arguments:
    * data (any iterable) -- data to be analyzed
    * param ("s", "m", "w") -- type of the data, symbols, morphemes, or words
    
"""

def find_sl(data, n=2, polar=False, param="s"):
    return sl_learn.find_sl(data, n, polar, param)

def find_tsl(data, n=2, polar=False, param="s"):
    return tsl_learn.find_tsl(data, n, polar, param)

def alphabet(data, param="s"):
    return helper.alphabetize(data, param)
