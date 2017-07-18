#!/bin/python3
# -*- coding: utf-8 -*-
# Subregular Toolkit: python local_helper.py module
# Author: Alena Aksenova

"""
Module with auxiliary functions for sl_learn and tsl_learn

*** change_polarity ***  changes polarity of a SL/TSL grammar
                         negative <-> positive
*** generate_ngrams ***  generates possible ngrams based on the
                         given alphabet
*** start_end_clean ***  gets rid of the ill-formed ngrams (like
                         "a>a" or "<<<")
"""

from itertools import product


def change_polarity(grammar, alphabet, n):
    """ For a given pos/neg local grammar,
        returns its neg/pos version
    """

    poss_seq = generate_ngrams(alphabet, n)
    return poss_seq.difference(grammar)



def generate_ngrams(init_alphabet, n):
    """ Generate possible sequences of the length n"""

    alphabet = init_alphabet[:]
    alphabet += [">", "<"]
    full_combinations = product(alphabet, repeat=n)

    # get rid of ill-formed tier sequences
    combinations = set([i for i in full_combinations if start_end_clean(i)])
        
    return combinations


def start_end_clean(seq):
    """ Auxiliary function for the tier sequence generator """

    # Start symbols exceptions:
    # -- nothing in-between two start symbols (i.e., '>a>')
    # -- nothing before a start symbol (i.e., 'a>')
    # -- amount of start symbols is less than n (i.e., '>>>')
    start = [i for i in range(len(seq)) if seq[i] == ">"]
    if len(start) > 0:
        s_inter = [i for i in range(start[0], start[-1]) if i not in start]
        if len(s_inter) > 0:
            return False
        elif start[0] != 0:
            return False
        elif len(start) == len(seq):
            return False

    # End symbols exceptions:
    # -- nothing in-between two end symbols (i.e., '<a<')
    # -- nothing after an end symbol (i.e., '<a')
    # -- amount of end symbols is less than n (i.e., '<<<')
    end = [i for i in range(len(seq)) if seq[i] == "<"]
    if len(end) > 0:
        e_inter = [i for i in range(end[0], end[-1]) if i not in end]
        if len(e_inter) > 0:
            return False
        elif end[-1] != (len(seq)-1):
            return False
        elif len(end) == len(seq):
            return False

    return True
