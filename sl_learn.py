#!/bin/python3
# -*- coding: utf-8 -*-
# Subregular Toolkit: python sl.py module
# Author: Alena Aksenova

"""
Module that extracts Strictly Local (SL) grammar from the input
data. Basically, creates a list of n-grams that is capable of
generating that data set.

*** find_sl ***       extracts SL grammar from a given data/file
*** ngramize_all ***  ngramizes the data/file
*** ngramize_item *** auxiliary function for ngramize_all
"""

from helper import *
from local_helper import *


def find_sl(obj, n=2, positive=False, param="s"):
    """ Extracts SL grammar based on the input data. """

    check_type(obj, n, positive, param)
    
    # if a string was given as 'obj', assume that it's a filename
    if type(obj) == str:
        if obj.endswith(".txt") or obj.endswith(".csv"):
            obj = open(obj, "r+")
        else:
            raise ValueError("Incorrect extension: must be '.txt' or '.csv'.")

    alphabet = list(alphabetize(obj, param))
    pos_grammar = ngramize_all(obj, n, param)

    # if positive grammar is requested, return as it is
    if positive==True:
        report("Positive strictly {}-local".format(n), alphabet, pos_grammar, param)
        return pos_grammar

    # if negative grammar is requested, convert pos_grammar to negative
    neg_grammar = change_polarity(pos_grammar, alphabet, n)
    report("Negative strictly {}-local".format(n), alphabet, neg_grammar, param)
    return neg_grammar



def ngramize_all(obj, n, param):
    """ Ngramizes the input items. """

    try: obj.seek(0)
    except: pass
    
    grammar = set()
    for i in obj:
        # annotate every input item with the start/end markers,
        # and only then ngramize it
        item = annotate(i, n, param)
        subgrammar = ngramize_item(item, n, param)
        
        for j in subgrammar:
            grammar.add(j)

    return grammar



def ngramize_item(obj, n, param):
    """ Ngramizes object and returns the set of arrays,
        where each array contains n elements.
        If object is words, first tokenizes the object.
    """

    obj = preprocess(obj,param)

    # collect the tuple of possible ngrams
    output = ()
    for t in range(len(obj)-(n-1)):
        ngram = tuple(obj[t:t+n])
        if ngram not in output:
            output = output + (ngram,)
            
    return output
