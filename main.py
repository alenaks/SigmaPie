#!/bin/python3
# -*- coding: utf-8 -*-
# Subregular Toolkit: __init__.py module
# Author: Alena Aksenova

import sl_learn, tsl_learn, helper, sl_clean, sl_fsm

""" List of funstions:

    --- find_sl(data, n, positive, param) ---
    Extracts strictly local grammar from the given data set.
    Arguments:
    * data (any iterable or a filename) -- data to be analyzed
    * positive (True or False) -- positive/negative grammar to be extracted
    * n (integer) -- length of ngrams to be constructed
    * param ("s", "m", "w") -- type of the data: symbols, morphemes, or words

    --- find_tsl(data, n, positive, param) ---
    Extracts tier-based strictly local grammar from the given
    data set. Follows the algorithm provided in (Jardine and
    McMullin in prep.) with small modifications.
    Arguments: see find_sl function.

    --- alphabet(data, param) ---
    Collects alphabet based on the input data type ("s", "m", "w").
    Arguments:
    * data (any iterable) -- data to be analyzed
    * param ("s", "m", "w") -- type of the data, symbols, morphemes, or words

    --- trim_sl(ngrams) ---
    Cleans the given grammar from useless (never occurring) ngrams.
    Arguments:
    * ngrams -- list of ngrams

    --- sl_to_fsm(ngrams) ---
    Translates SL grammar to the correspondong FSM.
    Arguments:
    * ngrams -- list of ngrams

    --- fsm_to_sl(transitions) ---
    Translates FSM to the corresponding SL grammar.
    Arguments:
    * transitions -- collection of transitions in the FSM
    
"""

def find_sl(data, n=2, positive=False, param="s"):
    return sl_learn.find_sl(data, n, positive, param)

def find_tsl(data, n=2, positive=False, param="s"):
    return tsl_learn.find_tsl(data, n, positive, param)

def alphabet(data, param="s"):
    return helper.alphabetize(data, param)

def trim_sl(ngrams, positive=True):
    return sl_clean.trim_sl(ngrams, positive)

def sl_to_fsm(ngrams):
    return sl_fsm.sl_to_fsm(ngrams)

def fsm_to_sl(transitions):
    return sl_fsm.fsm_to_sl(transitions)
