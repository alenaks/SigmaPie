#!/bin/python3
# -*- coding: utf-8 -*-
# Subregular Toolkit: python sl.py module
# Author: Alena Aksenova

"""
Module that extracts Strictly Local (SL) grammar from the input
data. Basically, creates a list of n-grams that is capable of
generating that data set.
"""

from helper import *


def find_sl(obj, n=2, text=False):
    """ Extracts SL grammar based on the input data. """

    # checks that the data types are appropriate
    check_type(n, text)
    # if a single word was given as dataset, convert it to a list
    if type(obj) == str:
        obj = [obj]
            
    return ngramize_all(obj, n, text)            



def ngramize_all(obj, n, text):
    """ Ngramizes the input items. """

    grammar = set()
    for i in range(len(obj)):
        # annotate every input item with the start/end markers,
        # and only then ngramize it
        item = annotate(obj[i], n, text)
        subgrammar = ngramize_item(item, n, text)
        
        for j in subgrammar:
            grammar.add(j)

    return grammar



def ngramize_item(obj, n, text):
    """ Ngramizes object and returns the set of arrays,
        where each array contains n elements.
        If object is words, first tokenizes the object.
    """

    # if the object is not text, make a list of symbols
    if text == False:
        if type(obj) == str:
            obj = list(obj.strip())

        # collect the tuple of possible ngrams
        output = ()
        for t in range(len(obj)-(n-1)):
            ngram = tuple(obj[t:t+n])
            if ngram not in output:
                output = output + (ngram,)
            
        return output
 
    elif text == True:
            
        # if the object is text, tokenize it first
        obj = tokenize(obj.strip())
        return ngramize_item(obj, n, text=False)
