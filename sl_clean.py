#!/bin/python3
# -*- coding: utf-8 -*-
# Subregular Toolkit: python sl_clean.py module
# Author: Alena Aksenova

"""
Module that detects useless n-grams in provided SL grammar and returns
the shortened version of the grammar.
"""

from sl_fsm import *
from local_helper import change_polarity
from helper import get_info

def trim_sl(ngrams, positive=True):

    alphabet, k = get_info(ngrams, "s")
    
    if positive == False:
        ngrams = change_polarity([tuple(i) for i in ngrams], list(alphabet), k)
        ngrams = ["".join(x) for x in ngrams]

    transitions = sl_to_fsm(ngrams)
    trimmed_fsm = trim_fsm(transitions, markers=[">", "<"])
    trimmed_ngrams = fsm_to_sl(trimmed_fsm)

    print("Positive grammar:\n", trimmed_ngrams)
    
    return trimmed_ngrams
