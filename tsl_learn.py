#!/bin/python3
# -*- coding: utf-8 -*-
# Subregular Toolkit: python tsl.py module
# Author: Alena Aksenova

"""
Module that extracts Tier-based Strictly k-Local (k-TSL) grammar
from the input data. The algorithm implemented is from (Jardine
and McMullin in prep.)
"""

from itertools import product
from helper import *
from sl import *


def find_tsl(obj, n=2, text=False):
    """ Extracts TSL grammar from the input data """

    # preprocessing
    check_type(n, text)
    if type(obj) == str:
        obj = [obj]

    # assume the tier alphabet to be the same as the
    # alphabet of the initial string
    sigma = alphabetize(obj, text)
    tier = sigma[:]

    # collect the set of ngrams
    ngrams = ngramize_all(obj, n, text)

    # for every symbol in tier, check whether the two tests hold
    # if they do, remove this symbol from the list of the tier elements
    for symb in sigma:
        if test_insert(obj, n, text, symb, ngrams) and test_remove(obj, n, text, symb, ngrams):
            tier.remove(symb)

    # generate all possible tier ngrams
    possib = generate_tier_ngr(tier, n)

    # do not show start/end markers in tier alphabet
    tier = [i for i in tier if i not in ["<", ">"]]

    # extract from the set of possible ngrams those that are allowed
    # construct the negative tsl grammar
    R = possib.difference(ngrams)
    print("Tier alphabet:\n", tier, "\n")
    print("Negative TSL grammar:\n", R, "\n")
                
    return tier, R



def test_insert(obj, n, text, symb, ngrams):
    """ Insertion test: check that for in every (n-1)-gram of the
        original text it is possible to insert the symbols under
        consideration in it. If not, it is a tier symbol.
    """

    # get the list of (n-1)-grams
    test = ngramize_all(obj, n-1, text)
    
    # deal with the special case where "<" and ">" are lost
    if (n-1) == 1:
        test.add((">",))
        test.add(("<",))

    # if a symbol can be inserted anywhere, it might be not
    # a tier symbol, depends on the second test
    answer = True
    for i in test:
        a = set(gen_insert(i, symb))
        if not (a.issubset(ngrams)):
            answer = False
            
    return answer


def gen_insert(ngram, symb):
    """ Auxiliary function for the insertion test """
    
    # define start as 0 or index after the last ">"
    # define end as the last index or index after the first "<"
    start = 0
    end = len(ngram)+1
    if ">" in ngram:
        ind = [x for x in range(len(ngram)) if ngram[x] == ">"]
        start = ind[-1]+1
    if "<" in ngram:
        ind = [x for x in range(len(ngram)) if ngram[x] == "<"]
        end = ind[0] + 1

    # generate possible sequences where the symbol is inserted
    # in the ngram
    for i in range(start, end):
        yield ngram[:i] + (symb,) + ngram[i:]



def test_remove(obj, n, text, symb, ngrams):
    """ Deleteion test: check that for all (n+1)-grams containint
        the symbol under consideration, this symbol can be removed
        from there. If not, it is a tier symbol.
    """

    # get the list of (n+1)-grams containing the needed symbol
    t = ngramize_all(obj, n+1, text)
    test = set([i for i in t if (symb in i) and (i[n-1] != ">") \
                and (i[-n] != "<")])

    # if a symbol can be removed from anywhere, it might be not
    # a tier symbol, depends on the first test
    answer = True
    for i in test:
        a = set(gen_remove(i, symb))
        if not (a.issubset(ngrams)):
            answer = False
            
    return answer


def gen_remove(ngram, symb):
    """ Auxiliary function for the deletion test """

    # generate a set of sequences where each instance of the symbol
    # is removed from the ngram
    for i in range(len(ngram)):
        if ngram[i] == symb:
            yield ngram[:i] + ngram[i+1:]



def generate_tier_ngr(tier, n):
    """ Generate possible tier sequences """
    
    tier += [">", "<"]
    full_combinations = product(tier, repeat=n)

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
