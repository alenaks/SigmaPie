#!/bin/python3
# -*- coding: utf-8 -*-
# Subregular Toolkit: python sl_clean.py module
# Author: Alena Aksenova

"""
Module that detects useless n-grams in provided SL grammar and returns
the shortened version of the grammar.
"""

from sl_fsm import *

def trim_sl(ngrams):
    safety_check(ngrams)

    transitions = sl_to_fsm(ngrams)
    trimmed_fsm = trim_fsm(transitions, markers=[">", "<"])
    trimmed_ngrams = fsm_to_sl(trimmed_fsm)

    return trimmed_ngrams
