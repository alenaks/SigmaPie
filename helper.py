#!/bin/python3
# -*- coding: utf-8 -*-
# Subregular Toolkit: python helper.py module
# Author: Alena Aksenova

"""
Module with general helper functions.

*** tokenize ***    nltk word_tokenize function
*** alphabetize *** collects alphabet from the input data
*** annotate ***    annotates each item from the input object with
                    start and end symbols
*** preprocess ***  parses the input file(s)
*** check_type ***  checks that the types of the input data is
                    of the appropriate type
*** report ***      reports on the extracted grammar
"""

from nltk import word_tokenize


def tokenize(obj):
    """ Tokenizes a sting """
    
    return word_tokenize(obj.strip())



def alphabetize(obj, param):
    """ Finds smallest units to work with.
        By-default (if text=False), breakes sequences in symbols.
        If text=True, tokenizes the string, and collects list of words.
    """
    
    try: obj.seek(0)
    except: pass

    alphabet = set()
    for line in obj:
        alphabet.update(preprocess(line, param))
    return alphabet



def annotate(obj, n, param):
    """ Annotates the sequences with n-1 start/end markers.
        Is needed for successful generation of (im)possible ngrams
        and further data generation.
    """
    
    if param == "s":
        return ">"*(n-1) + obj.strip() + "<"*(n-1)
    elif param == "w":
        return "> "*(n-1) + obj.strip() + " <"*(n-1)
    elif param == "m":
        return ">-"*(n-1) + obj.strip() + "-<"*(n-1)
    else:
        raise ValueError()



def preprocess(obj, param):
    """ Preprocessing function: depending on the type of an object,
        parses it.
    """

    # if the object is not text, make a list of symbols
    if param == "s":
        obj = list(obj.strip())
        
    elif param == "w":
            
        # if the object is text, tokenize it first
        obj = tokenize(obj.strip())

    elif param == "m":

        # if the object is a list of morphemes, split it by a dash
        obj = obj.replace("-", " ")
        obj = tokenize(obj.strip())
        
    else:
        raise RuntimeError("Unexpected behavior: please, report.")

    return obj



def check_type(obj, n, positive, param):
    """ Checks types of 'obj', 'n' and 'text' arguments. """

    if type(obj) not in [str, list, tuple]:
        raise TypeError("The type of 'obj' must be either 'str' for a filename, or 'list'/'tuple' for a dataset.")
    if type(n) != int:
        raise TypeError("The type of 'n' must be 'int'.")
    if type(positive) != bool:
        raise TypeError("The type of 'positive' must be 'bool'.")
    if param not in ["w", "m", "s"]:
        raise ValueError("The value of 'param' must be 'w' for words, 'm' for morphemes, or 's' for symbols.")



def report(info, alphabet, grammar, param):
    """ Prints the info about the generated grammar """
    
    if param == "s":
        t = "symbols"
    elif param == "m":
        t = "morphemes"
    elif param == "w":
        t = "words"
    print("{} grammar constructed.".format(info))
    print("Alphabet ({}): {}".format(t, alphabet))
    print("Grammar: {}".format(grammar))
