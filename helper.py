#!/bin/python3
# -*- coding: utf-8 -*-
# Subregular Toolkit: python helper.py module
# Author: Alena Aksenova

"""
Module with general helper functions:
 -- tokenize(obj)
 -- alphabetize(obj, text)
 -- annotate(obj, n, text)
 -- check_type(n, text)
"""

from nltk import word_tokenize


def tokenize(obj):
    """ Tokenizes a sting """
    
    return word_tokenize(obj.strip())



def alphabetize(obj, text=False):
    """ Finds smallest units to work with.
        By-default (if text=False), breakes sequences in symbols.
        If text=True, tokenizes the string, and collects list of words.
    """

    # if text==False, collect the list of symbols used
    # in the input data
    if text == False:
        alphabet = []
        for item in obj:
            for i in item:
                if i not in alphabet:
                    alphabet += [i]
        return alphabet

    # if the object is words, tokenize the object, and apply
    # the same function having words as smallest units
    else:
        obj = [tokenize(i) for i in obj]
        return alphabetize(obj, text=False)



def annotate(obj, n, text):
    """ Annotates the sequences with n-1 start/end markers.
        Is needed for successful generation of (im)possible ngrams
        and further data generation.
    """
    
    if text == False:
        return ">"*(n-1) + obj + "<"*(n-1)
    else:
        return "> "*(n-1) + obj + " <"*(n-1)



def check_type(n, text):
    """ Checks types of 'n' and 'text' arguments. """
        
    if type(n) != int:
        raise ValueError("The value of 'n' must be of the type 'int'.")
    if type(text) != bool:
        raise ValueError("The value of 'text' must be of the type 'bool'.")
