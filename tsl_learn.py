#!/bin/python3
# -*- coding: utf-8 -*-
# Subregular Toolkit: python tsl.py module
# Author: Alena Aksenova

"""
Module that extracts Tier-based Strictly k-Local (k-TSL) grammar
from the input data. The algorithm implemented is by (Jardine
and McMullin in prep.), with a small modification (third test).

*** find_tsl ***    extracts TSL grammar from a given data/file
*** erase ***       generator that yields tier image of the input data
*** erase_test ***  generates tier ngrams of the data under the erase
                    image and checks that it is subset of the ngrams of
                    the input data
*** test_insert *** insertion test, checks that for every (k-1)-gram, a
                    potentially non-tier symbol can be inserted
*** gen_insert ***  auxiliary function for test_insert
*** test_remove *** deletion test, checks that for every (k+1)-gram, a
                    potentially non-tier symbol can be removed
*** gen_remove ***  auxiliary function for test_remove
"""

from helper import *
from local_helper import *
from sl_learn import *


def find_tsl(obj, n=2, positive=False, param="s"):
    """ Extracts TSL grammar from the input data """

    # preprocessing
    check_type(obj, n, positive, param)
    
    # if a string was given as 'obj', assume that it's a filename
    if type(obj) == str:
        if obj.endswith(".txt") or obj.endswith(".csv"):
            obj = open(obj, "r+")
        else:
            raise ValueError("Incorrect extension: must be '.txt' or '.csv'.")

    # assume the tier alphabet to be the same as the
    # alphabet of the initial string
    sigma = list(alphabetize(obj, param))
    tier = sigma[:]

    # collect the set of ngrams
    ngrams = ngramize_all(obj, n, param)

    # for every symbol in tier, check whether the two tests hold
    for symb in sigma:
        if test_insert(obj, n, param, symb, ngrams) and test_remove(obj, n, param, symb, ngrams):
            # if they do, check whether removing this symbol from the tier will
            # produce tier sequences that were not found in the input data
            if erase_test(obj, tier, param, ngrams, symb, n):
                # if no, remove the symbol from the tier
                tier.remove(symb)

    # generate all possible tier ngrams
    possib = generate_ngrams(tier, n)

    # extract from the set of possible ngrams those that are allowed
    # construct the negative tsl grammar
    neg_gram = possib.difference(ngrams)

    # if the requested grammar is positive, change its polarity
    if positive == True:
        pos_gram = change_polarity(neg_gram, tier, n)
        report("Positive tier-based strictly {}-local".format(n), tier, pos_gram, param)
        return pos_gram

    # if negative grammar is expected, return it without modifications
    report("Negative tier-based strictly {}-local".format(n), tier, neg_gram, param)               
    return neg_gram

    

def erase(data, tier, param):
    """ Removes non-tier symbols from the data """

    for item in data:
        parsed = preprocess(item, param)
        tier_image = []

        # collects only tier items of the input data
        for i in parsed:
            if i in tier:
                tier_image.append(i)

        # reassembles the data, and yields it
        if param == "s":
            yield "".join(tier_image)
        elif param == "m":
            yield "-".join(tier_image)
        elif param == "w":
            yield " ".join(tier_image)
                


def erase_test(data, tier, param, ngrams, symb, n):
    """ Erasing test: checks that removing the symb from the list
        of tier symbols will not predict ngrams that were not found
        in the initial data.
    """
    
    newtier = [i for i in tier if i != symb]
    
    # create a tier image of the input data, and ngramize it
    newdata = erase(data, newtier, param)
    new_ngrams = ngramize_all(newdata, n, param)
    
    return new_ngrams.issubset(ngrams)



def test_insert(obj, n, param, symb, ngrams):
    """ Insertion test: check that for in every (n-1)-gram of the
        original text it is possible to insert the symbols under
        consideration in it. If not, it is a tier symbol.
    """

    # get the list of (n-1)-grams
    test = ngramize_all(obj, n-1, param)
    
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



def test_remove(obj, n, param, symb, ngrams):
    """ Deleteion test: check that for all (n+1)-grams containint
        the symbol under consideration, this symbol can be removed
        from there. If not, it is a tier symbol.
    """

    # get the list of (n+1)-grams containing the needed symbol
    t = ngramize_all(obj, n+1, param)
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
